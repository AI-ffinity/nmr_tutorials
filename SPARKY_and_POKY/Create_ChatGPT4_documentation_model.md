# POKY Documentation Conversion Tutorial

This tutorial guides you through the process of converting HTML documentation to a single PDF 
file using `wkhtmltopdf` and `pdfunite` on a system running Ubuntu. This could be particularly 
useful for consolidating documentation into a single, easily distributable format, with which
you can create a POKY-specific ChatGPT 4 model.

## Prerequisites

Make sure your system is up-to-date and has the necessary packages installed. Open a terminal and execute the following commands:

```bash
sudo apt update
sudo apt install wkhtmltopdf poppler-utils
```

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

### 4. Load the Documentation

You can find the [`POKY_documentation.pdf`](doc/POKY_documentation.pdf) file in the current folder for convenience.
Then create a new ChatGPT 4 model by loading the POKY_documentation.pdf file. Hopefuly,
the new model will be able to answer to your questions related to POKY's usage.