import pandas as pd
import json
from pandas.io.json import json_normalize
import numpy as np


class BasketSort:
    def __init__(self):

        self.df_products = self.data_frame_products()
        self.df_customers = self.data_frame_customers()
        self.df_orders = self.data_frame_orders()

        self.arr_of_appearance_from_orders_sep = []
        self.product_from_customer = []
        self.pairs_from_orders = []
        self.product_to_categories = {}

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

    # Списаок заказов пользователей
    def data_frame_orders(self):
        with open("orders.txt", "r", encoding='utf-8') as f:
            data = json.load(f)
            data = json_normalize(data)
            return pd.DataFrame(data)

    # Получаю все возможные комбинции из заказов причем двусторонние, т.е. [59, 88] и [88, 59] для удобной фильтрации
    # в следующем методе
    def get_pairs_from_orders(self) -> None:
        for i in range(len(self.df_orders)):
            temp1 = []
            for j in self.df_orders["products"][i]:
                temp1.append(j["id"])
            for n in temp1:
                for m in temp1:
                    if m != n:
                        self.pairs_from_orders.append([n, m])
        print("pairs_from_orders:")
        print(self.pairs_from_orders)

    # Получаем словарь, где ключ это id товара, значение словарь с названиями категорий и количством товаров
    # этой категории
    def get_product_to_categories(self) -> None:
        for i in self.pairs_from_orders:

            if not i[0] in self.product_to_categories:
                self.product_to_categories[i[0]] = dict([])

            if self.df_products["category"][i[1] - 1] in self.product_to_categories[i[0]]:
                self.product_to_categories[i[0]][self.df_products["category"][i[1] - 1]] += 1
            else:
                self.product_to_categories[i[0]][self.df_products["category"][i[1] - 1]] = 1

        print("product_to_categories")
        print(self.product_to_categories)

    # Для применения формулы требуется количество появлений категории (товара) отдельно от другого. То есть при
    # расчете знаменателя итоговой формулы нам нужно проходить не просто по спику заказов, а списку, из которого удлены
    # заказы, содержащие рассматриваемую комбинацию товаров. Для этого нужен этот промежуточный массив
    def appearance_from_orders_separated(self) -> None:
        for i in range(len(self.df_orders)):
            temp1 = []
            for j in self.df_orders["products"][i]:
                temp1.append(j["id"])
            self.arr_of_appearance_from_orders_sep.append(temp1)

        print("arr_of_appearance_from_orders_sep:")
        print(self.arr_of_appearance_from_orders_sep)

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
