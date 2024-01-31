
import subprocess
import pprint as pp
import re
import os
import datetime
import argparse

'''
version: '1.2'
'''

now = datetime.datetime.now()
date = now.strftime("%d%m%Y")

kubectl = '/usr/local/bin/kubectl'

kubeconf_stage = '/home/eugen/k8home/kkd-k8s-cls'
kubeconf_prod = '/home/eugen/k8home/kkd-k8s-prd'

command_stage = [kubectl, '--kubeconfig',
                 kubeconf_stage,
                 'get', 'pods',
                 '--namespace', 'kkd3-stage']

command_prod = [kubectl, '--kubeconfig',
                kubeconf_prod,
                'get', 'pods',
                '--namespace', 'kkd3-prod']

stage_route = '/usr/local/bin/kubectl --kubeconfig /home/eugen/k8home/kkd-k8s-cls  --namespace kkd3-stage'
prod_route = '/usr/local/bin/kubectl --kubeconfig /home/eugen/k8home/kkd-k8s-prd  --namespace kkd3-prod'




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



def inner_pod_command(route, name,command):
    str =route + f' exec -i {{name}} -- {{command}}'.format(name=name, command=command)
    return str




def get_dump(route,command):
    name = get_pod_name('kkd-ctl', command)
    config_name = f'config_bkp_stage_{{date}}.json'.format(date=date)

    #Команды
    command_ls = 'ls -al'
    create_dump = f'kkdctl config dump --config="{{config_name}}" --force'.format(config_name=config_name)
    save_dump = f'cp {{name}}:/opt/msp/kkdctl/{{config_name}} ~/kkd_files/{{config_name}}'\
        .format(name=name, config_name=config_name)

    make_tar = f'tar -cvzf config.tar.gz  {{config_name}}'.format(config_name=config_name)
    # get_error_log = f'cp {{name}}:/opt/msp/kkdctl/config.tar.gz ~/kkd_files/config.tar.gz'.format(name=name)
    get_tar = f'cp {{name}}:/opt/msp/kkdctl/config.tar.gz ~/kkd_files/config.tar.gz'.format(name=name)
    #полный вариант на выполнение
    #Делаем дамп

    os.system(inner_pod_command(route, name, create_dump))
    os.system(inner_pod_command(route, name, make_tar))

    #смотрим что у нас все ок
    

    #переносим конфиг на локальный
    # os.system(route + f' {{command}}'.format(command=save_dump))
    os.system(route + f' {{command}}'.format(command=get_tar))


def load_config(route,command):
    name = get_pod_name('kkd-ctl', command)
    new_config_name = f'kkd_configuration_service.json'

    apply_config = f'kkdctl config apply --config="{{new_config_name}}"'.format(new_config_name=new_config_name)
    load_config = f'cp ~/kkd_files/{{new_config_name}} {{name}}:/opt/msp/kkdctl/{{new_config_name}}' \
        .format(name=name, new_config_name=new_config_name)


    #загружаем конфиг
    load_config
    os.system(route + f' {{load_config}}'.format(load_config=load_config))


    # full_command = route + f' {{load_config}}'.format(load_config=get_error_log)
    # os.system(full_command)
    # print('load error - OK')

    #Применяем конфиг
    # full_command = route + f' exec -i {{name}} -- {{command}}'.format(name=name, command=apply_config)
    # os.system(inner_pod_command(route, name, apply_config))
    # print('apply config - OK')


def lists(name, route):
    command_ls = 'ls -al'
    os.system(inner_pod_command(route, name, command_ls))



# dump_config(stage_route)



# get_pod_name('kkd-configuration-service', command_prod)
# get_pod_name('kkd-configuration-service', command_stage)
# get_pod_name('kkd-ctl', command_stage)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--version', action='version', version='%(prog)s 1.1')
    parser.add_argument('-t', '--target', choices={"stage", "prod"}, help='Целевой контур')
    parser.add_argument('--test', action='store_true', help='попробовать, что получится')
    parser.add_argument('--get_dump', action='store_true', help='получить дамп конфига')
    parser.add_argument('--upload_config', action='store_true', help='Загрузить и применить конфига')

    args = parser.parse_args()


    try:
        if args.target == 'stage':
            route = stage_route
            command = command_stage
            print("route: ", route, "command: ", command)
        elif args.target == 'prod':
            route = prod_route
            command = command_prod
    except:
        print("ошибка в выборе целевого контура")


    try:
        if args.test == True:
            get_pod_name("kkd-ctl", command)
    except:
        print('ОШИБКАБЛЕАТЬ!!!!1111: не указан целевой контур')

    try:
        if args.get_dump == True:
            get_dump(route, command)
    except:
        print('ОШИБКАБЛЕАТЬ!!!!1111: во время дампа')

    try:
        if args.upload_config == True:
            load_config(route, command)
    except:
        print('ОШИБКАБЛЕАТЬ!!!!1111 в загрузке файла')
