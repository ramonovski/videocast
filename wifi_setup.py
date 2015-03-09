# Network setup script

import os
import time


interfaces_content = """
auto lo

iface lo inet loopback
iface eth0 inet dhcp

allow-hotplug wlan0
iface wlan0 inet manual
wpa-roam /etc/wpa_supplicant/wpa_supplicant.conf
iface default inet dhcp
"""

wpa_supplicant_content = """
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1

"""

if '__main__' == __name__:
    
    network_section = ""
    ssid = raw_input("Enter WIFI network SSID: ")
    has_password = raw_input("Does this network require a password to connect (yes/no)? ")
    if has_password.lower().startswith('y'):
        password = raw_input("Enter password for WIFI network: ")
        network_section = """
network={
    ssid="%s"
    psk="%s"
}
""" % (ssid, password)

    else:
        network_section = """
network={
    ssid="%s"
    key_mgmt=NONE
}
""" % ssid

    # Backup original network files if not already backed up
    if not os.path.exists("/etc/network/interfaces.newscast_backup"):
        os.system("mv /etc/network/interfaces /etc/network/interfaces.newscast_backup")
    
    if not os.path.exists("/etc/wpa_supplicant/wpa_supplicant.conf.newscast_backup"):
        os.system("mv /etc/wpa_supplicant/wpa_supplicant.conf /etc/wpa_supplicant/wpa_supplicant.conf.newscast_backup")
    
    open("/etc/network/interfaces", "w").write(interfaces_content)
    
    wpa_final_content = wpa_supplicant_content + network_section
    open("/etc/wpa_supplicant/wpa_supplicant.conf", "w").write(wpa_final_content)
    
    print("Updated network configuration written!")
    print("Restarting network ...")
    
    os.system("service networking stop; service networking start")
	time.sleep(1)
	os.system("ifup --force wlan0")
    
    print("Done!")
