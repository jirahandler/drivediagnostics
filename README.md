
# WD My Passport Drive Hardware Debug Smart Tools  Utility for Linux
## Installing

On an Ubuntu like distro, run the following commands to install necessary tools.

```
sudo apt install python3 python3-dev python3-pip git
```

Install these requirements as follows:

```
sudo python3 -m pip install py3_sg
sudo apt install smartmontools
sudo apt-get install sg3-utils
```

## Usage

```
#Change drive path string in wddiagnostics.py
#can be obtained by doing `lsblk`
sudo python3 wddiagnostics.py
sudo python3 wdscsi.py /dev/sdX
```


<h1>Disclaimer</h1>

Please use the scripts at your own risk. There is no support from Western Digital and developers of this repo assume no liability arising out of loss of information or drives crashing or security implications thereof.
