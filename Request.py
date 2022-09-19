import requests
import pandas as pd
import json
from pandas import json_normalize


class Request:
    def __init__(self, source: str):
        self.source = source
        self.data = self.get_data_from_html()

    def get_data_from_html(self):
        response = requests.get(self.source)

        print(response)
        return response.text

    def make_json_from_data(self):
        data = json.loads(self.data)

        return data

    def test_request(self):
        response = requests.get(self.source)
        print(response.text)



    # for line in r.text:
    #     print(line)

    with open("C:\\Users\\Vladimir\\Python\\pythonProject\\recommendation_module\\orders.txt", "r",
              encoding='utf-8') as f:
        data = json.load(f)
        data = json_normalize(data)
        df = pd.DataFrame(data)





