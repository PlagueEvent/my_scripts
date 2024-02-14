#!/bin/bash

curl -XGET 'http://10.206.148.120:9200/msr_vk/_search?pretty' -H 'Content-Type: application/json' -d '{
 "size": 4100,
 "query": {
    "bool": {
      "must": [
        {
          "exists": {
            "field": "data.snils"
          }
        },
        {
          "match_all": {}
        }
      ]
    }
    }
  },
  "aggs": {
    "duplicates": {
      "duplicate_detection": {
        "field": "data.snils",
        "max_docs_per_group": 10
      }
    },
    "snils": {
      "terms": {
        "field": "data.snils"
      }
    }
  }
}'