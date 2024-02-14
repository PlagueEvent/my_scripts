import os

deployments = [
"isp-config-service",
"isp-gate-service",
"isp-routing-service",
"isp-system-service",
"kkd-address-service",
"kkd-admin-ui",
"kkd-atlas-service",
"kkd-cmd-tools",
"kkd-configuration-service",
"kkd-ctl",
"kkd-ext-ipev-service",
"kkd-kafka-adapter-service",
"kkd-metrics-service",
"kkd-notify-service",
"kkd-pipeline-service",
"kkd-rabbit-mq-adapter-service",
"kkd-stomp-adapter-service",
"kkd-vertica-service",
"msp-admin-service",
"msp-admin-ui",
]

stage_command = '/usr/local/bin/kubectl --kubeconfig /home/eugen/k8home/kkd-k8s-cls  --namespace kkd3-stage'
prod_command = '/usr/local/bin/kubectl --kubeconfig /home/eugen/k8home/kkd-k8s-prd  --namespace kkd3-prod'

stage_deployment = "/home/eugen/work_code/kkd30/kkd/PP/deployments"
prod_deployment = "/home/eugen/work_code/kkd30/kkd/PROD/deployments"

for deploy in deployments:
    os.system(f'{stage_command}  apply -f  {stage_deployment}/{deploy}.yml')
    os.system(f'{prod_command} apply -f  {prod_deployment}/{deploy}.yml')