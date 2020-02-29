% if defined("filename"):
  % breadcrumbs = filename.split("/")
  % last = breadcrumbs.pop()
% else:
  % breadcrumbs = []
  % last = ""
% end
<nav>
  <ol class="breadcrumb">
    <li>//</li>
    % for b in breadcrumbs:
    <li>{{b}}</li>
    <li>/</li>
    % end
    <li class="active">{{last}}</li>
  </ol>
</nav>
