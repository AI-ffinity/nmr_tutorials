---
title: NMR Tutorials
layout: default
---

{% capture readme %}
{% include_relative README.md %}
{% endcapture %}
{{ readme
  | replace: '.md"', '.html"'
  | replace: '.md)</a>', '.html)</a>'
  | replace: '.md)', '.html)'
}}
