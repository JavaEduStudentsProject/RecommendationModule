import pandas as pd
import json
from pandas.io.json import json_normalize


class LiftSort:

    @staticmethod
    def products_from_customer() -> list:
        with open("customer.txt", "r", encoding='utf-8') as f:
            data = json.load(f)
            data = json_normalize(data)
            df = pd.DataFrame(data)

            arr_of_customer = []

            for i in df["products"]:
                print(i)
                arr_of_customer.append(i["id"])
                print(arr_of_customer)


    @staticmethod
    def list_of_all_products() -> list:
        with open("products.txt", "r", encoding='utf-8') as f:
            data = json.load(f)
            data = json_normalize(data)
            df = pd.DataFrame(data)

            arr_of_products = []

            for i in df:
                print(i)
                arr_of_products.append(i["id"])
                print(arr_of_products)

    @staticmethod
    def list_of_orders() -> list:
        with open("products.txt", "r", encoding='utf-8') as f:
            data = json.load(f)
            data = json_normalize(data)
            df = pd.DataFrame(data)

            arr_of_orders = []

            for i in df:
                print(i)
                arr_of_orders.append(i["id"])
                print(arr_of_orders)

    @staticmethod
    def possible_combinations() -> list:



# print(df["products"])
# print(df["products"][0])
#
# print(df["id"])
# print(df["id"][0])
#
# list_ = []
# for i in df["products"][0]:
#     print(i['id'])
#     list_.append(i['id'])
#     print(list_)
