Find all `.md` files and concatenate their contents into a single `all.md` file.

```bash
find . -type f -name "*.md" | sort | while IFS= read -r f; do cat "$f"; echo -e "\n"; done > all.md
```

Upload the `all.md` file to ChatGPT and ask it for instructions.