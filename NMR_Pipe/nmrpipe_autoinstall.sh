#!/bin/sh

install_dir=/opt/nmrpipe

set -e # fail as soon there is an error

# check that we are running a 64 bit system

num_bits=`getconf LONG_BIT`
if $num_bits != "64"; then
  echo This is not a 64 bit OS
  exit 1
fi

# download_dir=`mktemp -d /tmp/tmp_download.XXX`

download_dir=./tmp_download
if [ ! -d "$download_dir" ]; then
	mkdir $download_dir
fi

URL_list="https://www.ibbr.umd.edu/nmrpipe/install.com \
          https://www.ibbr.umd.edu/nmrpipe/binval.com \
          https://www.ibbr.umd.edu/nmrpipe/NMRPipeX.tZ \
          https://www.ibbr.umd.edu/nmrpipe/s.tZ \
          https://www.ibbr.umd.edu/nmrpipe/dyn.tZ \
          https://www.ibbr.umd.edu/nmrpipe/talos.tZ \
          http://spin.niddk.nih.gov/bax/software/smile/plugin.smile.tZ"

for i in $URL_list; do
    filename=$(basename "$i")
    if [ -f "$download_dir/$filename" ]; then
        echo "File $filename already exists. Skipping download."
    else
        echo "Downloading $i"
        wget --directory-prefix="$download_dir" --no-directories "$i"
    fi
done

if [ ! -d "$install_dir" ]; then 
    sudo mkdir "$install_dir"
fi
	
sudo find $download_dir -maxdepth 1 -mindepth 1 -type f -name '*.com' -exec cp {} "$install_dir" \;

sudo find "$install_dir" -maxdepth 1 -mindepth 1 -type f -name '*.com' -exec chmod 755 {} \;

sudo dpkg --add-architecture i386

sudo apt-get update

echo ttf-mscorefonts-installer msttcorefonts/accepted-mscorefonts-eula select true | sudo debconf-set-selections

sudo apt-get install -y tcsh
#sudo apt-get install -y default-jdk
#sudo apt-get install -y default-jre
#sudo apt-get install -y libc6:i386
#sudo apt-get install -y libstdc++6:i386
sudo apt-get install -y xterm
sudo apt-get install -y xfonts-75dpi
sudo apt-get install -y libx11-6:i386
sudo apt-get install -y libxext6:i386
sudo apt-get install -y msttcorefonts

sudo sh -c "cd $install_dir ; ./install.com +src $(realpath $download_dir)"

echo "Installation done"

echo "Modifying the ~/.cshrc to make nmrPipe initialize"

# Define the path to the example.cshrc file
example_cshrc="$install_dir/example.cshrc"

# Define the user's .cshrc file
user_cshrc="$HOME/.cshrc"

# Define a backup file
backup_cshrc="$user_cshrc.bak"

# Check if the example.cshrc file exists
if [ ! -f "$example_cshrc" ]; then
    echo "Error: $example_cshrc does not exist."
    exit 1
fi

if [ ! -f "$user_cshrc" ]; then
    echo "The ~/.cshrc file for current user does not exist yet, creating..."
    touch ~/.cshrc
    echo "#!/bin/sh" >> ~/.cshrc
fi

# Create a backup of the user's .cshrc file
cp "$user_cshrc" "$backup_cshrc"
echo "Backup of $user_cshrc created at $backup_cshrc"

# Append lines 7 to 18 from example.cshrc to .cshrc
echo "Copying content of $example_cshrc to $user_cshrc (code only)"
sed -n '7,18p' "$example_cshrc" >> "$user_cshrc"

read -p "Remove the installation files? (y/N) " user_flag

if [[ "$user_input" =~ ^[Yy]$ ]]; then
    echo "Cleaning up..."
    eval "rm -rf ./tmp_download"
else
    echo "Leaving the installation files in place."
fi

echo "Done."
