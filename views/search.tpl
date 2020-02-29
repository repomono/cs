% rebase("base.tpl", title=query)

<nav>
  <ol class="breadcrumb">
    % if total_count == 0:
    <li>No results for your query</li>
    % else:
    <li>Results <b>1 - {{len(search_results)}}</b> of <b>{{total_count}}</b></li>
    % end
    <li>(<b>{{elapsed_seconds}}</b> seconds)</li>
  </ol>
</nav>

<main id="search_results">
<article>
% for path, lines in search_results:
<section class="search-result pane">
  <div class="header">
    <span class="file-name">{{path}}</span>
  </div>
  % line_numbers = sorted(lines.keys())
  % start = 0
  % while start < len(line_numbers):
    % offset = find_hunk_offset(line_numbers, start)
    <div class="content">
      <div class="source-code-viewer">
        <div class="line-numbers">
          % for i in range(start, start + offset):
            % l = line_numbers[i]
            <a href="/view/{{path}}#L{{l}}">{{l}}</a>
          % end
        </div>
        <pre><code>\\
          % for i in range(start, start + offset):
            % l = line_numbers[i]
            % line = lines[l]
            % if len(line) == 0:
              % line = ' '
            % end
<a class="line" href="/view/{{path}}#L{{l}}">{{!highlight_query(line, query)}}</a>
          % end
</code></pre>
      </div>
    </div>
    % start += offset
  % end
</section>
% end
</article>
</main>
