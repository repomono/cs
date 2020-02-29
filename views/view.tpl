% rebase("base.tpl", title=title)
% include("breadcrumb.tpl")
<main>
  <aside class="pane">
    <div class="header">
      <span class="tab-name">Files</span>
    </div>
    <div class="content file-tree" id="filetree">
      {{!file_tree}}
    </div>
  </aside>
  <div class="vertical divider"></div>
  <article>
    <section class="center pane">
      <div class="header">
        <span class="file-name">{{basename}}</span>
        <div class="buttons">
        </div>
      </div>
      <div class="content">
        <div class="source-code-viewer">
        % if defined("html_code"):
          <div class="line-numbers">
            % for l in range(1, line_count + 1):
            <a href="#L{{l}}">{{l}}<span id="L{{l}}"></span></a>
            % end
          </div>
          {{!html_code}}
        %end
        </div>
      </div>
    </section>
  </article>
</main>
