import pandas as pd
import json
from pandas import json_normalize
from BestProductAlgorithm import BestProductsAlgorithm


class BasketCategoriesAlgorithm:
    def __init__(self, products, orders, customers):

        self.df_products = self.set_products(products)
        print("products")
        print(self.df_products)
        self.df_orders = self.set_orders(orders)
        print("orders")
        print(self.df_orders)
        self.df_customers = self.set_customers(customers)
        print("customers")
        print(self.df_customers)

        self.arr_of_order_combinations = []
        self.product_to_categories = {}
        self.possible_combinations = []
        self.arr_of_appearance_from_orders = []
        self.formula_result = []
        self.final_map = {}
        self.arr_recommendations_for_user = []
        self.arr_recommendations_for_user_id = []

    def parsing_products(self, raw_str):
        raw_str = raw_str.replace("{\'", "{\"")
        raw_str = raw_str.replace(" \'", " \"")
        raw_str = raw_str.replace("\':", "\":")
        raw_str = raw_str.replace("\',", "\",")
        raw_str = raw_str.replace("\'},", "\"},")
        raw_str = raw_str.replace("\'}]", "\"}]")
        raw_str = raw_str.replace("},  ,", "},")
        raw_str = raw_str.replace("  \"non_filter_features\": {", " ")
        raw_str = raw_str.replace("  },    \"filter_features\": { ", ",")
        raw_str = raw_str.replace("    },    ", " ,")

        return raw_str

    def parsing_orders(self, raw_str):
        raw_str = raw_str.replace("},  ,", "},")
        return raw_str

    def set_products(self, products):
        raw_str = eval(products)
        raw_products = self.parsing_products(raw_str)
        print("Danil product")
        print(raw_products)
        data = json.loads(raw_products)
        print("Final DFProducts")
        print(json_normalize(data))
        return pd.DataFrame(json_normalize(data))

    def set_orders(self, orders):
        raw_str = eval(orders)
        print("Danil order")
        print(raw_str)
        raw_orders = self.parsing_orders(raw_str)
        print("Danil raw_orders")
        print(raw_orders)
        data = json.loads(raw_orders)
        return pd.DataFrame(json_normalize(data))

    def set_customers(self, customers):
        str_to_parse = customers
        return list(map(int, str_to_parse.split(",")))


    def get_arr_of_order_combinations(self) -> None:
        """
        Получаю все возможные комбинции из заказов причем двусторонние, т.е. [59, 88] и [88, 59] для удобной фильтрации
        в методе получения словаря
        :return: None
        """
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

    def get_product_to_categories(self) -> None:
        """
        Получаем словарь, где ключ это id товара, значение словарь с названиями категорий и количством товаров
        этой категории
        :return: None
        """
        for i in self.arr_of_order_combinations:

            if not i[0] in self.product_to_categories:
                self.product_to_categories[i[0]] = dict([])

            if self.df_products["category"][i[1] - 1] in self.product_to_categories[i[0]]:
                self.product_to_categories[i[0]][self.df_products["category"][i[1] - 1]] += 1
            else:
                self.product_to_categories[i[0]][self.df_products["category"][i[1] - 1]] = 1

        print("product_to_categories")
        print(self.product_to_categories)

    def get_possible_combinations(self) -> None:
        """
        Из предыдущего словаря получаем список всех возможных комбинаций, встречающихся в заказах
        который и будем прогонять через формулу
        :return: None
        """
        for i in self.product_to_categories.items():
            for j in i[1].items():
                self.possible_combinations.append([i[0], j[0]])
        print("possible_combinations:")
        print(self.possible_combinations)

    def get_appearance_from_orders_separated(self) -> None:
        """
        Для применения формулы требуется количество появлений категории (товара) отдельно от другого. То есть при
        расчете знаменателя итоговой формулы нам нужно проходить не просто по спику заказов, а списку, из которого удлены
        заказы, содержащие рассматриваемую комбинацию товаров. Для этого нужен этот промежуточный массив
        :return: None
        """
        for i in range(len(self.df_orders)):
            temp1 = []
            for j in self.df_orders["products"][i]:
                temp1.append(j["id"])
            self.arr_of_appearance_from_orders.append(temp1)

        print("arr_of_appearance_from_orders:")
        print(self.arr_of_appearance_from_orders)

    def use_formula(self) -> None:
        """
        Применяем формулу. Перед самой формулой выбрасываем из рассмотрения те заказы, в которых встретилась
        рассчитываемая пара товаров
        :return:
        """
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

            value = self.product_to_categories[i[0]][i[1]] /(0.1 + temp_cleared_id.count(i[0]) + temp_cleared_category.count(i[1]))
            self.formula_result.append([i, value])

        print("formula_result")
        print(self.formula_result)

    def finalization(self) -> None:
        """
        Сравниваем полученные из формулы веса и оставляем только одну пару для каждого товара, получая финальный словарь
        :return: None
        """
        for i in self.formula_result:
            temp_array = i
            for j in self.formula_result:
                if i != j:
                    if i[0][0] == j[0][0]:
                        if temp_array[1] < j[1]:
                            temp_array = j
            self.final_map[temp_array[0][0]] = temp_array[0][1]

        print("final_map_basket:")
        print(self.final_map)
        # print("sorted_map")
        # print(sorted(self.final_map.items()))

    def get_recommendations_for_user(self, basket: list) -> list:
        """
        Метод принимает заказы пользователя и возварщает рекомендованные товары
        :param basket: list of product id in the basket:
        :return: arr of categories
        """
        print("Злоебучие заказы с фронта")
        print(basket)
        for i in basket:
            self.arr_recommendations_for_user.append(self.final_map.get(i))
        return self.arr_recommendations_for_user



    def unique(self, arr):
        """
        Method for making arr of unique categories for the last methods
        :param arr: arr of categories for customer
        :return: arr of unique categories for customer
        """
        output = []
        for x in arr:
            if x not in output:
                output.append(x)
        return output

    def do_basket_categories_algorithm(self, products):
        """
        Последовательное применение всех методов и получение рекоммендаций
        :return: list of products id
        """
        self.get_arr_of_order_combinations()
        self.get_product_to_categories()
        self.get_possible_combinations()
        self.get_appearance_from_orders_separated()
        self.use_formula()
        self.finalization()
        result_1 = self.get_recommendations_for_user(self.df_customers)
        print("res1")
        print(result_1)
        # Избавляемся от Null
        result_1 = [i for i in result_1 if i is not None]
        # Избавляемся от одинаковых категорий в списке
        result_1 = self.unique(result_1);
        print("res1")
        print(result_1)
        bp = BestProductsAlgorithm(products)
        result_2 = bp.do_best_product_algorithm()
        print("res2")
        print(result_2)
        for i in result_1:
            for j in result_2[i]:
                self.arr_recommendations_for_user_id.append(j)
        print("Spesial for you")
        print(self.arr_recommendations_for_user_id)
        return self.arr_recommendations_for_user_id
