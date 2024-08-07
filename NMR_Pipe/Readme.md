# Single line NMR Pipe installation

Download, install and set up [NMRPipe](https://spin.niddk.nih.gov/bax/NMRPipe/) on Ubuntu 22.04 Jammy LTS with the single line!

```sh
wget -qO- https://github.com/AI-ffinity/nmr_tutorials/blob/8ea33433f58a31e45138687217b24309d5c2ef2f/NMR_Pipe/nmrpipe_autoinstall.sh | bash
```

Alternatively, download the script [nmrpipe_autoinstall.sh](./nmrpipe_autoinstall.sh) and execute it. 

The script will take care of downloading the source files, installing dependancies, and the post-installation modifications of the ~/.cshrc file.

## Requirements
* Ubuntu 22.04.4 LTS
* Admin rights
* `wget` to fetch the script
* `csh` or `tcsh` shell to run NMR pipe

## Note on Ubuntu 24
The default installation will work for the command-line-based programs within NMR Pipe - however, NMRDraw will not open the window. To fix this: 
* Get the following two files (X11 libraries from Ubuntu 20)
  * https://www.ibbr.umd.edu/nmrpipe/libX11.so.6
  * https://www.ibbr.umd.edu/nmrpipe/libXau.so.6
* Put them in the nmrbin.*/lib directory.

See this [thread](https://groups.io/g/nmrpipe/topic/99567785) for more details.

## Flow
1. Creates a folder `tmp_download` in the current directory
2. Checks if the necessary files already exist and downloads them, if necessary
3. Creates the installation directory: `/opt/nmrpipe` (here you'll have to type your admin password)
4. Installs the dependancies
5. Copies the installation scripts there and executes the `install.com`
6. Modifes the `~/.cshrc` file as directed in README_NMRPIPE_USERS
7. Prompts user to remove the `tmp_download` folder with the source archives.

Simple as that!





