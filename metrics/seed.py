import json
import requests
from queries import Queries

retrieved_size = 1000

for query in Queries:
    response = requests.get("http://localhost:9200/news_data/_search?q={}&size={}".format(query, retrieved_size))
    data = response.json()
    retrieved = data["hits"]["hits"]
    urls = list(map(lambda result: result["_source"]["URL"], retrieved))
    with open("relevant_results/{}.json".format(query), "w") as outfile:
        json.dump(urls, outfile)
