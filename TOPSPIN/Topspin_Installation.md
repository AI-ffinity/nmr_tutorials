---
title: "Topspin installation on Linux"
layout: default
---

# Topspin installation on Linux 

Here we consider just Debian-based systems. 
> ![NOTE]
> Bruker officially supports only RHEL-based Linux, such as AlmaLinux. 

1. Log in to your Bruker account, find the latest release of Topspin and download it. The file will have `.sh` extension. 
2. Meanwhile, go to the [Wibu.com](https://www.wibu.com/support/user/user-software.html) 
and download and install its debian package: https://www.wibu.com/support/user/user-software/file/download/14414.html 
3. Once the downloads finish, navigate to the `.sh` file and issue 

```bash
$ sudo topspin-4.4.0-linux.sh
```
where 4.4.0 is the TopSpin version.

Note, that the installation will not work if you just open the shell as root; also, it will not work without `sudo` priveleges.

4. The installer will offer several installation options: choose the defaults. It will also create an NMR superuser and the `nmrsu` group. You will not need to interact with it too much.
5. Once the installation is complete, start the Codemeter. (You can now find it in the application menu)
6. **Important!** Allow yourself as a user to access and execute files in the topspin folder. The simplest way to do this is to issue

```bash
sudo chmod 777 -R /opt/topspin-4.4.0/
```
7. Navigate to the Topspin download page and generate yourself the license code (academic or evaluation). Copy the 25-symbol code. 
8. *Make sure you have the internet connection.* Start TopSpin: either from the terminal or from the application menu in your desktop environment. It will prompt you to add a license. Follow the prompts and paste the code.

9. Your installation is complete!

> ![NOTE]
> Sometimes Topspin can not start because of the error "Failed to connect to a data server". To us, the reasons are yet unknown, but perhaps they have something to di with the network and firewall configuration. If this happens, simply turn *off* your internet connection while starting TopSpin. Turn it back on once the GUI is loaded. 
