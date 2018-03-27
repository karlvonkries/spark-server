
Full Installation on a Raspberry PI
=======================================

If you're already familiar with the command line, or you are comfortable setting up a new [pi SD card](http://elinux.org/RPi_Easy_SD_Card_Setup), and following a script, here's the quick install guide!


```sh

	sudo apt-get update
	sudo apt-get upgrade

	#
	#	Expand your partition to fill your SD card
	#	Make sure you're booting into the console
	#
	# sudo raspi-config
	sudo update-rc.d lightdm disable

	#
	#	Set up Ethernet as a server
	#	Modified instructions from [this wiki](https://www.raspberrypi.org/documentation/configuration/wireless/access-point.md)
	sudo apt-get install dnsmasq
	sudo systemctl stop dnsmasq

	# Configure static IP
	echo -e "interface eth0\n    static ip_address=192.168.4.1/24" >> /etc/dhcpcd.conf
	sudo service dhcpcd restart

	# Set up dnsmasq
	sudo mv /etc/dnsmasq.conf /etc/dnsmasq.conf.orig
	echo -e "interface=eth0   # Use the require interface - usually eth0\n   dhcp-range=192.168.4.2,192.168.4.20,255.255.255.0,24h" | sudo tee -a /etc/dnsmasq.conf

	sudo systemctl start dnsmasq

	# Add routing and masquerade
	sudo sed -i "s/^#net.ipv4.ip_forward=1.*/net.ipv4.ip_forward=1/" /etc/sysctl.conf
	sudo iptables -t nat -A  POSTROUTING -o wlan0 -j MASQUERADE
	sudo sh -c "iptables-save > /etc/iptables.ipv4.nat"

	sudo sed -i "s/^exit 0.*/iptables-restore < \/etc\/iptables.ipv4.nat\n\nexit 0/" /etc/rc.local

	sudo reboot

	#
	#	Install Node.js
	# [You can set up other versions here](https://nodejs.org/en/download/package-manager/#debian-and-ubuntu-based-linux-distributions)
	curl -sL https://deb.nodesource.com/setup_6.x | sudo -E bash -
  	sudo apt-get install -y nodejs


	#
	#	Install DFU-Util
	#
	sudo apt-get install libusb-1.0-0-dev
	wget http://dfu-util.sourceforge.net/releases/dfu-util-0.9.tar.gz
	tar xvf dfu-util-0.9.tar.gz
	cd dfu-util-0.9
	./configure
	make
	sudo make install


	#
	#	Install the Particle-CLI
	#
	sudo npm install -g particle-cli --unsafe-perm

	#
	#	Setup a project folder
	#

	sudo mkdir /spark
	sudo chown pi /spark
	sudo chgrp pi /spark
	cd /spark

	git clone https://github.com/karlvonkries/spark-server.git
	cd spark-server/
	npm install
	# node main.js

	sudo cp 50-particle.rules /etc/udev/rules.d/50-particle.rules
	sudo cp PhotonInit.py /home/pi/Desktop/PhotonInit.py
	chmod +x /home/pi/Desktop/PhotonInit.py
	# Create desktop binaries folder
	mkdir /home/pi/Desktop/binaries

	# Install PM2
	sudo npm install pm2 -g
	pm2 start dist/main.js
	# pm2 startup
	sudo env PATH=$PATH:/usr/bin /usr/lib/node_modules/pm2/bin/pm2 startup systemd -u pi --hp /home/pi
	pm2 save

	particle config local_cloud apiUrl "http://192.168.4.1:8080"
	particle config local_cloud

	particle setup

```

After this you can follow the normal instructions for setting up the server.  I had trouble getting `particle identify` working so I used `ssh` to get my server key and set up the device from my main computer.
https://www.raspberrypi.org/documentation/remote-access/ssh/

If you want the node server to run whenever the Pi starts up, look into `pm2`:
https://github.com/Unitech/pm2
