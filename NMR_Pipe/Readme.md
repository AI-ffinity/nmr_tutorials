# Single line NMR Pipe installation

Download, install and set up [NMRPipe](https://spin.niddk.nih.gov/bax/NMRPipe/) on Ubuntu 22.04 Jammy LTS with the single line!

```sh
wget -qO- PUT_URL_TO_THE_SCRIPT_HERE | bash
```

Alternatively, download the script [nmrpipe_autoinstall.sh](./nmrpipe_autoinstall.sh) and execute it. 

The script will take care of downloading the source files, installing dependancies, and the post-installation modifications of the ~/.cshrc file.

## Requirements
* Ubuntu 22.04.4 LTS
* Admin rights

## Flow
1. Creates a folder `tmp_download` in the current directory
2. Checks if the necessary files already exist and downloads them, if necessary
3. Creates the installation directory: `/opt/nmrpipe` (here you'll have to type your admin password)
4. Installs the dependancies
5. Copies the installation scripts there and executes the `install.com`
6. Modifes the `~/.cshrc` file as directed in README_NMRPIPE_USERS
7. Prompts user to remove the `tmp_download` folder with the source archives.

Simple as that!





