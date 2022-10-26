import pandas as pd
import json
from pandas.io.json import json_normalize
import numpy as np


class BestProductsAlgorithm:
    def __init__(self):
        self.df_products = self.data_frame_products()
        self.map_of_categories = {}
        self.final_map = {}

    def data_frame_products(self) :
        with open("products.txt", "r", encoding='utf-8') as f:
            data = json.load(f)
            data = json_normalize(data)
            return pd.DataFrame(data)

    # def set_products(self, products):
    #     print("DANIL STAFF")
    #     print("Danil products" + products)
    #     print(type(products))
    #     raw_products = eval(products)
    #     print("Danil raw_products" + raw_products)
    #     print(type(raw_products))
    #     # str_products = eval(raw_products)
    #     # print(str_products)
    #     # print(type(str_products))
    #     data = json.loads(raw_products)
    #     return pd.DataFrame(json_normalize(data))

    # Получаем словарь словарей, в котором ключем будут названия категории, значем - словарь с ключем id товара
    # и значением рейтинга
    def get_product_to_categories(self):
        for i in range(len(self.df_products)):
            if not self.df_products["category"][i] in self.map_of_categories:
                self.map_of_categories[self.df_products["category"][i]] = dict([])

            self.map_of_categories[self.df_products["category"][i]][self.df_products["id"][i]] = self.df_products["rating"][i]

        print("map_of_categories")
        print(self.map_of_categories)

    # Сортируем по убыванию оценок и записывааем в новый словарь только 2 лучших товара из каждой ктегории
    def sort_and_get_final(self):
        for i in self.map_of_categories.items():
            temp1 = sorted(i[1].items(), key=lambda x: x[1], reverse=True)
            temp2 = []
            for j in range(2):
                temp2.append(temp1[j][0])
            self.final_map[i[0]] = temp2
        print("final_map")
        print(self.final_map)
        return self.final_map

    def do_best_product_algorithm(self):
        self.get_product_to_categories()
        result = self.sort_and_get_final()
        return result

