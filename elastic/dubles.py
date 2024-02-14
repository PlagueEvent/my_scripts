import requests
import json

url = "http://10.206.148.120:9200/msr_vk/_search?pretty"

payload = "{\n \"size\": 20,\n \"query\": {\n    \"bool\": {\n      \"must\": [\n        {\n          \"exists\": {\n            \"field\": \"data.snils\"\n          }\n        },\n        {\n          \"match_all\": {}\n        }\n      ]\n    }\n    }\n  },\n  \"aggs\": {\n    \"duplicates\": {\n      \"duplicate_detection\": {\n        \"field\": \"data.snils\",\n        \"max_docs_per_group\": 10\n      }\n    },\n    \"snils\": {\n      \"terms\": {\n        \"field\": \"data.snils\"\n      }\n    }\n  }\n}"
headers = {
  'Content-Type': 'application/json'
}

response = requests.request("GET", url, headers=headers, data=payload)

# print(response.text)


# Обработайте ответ
if response.status_code == 200:
  data = response.json()
  print  (data)
#   duplicates = data["aggs"]["duplicates"]["buckets"]
#   snils = data["aggs"]["snils"]["buckets"]
#
#   # Печать результатов
#   for duplicate in duplicates:
#     print(f"Дубликат: {duplicate['key']}")
#     print(f"Количество документов: {duplicate['doc_count']}")
#
#   for snil in snils:
#     print(f"SNILS: {snil['key']}")
#     print(f"Количество документов: {snil['doc_count']}")
# else:
#   print(f"Ошибка: {response.status_code}")
#   print(response.text)
