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


#Получаем полное имя целевого пода
def inner_pod_command(route, name,command):
    str =route + f' exec -i {{name}} -- {{command}}'.format(name=name, command=command)
    return str

#Делаем дамп конфиг файла
def get_dump(route,command,cluster_name):
    cluster_name = cluster_name
    tar_name = f'config_{{cluster_name}}_{{date}}.tar.gz'.format(cluster_name=cluster_name, date=date)
    name = get_pod_name('kkd-ctl', command)
    config_name = f'config_bkp_{{cluster_name}}_{{date}}.json'.format(cluster_name=cluster_name, date=date)

    #Команды
    command_ls = 'ls -al'
    create_dump = f'kkdctl config dump --config="{{config_name}}" --force'.format(config_name=config_name)
    make_tar = f'tar -cvzf {{tar_name}}  {{config_name}}'\
        .format(tar_name=tar_name,config_name=config_name)
    get_tar = f'cp {{name}}:/opt/msp/kkdctl/{{tar_name}}' \
              f' ~/kkd_files/{{tar_name}}'\
        .format(name=name,tar_name=tar_name)

    #Делаем дамп
    os.system(inner_pod_command(route, name, create_dump))
    os.system(inner_pod_command(route, name, make_tar))
    #переносим конфиг на локальный
    os.system(route + f' {{command}}'.format(command=get_tar))
    #Распаковочка
    sleep(5)
    os.system(f'tar -xvf ~/kkd_files/{{tar_name}} -C ~/kkd_files'.format(tar_name=tar_name))

def upload_config(route,command):
    name = get_pod_name('kkd-ctl', command)
    new_config_name = f'kkd_configuration_service.json'

    apply_config = f'kkdctl config apply --config="{{new_config_name}}"'.format(new_config_name=new_config_name)
    load_config = f'cp ~/kkd_files/{{new_config_name}} {{name}}:/opt/msp/kkdctl/{{new_config_name}}' \
        .format(name=name, new_config_name=new_config_name)


    #загружаем конфиг
    os.system(route + f' {{load_config}}'.format(load_config=load_config))

def lists(name, route):
    command_ls = 'ls -al'
    os.system(inner_pod_command(route, name, command_ls))


'''Основная чать скрипта'''
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--version', action='version', version='%(prog)s 0.1.4')
    parser.add_argument('-t', '--target', choices={"stage", "prod"}, help='Целевой контур')
    # parser.add_argument('--test', action='store_true', help='попробовать, что получится')
    parser.add_argument('--get-dump', action='store_true', help='получить дамп конфига')
    parser.add_argument('--upload-config', action='store_true', help='Загрузить и применить конфига')

    args = parser.parse_args()

#Заполняем ключи для корректного получения дампа
    try:
        if args.target == 'stage':
            route = stage_route
            command = command_stage
            cluster_name = 'stage'
            print("route: ", route, "command: ", command)
        elif args.target == 'prod':
            route = prod_route
            command = command_prod
            cluster_name = 'prod'
    except:
        print("ошибка в выборе целевого контура")

    try:
        if args.test == True:
            get_pod_name("kkd-ctl", command)
    except:
        print('ОШИБКАБЛЕАТЬ!!!!1111: во время дампа')


    try:
        if args.get_dump == True:
            get_dump(route, command, cluster_name)
    except:
        print('ОШИБКАБЛЕАТЬ!!!!1111: во время дампа')


    try:
        if args.upload_config == True:
            upload_config(route, command)
    except:
        print('ОШИБКАБЛЕАТЬ!!!!1111 в загрузке файла')


