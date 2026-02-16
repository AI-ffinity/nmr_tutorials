---
title: "quick search"
layout: default
---





<img src="./images/home.svg" width=100, height=100 />



Find all `.md` files and concatenate their contents into a single `all.md` file.

**Linux / MacOS**

```bash
find . -type f -name "*.md" | sort | while IFS= read -r f; do cat "$f"; echo -e "\n"; done > all.md
```

**Windows (PowerShell)**

```powershell
Get-ChildItem -Recurse -Filter *.md | Sort-Object FullName | ForEach-Object { Get-Content $_.FullName; "`n" } | Out-File -FilePath all.md -Encoding utf8
```

Upload the `all.md` file to ChatGPT and ask it for instructions.

Back to the [main page](https://ai-ffinity.github.io/nmr_tutorials/)