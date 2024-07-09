#!/bin/bash 

sudo virsh net-start vm_network
sudo virsh start build
sudo virsh start harbor
sudo virsh start newie
sleep 20
sudo virsh net-dhcp-leases vm_network
