---
title: "POKY Documentation Conversion Tutorial"
layout: default
---

POKY manual is provided in HTML format.
You can find the [`POKY_documentation.pdf`](./POKY/doc/POKY_documentation.pdf) file in the current folder for convenience.
Then feed the file into the latest ChatGPT or other LLM of your choice and ask it questions.

# Converting POKY manual from HTML to PDF

> For Linux / MacOS 

This tutorial guides you through the process of converting HTML documentation to a single PDF 
file using `wkhtmltopdf` and `pdfunite`. This could be particularly 
useful for consolidating documentation into a single, easily distributable format, with which
you can create a POKY-specific ChatGPT 4 model.

## Prerequisites

Make sure your system is up-to-date and has the necessary packages installed. Open a terminal and execute the following commands:

```bash
sudo apt update
sudo apt install wkhtmltopdf poppler-utils
```

use `dnf` instead of `apt` on RHEL-based systems and `brew` on MacOS.

## Step-by-Step Guide

### 1. Navigate to the Documentation Directory

Change the directory to where your HTML files are located. In this example, we use the POKY documentation directory:

```bash
cd /opt/POKY/poky_linux/manual
```

### 2. Convert HTML Files to PDF

Use `wkhtmltopdf` to convert each HTML file in the directory to a PDF. The `--enable-local-file-access` option allows the tool to access local file resources, such as images and stylesheets:

```bash
for file in *.html; do
    wkhtmltopdf --enable-local-file-access "$file" "${file%.html}.pdf"
done
```

### 3. Merge PDF Files

Merge all the PDF files you've created into a single PDF document named `POKY_documentation.pdf`:

```bash
pdfunite *.pdf POKY_documentation.pdf
```
