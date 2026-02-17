---
title: "Single line NMR Pipe installation"
permalink: /NMR_Pipe/
layout: default
---

# Single line NMR Pipe installation

Download, install and set up [NMRPipe](https://spin.niddk.nih.gov/bax/NMRPipe/) on Ubuntu with the single line!

```sh
wget -qO- https://raw.githubusercontent.com/AI-ffinity/nmr_tutorials/refs/heads/main/NMR_Pipe/nmrpipe_autoinstall.sh | bash
```

Alternatively, download the script [nmrpipe_autoinstall.sh](./nmrpipe_autoinstall.sh) and execute it. 

The script will take care of downloading the source files, installing dependancies, and the post-installation modifications of the ~/.cshrc file.

## Requirements
* Ubuntu 22 or older
* Admin rights
* `wget` to fetch the script
* `csh` or `tcsh` shell to run NMR pipe

### Note on Ubuntu 24

NMRPipe release from 03. Apr 2025 made the software compatible with the newest versions of Ubuntu. However, if the GUI still won't display, an old solution may help:

> * Get the following two files (X11 libraries from Ubuntu 20)
>   * https://www.ibbr.umd.edu/nmrpipe/libX11.so.6
>   * https://www.ibbr.umd.edu/nmrpipe/libXau.so.6
> * Put them in the nmrbin.*/lib directory.

Tested on Ubuntu 24-based TuxedoOS with KDE desktop environment.  

If something still doesn't work, try MATE desktop environment, which was used on the NMRPipe development virtual machine. 
 If there are still problems, use NMRPipe in a virtual machine. 

See this [thread](https://groups.io/g/nmrpipe/message/3225) for more details.

## Flow
1. Creates a folder `tmp_download` in the current directory
2. Checks if the necessary files already exist and downloads them, if necessary
3. Creates the installation directory: `/opt/nmrpipe` (here you'll have to type your admin password)
4. Installs the dependancies
5. Copies the installation scripts there and executes the `install.com`
6. Modifes the `~/.cshrc` file as directed in README_NMRPIPE_USERS
7. Prompts user to remove the `tmp_download` folder with the source archives.

Simple as that!




