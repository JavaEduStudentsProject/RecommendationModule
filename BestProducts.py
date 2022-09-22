import pandas as pd
import json
from pandas.io.json import json_normalize
import numpy as np


class BestProducts:
    def __init__(self):
        self.df_products = self.data_frame_products()
        self.map_of_categories = {}
        self.sort_arr = []
        self.ready = []

    def data_frame_products(self) :
        with open("products.txt", "r", encoding='utf-8') as f:
            data = json.load(f)
            data = json_normalize(data)
            return pd.DataFrame(data)

    # Получаем словарь словарей, в котором ключем будут названия категории, значем - словарь с ключем id товара
    # и значением рейтинга
    def get_product_to_categories(self):
        for i in range(len(self.df_products)):
            if not self.df_products["category"][i] in self.map_of_categories:
                self.map_of_categories[self.df_products["category"][i]] = dict([])

            self.map_of_categories[self.df_products["category"][i]][self.df_products["id"][i]] = self.df_products["rating"][i]

        print("map_of_categories")
        print(self.map_of_categories)

    def sort_and_get_final(self):
        self.sort_arr = list(self.map_of_categories.items())
        print(list(self.map_of_categories.items()))
        self.sort_arr.sort(key=lambda i: i[1])
        print(self.sort_arr)


    #         for i in df["products"][0]:
    #             self.arr_of_customer.append(i["id"])
    #
    #         print("arr_of_customer:")
    #         print(self.arr_of_customer)
    #
    # def customer_combinations(self) -> None:
    #     for i in self.arr_of_customer:
    #         for j in self.arr_of_customer:
    #             if j != i:
    #                 self.arr_of_customer_combinations.append([i, j])
    #
    #     print("arr_of_customer_combinations:")
    #     print(self.arr_of_customer_combinations)
    #
    # def appearance_from_orders_separated(self) -> None:
    #     with open("orders.txt", "r", encoding='utf-8') as f:
    #         data = json.load(f)
    #         data = json_normalize(data)
    #         df = pd.DataFrame(data)
    #
    #         for i in range(len(df)):
    #             temp1 = []
    #             for j in df["products"][i]:
    #                 temp1.append(j["id"])
    #             self.arr_of_appearance_from_orders_sep.append(temp1)
    #
    #         print("arr_of_appearance_from_orders_sep:")
    #         print(self.arr_of_appearance_from_orders_sep)
    #
    # def appearance_from_orders_unseparated(self) -> None:
    #     with open("orders.txt", "r", encoding='utf-8') as f:
    #         data = json.load(f)
    #         data = json_normalize(data)
    #         df = pd.DataFrame(data)
    #
    #         for i in range(len(df)):
    #             for j in df["products"][i]:
    #                 self.arr_of_appearance_from_orders_unsep.append(j["id"])
    #
    #         print("arr_of_appearance_from_orders_unsep:")
    #         print(self.arr_of_appearance_from_orders_unsep)
    #
    # def combinations_from_orders_separated(self) -> None:
    #     with open("orders.txt", "r", encoding='utf-8') as f:
    #         data = json.load(f)
    #         data = json_normalize(data)
    #         df = pd.DataFrame(data)
    #
    #         for i in range(len(df)):
    #             temp1 = []
    #             for j in df["products"][i]:
    #                 temp1.append(j["id"])
    #             temp2 = []
    #             for n in temp1:
    #                 for m in temp1:
    #                     if m != n:
    #                         temp2.append([n, m])
    #             self.arr_of_order_combinations_sep.append(temp2)
    #
    #         print("arr_of_order_combinations_sep:")
    #         print(self.arr_of_order_combinations_sep)
    #
    # def combinations_from_orders_unseparated(self) -> None:
    #     with open("orders.txt", "r", encoding='utf-8') as f:
    #         data = json.load(f)
    #         data = json_normalize(data)
    #         df = pd.DataFrame(data)
    #
    #         for i in range(len(df)):
    #             temp1 = []
    #             for j in df["products"][i]:
    #                 temp1.append(j["id"])
    #             for n in temp1:
    #                 for m in temp1:
    #                     if m != n:
    #                         self.arr_of_order_combinations_unsep.append([n, m])
    #
    #         print("arr_of_order_combinations_unsep:")
    #         print(self.arr_of_order_combinations_unsep)
    #
    # def set_from_orders(self) -> None:
    #
    #     # self.set_orders = set(self.arr_of_appearance)
    #
    #     for item in self.arr_of_appearance_from_orders_unsep:
    #         if item not in self.set_orders:
    #             self.set_orders.append(item)
    #
    #     print("set_orders:")
    #     print(self.set_orders)
    #
    # def bilateral_combination_to_estimate(self) -> None:
    #     for i in self.set_orders:
    #         for j in self.set_orders:
    #             if j != i:
    #                 self.arr_of_possible_combinations.append([i, j])
    #
    #     print("arr_of_possible_combinations:")
    #     print(self.arr_of_possible_combinations)
    #
    # def formula(self) -> None:
    #     for i in self.arr_of_possible_combinations:
    #         temp_cleared = []
    #         for j in self.arr_of_appearance_from_orders_sep:
    #             if not (i[0] in j and
    #                     i[1] in j):
    #                 for n in j:
    #                     temp_cleared.append(n)
    #
    #         value = self.arr_of_order_combinations_unsep.count(i) / (0.1 +
    #                 temp_cleared.count(i[0]) + temp_cleared.count(i[1]))
    #         self.semi_result.append([i, value])
    #
    #     print("semi_result")
    #     print(self.semi_result)
    #
    # def finalization(self) -> None:
    #     for i in self.semi_result:
    #         temp_array = i
    #         for j in self.semi_result:
    #             if i != j:
    #                 if i[0][0] == j[0][0]:
    #                     if temp_array[1] < j[1]:
    #                         temp_array = j
    #         self.final_map[temp_array[0][0]] = temp_array[0][1]
    #
    #     print("final_map:")
    #     print(self.final_map)
    #     print("sorted_map")
    #     print(sorted(self.final_map.items()))
    #
    # def recommendations_for_user(self, basket:list) -> list:
    #     for i in basket:
    #         self.arr_recommendations_for_user.append(self.final_map.get(i))
    #     print("SPECIAL FOR YOU!!!")
    #     print(self.arr_recommendations_for_user)


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
