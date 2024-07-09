#!/bin/bash 

name=$1

ansible_path="/home/eugen/mycode/ansible"

#create playbook
mkdir $ansible_path/playbooks/$1
touch $ansible_path/playbooks/$1/main.yml

#create role
arr=("defaults" "tasks" "handlers" "templates" "files")

for item in ${arr[*]}
do 
	echo "Creating $ansible_path/roles/$name/$item"
	mkdir -p $ansible_path/roles/$name/$item
done

for item in ${arr[*]}
do 
	if [ "$item" != "templates" ]
	then
    echo "Creating $ansible_path/roles/$name/$item/main.yml"
	touch $ansible_path/roles/$name/$item/main.yml
    else
    	break
	fi
	
done
