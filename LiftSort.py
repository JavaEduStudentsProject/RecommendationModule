import pandas as pd
import json
from pandas.io.json import json_normalize
import numpy as np


class LiftSort:
    def __init__(self):

        self.df_customers = self.data_frame_customers()
        self.df_orders = self.data_frame_orders()

        self.arr_of_customer = []

        self.arr_of_appearance_from_orders_sep = []
        self.arr_of_order_combinations = []

        self.set_orders = []
        self.arr_of_possible_combinations = []
        self.semi_result = []

        self.final_map = {}
        self.arr_recommendations_for_user = []

    def data_frame_products(self):
        with open("products.txt", "r", encoding='utf-8') as f:
            data = json.load(f)
            data = json_normalize(data)
            return pd.DataFrame(data)

    def data_frame_customers(self):
        with open("customer.txt", "r", encoding='utf-8') as f:
            data = json.load(f)
            data = json_normalize(data)
            return pd.DataFrame(data)

    def data_frame_orders(self):
        with open("orders.txt", "r", encoding='utf-8') as f:
            data = json.load(f)
            data = json_normalize(data)
            return pd.DataFrame(data)

    # Списаок заказов пользователей

    def products_from_customer(self) -> None:
        for i in self.df_customers["products"][0]:
            self.arr_of_customer.append(i["id"])

        print("arr_of_customer:")
        print(self.arr_of_customer)

    # Данный список нужен для того, чтобы мы могли для каждой пары товаров искать по формуле знаменатель, т.к. в нем
    # число появлений товаров раздельно, то есть нам надо исключить из поиска корзины в которых 2 товара были вместе
    def appearance_from_orders_separated(self) -> None:
        for i in range(len(self.set_orders)):
            temp1 = []
            for j in self.set_orders["products"][i]:
                temp1.append(j["id"])
            self.arr_of_appearance_from_orders_sep.append(temp1)

        print("arr_of_appearance_from_orders_sep:")
        print(self.arr_of_appearance_from_orders_sep)

    def combinations_from_orders(self) -> None:
        for i in self.arr_of_appearance_from_orders_sep:
            temp1 = []
            for j in self.arr_of_appearance_from_orders_sep:
                i[j]

        print("arr_of_order_combinations_unsep:")
        print(self.arr_of_order_combinations)


def formula(self) -> None:
    for i in self.arr_of_possible_combinations:
        temp_cleared = []
        for j in self.arr_of_appearance_from_orders_sep:
            if not (i[0] in j and
                    i[1] in j):
                for n in j:
                    temp_cleared.append(n)

        value = self.arr_of_order_combinations_unsep.count(i) / (0.1 +
                                                                 temp_cleared.count(i[0]) + temp_cleared.count(
                    i[1]))
        self.semi_result.append([i, value])

    print("semi_result")
    print(self.semi_result)


def finalization(self) -> None:
    for i in self.semi_result:
        temp_array = i
        for j in self.semi_result:
            if i != j:
                if i[0][0] == j[0][0]:
                    if temp_array[1] < j[1]:
                        temp_array = j
        self.final_map[temp_array[0][0]] = temp_array[0][1]

    print("final_map:")
    print(self.final_map)
    print("sorted_map")
    print(sorted(self.final_map.items()))


def recommendations_for_user(self, basket: list) -> list:
    for i in basket:
        self.arr_recommendations_for_user.append(self.final_map.get(i))
    print("SPECIAL FOR YOU!!!")
    print(self.arr_recommendations_for_user)

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
