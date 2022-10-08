import pandas as pd
import json
from pandas.io.json import json_normalize
import numpy as np


class BasketCategoriesAlgorithm:
    def __init__(self, products, orders, basket):

        self.df_products = self.set_products(products)
        self.df_customers = self.set_basket(basket)
        self.df_orders = self.set_orders(orders)

        self.arr_of_order_combinations = []
        self.product_to_categories = {}
        self.possible_combinations = []
        self.arr_of_appearance_from_orders = []
        self.formula_result = []
        self.final_map = {}
        self.arr_recommendations_for_user = []

        self.arr_of_customer = []

    # def data_frame_products(self):
    #     with open("products.txt", "r", encoding='utf-8') as f:
    #         data = json.load(f)
    #         data = json_normalize(data)
    #         return pd.DataFrame(data)

    # def data_frame_customers(self):
    #     with open("customer.txt", "r", encoding='utf-8') as f:
    #         data = json.load(f)
    #         data = json_normalize(data)
    #         return pd.DataFrame(data)
    #
    # def data_frame_orders(self):
    #     with open("orders.txt", "r", encoding='utf-8') as f:
    #         data = json.load(f)
    #         data = json_normalize(data)
    #         return pd.DataFrame(data)

    def set_products(self, products):
        raw_products = eval(products)
        data = json.loads(raw_products)
        return pd.DataFrame(json_normalize(data))

    def set_orders(self, orders):
        raw_orders = eval(orders)
        data = json.loads(raw_orders)
        return pd.DataFrame(json_normalize(data))

    def set_basket(self, basket):
        raw_basket = eval(basket)
        data = json.loads(raw_basket)
        return pd.DataFrame(json_normalize(data))

     # Список заказов пользователей
    def get_products_from_customer(self) -> None:
        for i in self.df_customers["products"][0]:
            self.arr_of_customer.append(i["id"])

        print("arr_of_customer:")
        print(self.arr_of_customer)

    # Получаю все возможные комбинции из заказов причем двусторонние, т.е. [59, 88] и [88, 59] для удобной фильтрации
    # в методе получения словаря
    def get_arr_of_order_combinations(self) -> None:
        for i in range(len(self.df_orders)):
            temp1 = []
            for j in self.df_orders["products"][i]:
                temp1.append(j["id"])
            for n in temp1:
                for m in temp1:
                    if m != n:
                        self.arr_of_order_combinations.append([n, m])
        print("pairs_from_orders:")
        print(self.arr_of_order_combinations)


    # Получаем словарь, где ключ это id товара, значение словарь с названиями категорий и количством товаров
    # этой категории
    def get_product_to_categories(self) -> None:
        for i in self.arr_of_order_combinations:

            if not i[0] in self.product_to_categories:
                self.product_to_categories[i[0]] = dict([])

            if self.df_products["category"][i[1] - 1] in self.product_to_categories[i[0]]:
                self.product_to_categories[i[0]][self.df_products["category"][i[1] - 1]] += 1
            else:
                self.product_to_categories[i[0]][self.df_products["category"][i[1] - 1]] = 1

        print("product_to_categories")
        print(self.product_to_categories)

    # Из предыдущего словаря получаем список всех возможных комбинаций, встречающихся в заказах
    # который и будем прогонять через формулу
    def get_possible_combinations(self) -> None:
        for i in self.product_to_categories.items():
            for j in i[1].items():
                self.possible_combinations.append([i[0], j[0]])
        print("possible_combinations:")
        print(self.possible_combinations)

    # Для применения формулы требуется количество появлений категории (товара) отдельно от другого. То есть при
    # расчете знаменателя итоговой формулы нам нужно проходить не просто по спику заказов, а списку, из которого удлены
    # заказы, содержащие рассматриваемую комбинацию товаров. Для этого нужен этот промежуточный массив
    def get_appearance_from_orders_separated(self) -> None:
        for i in range(len(self.df_orders)):
            temp1 = []
            for j in self.df_orders["products"][i]:
                temp1.append(j["id"])
            self.arr_of_appearance_from_orders.append(temp1)

        print("arr_of_appearance_from_orders:")
        print(self.arr_of_appearance_from_orders)

    # Применяем формулу. Перед самой формулой выбрасываем из рассмотрения те заказы, в которых встретилась
    # рассчитываемая пара товаров
    def use_formula(self) -> None:
        for i in self.possible_combinations:
            temp_cleared_id = []
            temp_cleared_category = []
            for j in self.arr_of_appearance_from_orders:
                temp = []
                for m in j:
                    temp.append(self.df_products["category"][m - 1])
                if not (i[0] in j and
                        i[1] in temp):
                    for n in j:
                        temp_cleared_id.append(n)
                        temp_cleared_category.append(self.df_products["category"][n - 1])

            # 0,1 доблены в сумму что б не получалось деления на 0
            value = self.product_to_categories[i[0]][i[1]] /(0.1 + temp_cleared_id.count(i[0]) + temp_cleared_category.count(i[1]))
            self.formula_result.append([i, value])

        print("formula_result")
        print(self.formula_result)

    # Сравниваем полученные из формулы веса и оставляем только одну пару для каждого товара, получая финальный словарь
    def finalization(self) -> None:
        for i in self.formula_result:
            temp_array = i
            for j in self.formula_result:
                if i != j:
                    if i[0][0] == j[0][0]:
                        if temp_array[1] < j[1]:
                            temp_array = j
            self.final_map[temp_array[0][0]] = temp_array[0][1]

        print("final_map:")
        print(self.final_map)
        print("sorted_map")
        print(sorted(self.final_map.items()))

    # Метод принимает заказы пользователя и возварщает рекомендованные товары
    def get_recommendations_for_user(self, basket: list) -> list:
        for i in basket:
            self.arr_recommendations_for_user.append(self.final_map.get(i))
        print("SPECIAL FOR YOU!!!")
        print(self.arr_recommendations_for_user)
        return self.arr_recommendations_for_user

    def do_basket_categories_algorithm(self):
        self.get_arr_of_order_combinations()
        self.get_product_to_categories()
        self.get_possible_combinations()
        self.get_appearance_from_orders_separated()
        self.use_formula()
        self.finalization()
        self.get_products_from_customer()
        self.get_recommendations_for_user(self.arr_of_customer)