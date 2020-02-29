import bottle
import html
import os
import re
import subprocess

from bottle import get, redirect, request, route, run, static_file, template, view
from hashlib import sha256
from pathlib import Path
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import guess_lexer_for_filename
from pygments.util import ClassNotFound
from time import time

self_dir = Path(os.path.dirname(os.path.realpath(__file__)))


@route("/assets/<filename:path>")
def assets(filename):
    return static_file(filename, root=str(self_dir / "assets"))


class CustomHtmlFormatter(HtmlFormatter):
    def wrap(self, source, outfile):
        # skip <div class="highlight"></div>
        return self._wrap_pre(self._wrap_code(source))


def file_tree_html(tree, current_filename=""):
    html = "<ol>"
    for child in tree.iterdir():
        if child.is_dir():
            child_prefix = str(child) + "/"
            li_id = sha256(child_prefix.encode("utf-8")).hexdigest()
            if current_filename.startswith(child_prefix):
                li_class = "collapse"
            else:
                li_class = "expand"
            child_html = file_tree_html(child, current_filename)
            html += template("""
                             <li class="{{li_class}}" id="{{li_id}}">
                               <div class="dir" title="{{name}}">
                                 <a href="#">{{name}}</a>
                               </div>
                               {{!child_html}}
                             </li>
                             """,
                             li_class=li_class,
                             li_id=li_id,
                             name=child.name,
                             child_html=child_html)
    for child in tree.iterdir():
        if not child.is_dir():
            if current_filename == str(child):
                selected = " selected"
            else:
                selected = ""
            html += template("""
                             <li>
                               <div class="file{{selected}}" title="{{name}}">
                                 <a href="/view/{{child_path}}">{{name}}</a>
                               </div>
                             </li>
                             """,
                             selected=selected,
                             name=child.name,
                             child_path=str(child))
    html += "</ol>"
    return html


@get("/view/<filename:path>")
@view("view")
def view_file(filename):
    with open(filename, "r") as f:
        lines = f.readlines()
    line_count = len(lines)
    content = "".join(lines)
    try:
        lexer = guess_lexer_for_filename(filename, content)
        html_code = highlight(content, lexer, CustomHtmlFormatter())
    except ClassNotFound:
        html_code = template("<pre><code>{{content}}</code></pre>",
                             content=content)
    file_tree = file_tree_html(Path("."), filename)
    basename = Path(filename).name
    return {
        "title": basename,
        "filename": filename,
        "basename": basename,
        "line_count": line_count,
        "html_code": html_code,
        "file_tree": file_tree,
    }


@get("/")
@view("view")
def index():
    return {
        "title": "/",
        "file_tree": file_tree_html(Path(".")),
        "basename": "/",
    }


def split_by(delim, lst):
    result = []
    current = []
    for item in lst:
        if item == delim:
            if len(current) > 0:
                result.append(current)
                current = []
        else:
            current.append(item)
    if len(current) > 0:
        result.append(current)
    return result


def parse_grep_section(grep_section):
    path = None
    lines = {}
    for line in grep_section:
        if not line.startswith("./"):
            # TODO report error?
            return None, None
        line = line[2:]
        this_path, line = line.split("\0", maxsplit=1)
        if path is None:
            path = this_path
        elif path != this_path:
            # TODO report error?
            return None, None
        line_number, line = re.split("[-:]", line, maxsplit=1)
        lines[int(line_number)] = line
    return path, lines


def parse_grep_output(output):
    # [path] -> ( [line number] -> "line text" )
    search_results = {}
    for grep_section in split_by("--", filter(len, output.splitlines())):
        path, lines = parse_grep_section(grep_section)
        if path is None:
            continue
        if path in search_results:
            search_results[path].update(lines)
        else:
            search_results[path] = lines
    return list(search_results.items())


def highlight_query(line, query):
    parts = line.split(query)
    html_parts = map(html.escape, parts)
    span = template('<span class="highlight">{{query}}</span>', query=query)
    return span.join(html_parts)


def find_hunk_offset(line_numbers, start):
    start_ln = line_numbers[start]
    offset = 0
    while start + offset < len(line_numbers):
        ln = line_numbers[start + offset]
        if ln != start_ln + offset: break
        offset += 1
    return offset


@get("/search")
@view("search")
def search():
    query = request.query.get("q")
    if len(query) == 0:
        redirect("/")
        return
    grep_args = [
        "grep",
        "--fixed-strings",
        "--no-messages",
        "--with-filename",
        "--line-number",
        "--null",
        "--context=1",
        "--binary-files=without-match",
        "--recursive",
        query,
        ".",
    ]
    start_time = time()
    grep = subprocess.run(grep_args, capture_output=True)
    search_results = parse_grep_output(grep.stdout.decode("utf-8"))
    total_count = len(search_results)
    max_show_count = 100
    search_results = search_results[:max_show_count]
    elapsed_seconds = time() - start_time
    return {
        "query": query,
        "total_count": total_count,
        "search_results": search_results,
        "elapsed_seconds": "%.3f" % elapsed_seconds,
        "find_hunk_offset": find_hunk_offset,
        "highlight_query": highlight_query,
    }


if __name__ == "__main__":
    bottle.TEMPLATE_PATH.insert(0, str(self_dir / "views"))
    run(host="localhost", port=56789, debug=True)
