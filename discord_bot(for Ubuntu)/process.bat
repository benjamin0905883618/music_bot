#from https://linziyou.info/2020/03/19/%E5%B0%87-ubuntu-18-04-%E7%9A%84-python-%E6%8F%9B%E8%87%B3-python-3-7/
sudo apt update
sudo apt install python3.7
sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.7 1
sudo update-alternatives --config python3
sudo rm /usr/bin/python3
sudo ln -s python3.7 /usr/bin/python3
sudo apt install python3-pip
sudo apt-get install screen
python3 -V
sudo apt-get install python3.7-devls
sudo apt install ffmpeg

pip3 install discord
pip3 install youtube_dl
pip3 install PyNaCl

