import pandas as pd
import json
from pandas.io.json import json_normalize
import numpy as np


class BestProductsAlgorithm:
    def __init__(self, products):
        self.df_products = self.set_products(products)
        self.map_of_categories = {}
        self.final_map = {}

    def parsing(self, raw_str):
        raw_str = raw_str.replace("{\'", "{\"")
        raw_str = raw_str.replace(" \'", " \"")
        raw_str = raw_str.replace("\':", "\":")
        raw_str = raw_str.replace("\',", "\",")
        raw_str = raw_str.replace("},  ,", "},")

        raw_str = raw_str.replace("  \"non_filter_features\": {", " ")
        raw_str = raw_str.replace("  },    \"filter_features\": { ", ",")
        raw_str = raw_str.replace("    },    ", " ,")

        return raw_str

    def set_products(self, products):
        print("DANIL STAFF")
        raw_str = eval(products)
        print("Danil raw_str")
        print(raw_str)
        raw_products = self.parsing(raw_str)
        print("Danil raw_products" + raw_products)
        print(type(raw_products))

        data = json.loads(raw_products)
        print("Final DF")
        print(json_normalize(data))
        return pd.DataFrame(json_normalize(data))

    def get_product_to_categories(self):
        """
        Получаем словарь словарей, в котором ключем будут названия категории, значем - словарь с ключем id товара
        и значением рейтинга
        :return: None
        """
        for i in range(len(self.df_products)):
            if not self.df_products["category"][i] in self.map_of_categories:
                self.map_of_categories[self.df_products["category"][i]] = dict([])

            self.map_of_categories[self.df_products["category"][i]][self.df_products["id"][i]] = self.df_products["rating"][i]

    def sort_and_get_final(self):
        """
        Сортируем по убыванию оценок и записывааем в новый словарь только 2 лучших товара из каждой ктегории
        :return: dict of recommendations
        """
        for i in self.map_of_categories.items():
            temp1 = sorted(i[1].items(), key=lambda x: x[1], reverse=True)
            temp2 = []
            for j in range(4):
                temp2.append(temp1[j][0])
            self.final_map[i[0]] = temp2
        print("final_map")
        print(self.final_map)
        print(type(self.final_map))
        return self.final_map

    def do_best_product_algorithm(self):
        """
        Последовательное применение всех методов и получение рекоммендаций
        :return: dict of recommendations
        """
        self.get_product_to_categories()
        result = self.sort_and_get_final()
        return result

