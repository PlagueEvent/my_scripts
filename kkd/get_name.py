#!/usr/bin/env python3
import subprocess
import pprint as pp
import re
import os
import datetime
import argparse
from time import sleep as sleep

'''
version: '0.1.4'

Скрипт для взаимоствия с kkd-ctl:
- делает бекап конфигурационного файла
- загружает конфиг файл 
- применяет его 

'''

'''Персональные настройки'''
kubectl = '/usr/local/bin/kubectl'
kubeconf_stage = '/home/eugen/k8home/kkd-k8s-cls'
kubeconf_prod = '/home/eugen/k8home/kkd-k8s-prd'
stage_route = '/usr/local/bin/kubectl --kubeconfig /home/eugen/k8home/kkd-k8s-cls  --namespace kkd3-stage'
prod_route = '/usr/local/bin/kubectl --kubeconfig /home/eugen/k8home/kkd-k8s-prd  --namespace kkd3-prod'

'''Общие переменные'''
now = datetime.datetime.now()
date = now.strftime("%d%m%Y")

command_stage = [kubectl, '--kubeconfig',
                 kubeconf_stage,
                 'get', 'pods',
                 '--namespace', 'kkd3-stage']

command_prod = [kubectl, '--kubeconfig',
                kubeconf_prod,
                'get', 'pods',
                '--namespace', 'kkd3-prod']


'''Функции и команды'''
#Получаем имя пода
def get_pod_name(name, command):
    name = name+'.*'

    p = subprocess.Popen(command,
                         stdout=subprocess.PIPE)
    while True:
        line = p.stdout.readline()
        if not line:
            break
        line = (str(line).split(' ')[0])
        line = (line.replace("b'", ""))
        result = re.match(name, line)
        if result is not None:
            print(result.string)
            pod_name = result.string
            return pod_name


get_pod_name("kkd-ctl", command_stage)