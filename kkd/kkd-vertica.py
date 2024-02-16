import json
import requests
import warnings

'''
наши даты
'''
date_payload = json.dumps({
  "from": "2024-02-14",
  "to": "2024-02-15"
})

'''
Получаем админский токен
'''
headers = {
    'X-APPLICATION-TOKEN': 'oRZE4kiNJ3zdBRk9IN9EYmhO6yZ45EvfxQN2xCKQSkNql629JzERN4YT5HLux3vX',
}

json_data = {
    'email': 'admin@ex.com',
    'password': 'Xnp5kRZh',
}
warnings.simplefilter('ignore' ,requests.packages.urllib3.exceptions.InsecureRequestWarning)
response = requests.post('https://kkd-admin.data.corp/api/admin/auth/login',
                         headers=headers, json=json_data, verify=False)

r = json.loads(response.text)

admin_token = r.get('token')

'''
Отправляем запрос на целевую ручку
'''
url = "https://kkd-admin.data.corp/api/kkd-vertica-service/resend"
#Для проверке на стейдже
# date_payload = json.dumps({
#   "snils": "202-619-243 25",
# })


headers = {
  'X-APPLICATION-TOKEN': 'oRZE4kiNJ3zdBRk9IN9EYmhO6yZ45EvfxQN2xCKQSkNql629JzERN4YT5HLux3vX',
  'X-AUTH-ADMIN': admin_token,
  'Content-Type': 'application/json'
}

response = requests.request("GET", url, headers=headers, data=date_payload,  verify=False)


