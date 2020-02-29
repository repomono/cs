<!doctype html>
<meta charset="utf-8">
<title>{{title}}</title>

<link rel="stylesheet" href="/assets/reset.css">
<link rel="stylesheet" href="/assets/main.css">

<form id="search_bar" action="/search" method="GET">
  <a href="/"><img src="/assets/logo.png" class="logo"></a>
  <input type="text" name="q" class="query" value="{{get("query", "")}}">
  <input type="submit" value="Search" class="submit">
</form>

{{!base}}

<script src="/assets/jquery-3.4.1.min.js"></script>
<script src="/assets/main.js"></script>
