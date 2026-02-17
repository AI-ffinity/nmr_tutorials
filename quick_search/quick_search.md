---
title: "quick search"
layout: default
---

Find all `.md` files and concatenate their contents into a single `all.md` file.

Download the repository from https://github.com/AI-ffinity/nmr_tutorials, navigate to that folder and open a terminal.

**Linux / MacOS**

```bash
find . -type f -name "*.md" | sort | while IFS= read -r f; do cat "$f"; echo -e "\n"; done > all.md
```

**Windows (PowerShell)**

```powershell
Get-ChildItem -Recurse -Filter *.md | Sort-Object FullName | ForEach-Object { Get-Content $_.FullName; "`n" } | Out-File -FilePath all.md -Encoding utf8
```

Upload the `all.md` file to ChatGPT and ask it for instructions.
