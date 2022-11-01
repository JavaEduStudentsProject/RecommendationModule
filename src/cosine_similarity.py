import json
import math
import copy
from typing import Optional

import numpy as np
from numpy import ndarray, float64


class CosineSimilarity:

    def __init__(self, current_user_username, data):
        self.current_user_username = current_user_username
        self.data = data
        self.current_user_id = self.define_current_user_id()

        self.orders_from_all_users = self.orders_dict_creating()
        self.orders_from_all_users_except_current_user = self.set_orders_from_all_users_except_current_user()

    def define_current_user_id(self):
        userId = None
        for order in self.orders_list_regex():
            if order['username'] == self.current_user_username:
                return str(order['userId'])

        return userId

    def orders_list_regex(self):
        str_orders = eval(self.data)
        str_orders = str_orders.replace("{\'", "{\"")
        str_orders = str_orders.replace(" \'", " \"")
        str_orders = str_orders.replace(",\'", ",\"")
        str_orders = str_orders.replace("\':", "\":")
        str_orders = str_orders.replace("\',", "\",")
        str_orders = str_orders.replace("\'},", "\"},")
        str_orders = str_orders.replace("\'}]", "\"}]")
        print("str_orders")
        print(str_orders)
        orders = json.loads(str_orders)
        print("orders in 33 string:")
        print(orders)
        return orders

    def orders_dict_creating(self) -> dict:
        """
        Creating of dictionary with users and products, they have bought.
        :return: dictionary with users and sorted list of products, they have bought {user: [1, 2, 34, 56, 88]}
        """
        orders = self.orders_list_regex()
        orders_dict = {}
        all_orders_quantity = len(orders)
        for order in orders:
            # print("order in 45 str")
            # print(order)
            # print(order["userId"])
            if f"{order['userId']}" in orders_dict:
                for product in order['products']:
                    if product['id'] in orders_dict[f"{order['userId']}"].keys():
                        orders_dict[f"{order['userId']}"][product['id']][0] += product['quantity']
                        orders_dict[f"{order['userId']}"][product['id']][1] += 1
                    else:
                        orders_dict[f"{order['userId']}"][product['id']] = []
                        orders_dict[f"{order['userId']}"][product['id']].append(product['quantity'])
                        orders_dict[f"{order['userId']}"][product['id']].append(1)

            else:
                orders_dict[f"{order['userId']}"] = {}
                for product in order['products']:
                    orders_dict[f"{order['userId']}"][product['id']] = []
                    orders_dict[f"{order['userId']}"][product['id']].append(product['quantity'])
                    orders_dict[f"{order['userId']}"][product['id']].append(1)

        print(f"orders_dict: {orders_dict}")

        final_orders_dict = {}
        for user, products in orders_dict.items():
            final_orders_dict[user] = {}
            for product_id, coeff_list in products.items():
                final_orders_dict[user][product_id] = coeff_list[0] * (coeff_list[1] / all_orders_quantity)

        # self.anomaly_deleting(orders_dict)

        print(f"final_orders_dict: {final_orders_dict}")
        return final_orders_dict

    def anomaly_deleting(self, orders_dict: dict) -> None:
        """
        Deletes those users' rating sets, which are likely to be strange - all rates are similar
        :param ratings: Dict of all users with their rating sets
        :return: None
        """
        temp_rating_set = copy.deepcopy(orders_dict)
        for user, rates in temp_rating_set.items():
            if len(list(rates.values())) > 5 and sum(list(rates.values())) / len(list(rates.values())) == list(rates.values())[0]:
                orders_dict.pop(user)

    def set_orders_from_all_users_except_current_user(self) -> dict:
        """
        Sets dictionary of all users except current user
        :return: dict of users with dicts of their product ratings
        """
        if self.current_user_id is None:
            self.define_recommended_product()
        else:
            dict_without_current_user = copy.deepcopy(self.orders_from_all_users)
            dict_without_current_user.pop(self.current_user_id)
            return dict_without_current_user

    @staticmethod
    def dist_cosine(vector_one: dict, vector_two: dict) -> float:
        """
        Calculation of cosine similarity between two users
        :param vector_one: dictionary of first user's ratings
        :param vector_two: dictionary of second user's ratings
        :return: coefficient of cosine similarity
        """
        def dot_product(vector_one, vector_two):
            d = 0.0
            for dim in vector_one:
                if dim in vector_two:
                    d += vector_one[dim] * vector_two[dim]

            return d

        return dot_product(vector_one, vector_two) / (
                    math.sqrt(dot_product(vector_one, vector_one)) * math.sqrt(dot_product(vector_two, vector_two)))

    def user_rating_comparison(self) -> dict:
        """
        Comparison between current user and other users
        :return: dict of cosine similarities between current user and other users
        """
        matching_factor_dict = {}
        for user_id in self.orders_from_all_users_except_current_user:
            matching_factor_dict[user_id] = self.dist_cosine(self.orders_from_all_users[self.current_user_id],
                                                         self.orders_from_all_users_except_current_user[user_id])

        result = dict(sorted(matching_factor_dict.items(), key=lambda x: x[1], reverse=True)[:10])

        return result

    def get_product_id_list(self):
        comparison = self.user_rating_comparison()
        product_id_list = []
        for user in list(comparison.keys()):
            product_id_list.extend(list(self.orders_from_all_users_except_current_user[user].keys()))
        product_id_list = sorted(set(product_id_list))
        print("product_id_list: (139)")
        print(product_id_list)
        return product_id_list

    def empty_matrix_creating(self):
        """
        Creating empty matrix
        :return: numpy two dimensional array, matrix
        """

        comparison = self.user_rating_comparison()
        print(f"comparison: {comparison}")


        product_id_list = self.get_product_id_list()
        print(product_id_list)
        print(len(product_id_list))
        matrix = np.zeros((11, len(product_id_list) + 1))

        # list_1 = [75, 76, 13, 30, 63, 83, 58, 26, 56, 1]
        #
        # list_2 = [2, 3, 7, 9, 11, 12, 14, 16, 21, 23, 24, 25, 29, 30, 32, 36, 37, 39, 45, 46, 47, 48, 53, 54, 59, 61, 64, 66, 68, 70, 75, 76, 80, 81, 83, 84, 88, 90, 91, 92, 93, 94, 96, 97, 99]

        user_id_list = [int(x) for x in list(comparison.keys())]
        print(user_id_list)

        matrix[1:, 0] = user_id_list
        matrix[0, 1:] = product_id_list

        return matrix

    def matrix_filling(self) -> ndarray:
        """
        Fills empty matrix with ratings multiplied by cosine similarity
        :return:
        """
        comparison = self.user_rating_comparison()
        matrix = self.empty_matrix_creating()

        user_list = list(comparison.keys())

        for i, user_id in enumerate(list(matrix[1:, 0])):
            # product_id_list = list(map(lambda x: x.keys()[0], list(self.orders_from_all_users_except_current_user.values())[user_list[i]]))
            for j, product_id in enumerate(list(matrix[0, 1:])):
                if int(product_id) in self.orders_from_all_users[self.current_user_id].keys():
                    matrix[i + 1, j + 1] = np.NAN
                else:
                    if int(product_id) in list(self.orders_from_all_users_except_current_user[f"{int(user_id)}"].keys()):
                        matrix[i + 1, j + 1] = self.orders_from_all_users_except_current_user[f"{int(user_id)}"][int(product_id)] * 100 * comparison[f"{int(user_id)}"]

        return matrix

    def get_sum_for_each_product(self) -> list:
        """
        Calculating list of sums of all rates for each product, multiplied by cosine similarity
        :return: list of sums
        """
        matrix = self.matrix_filling()

        sum_ = matrix[1:, 1:].sum(axis=0)

        return sum_

    def get_final_weight_for_each_product(self, matrix: ndarray) -> dict:
        """
        Calculating final weights for each product by subtracting sum on sum of all users' cosine similarities
        :param matrix:
        :return: list of weights for each product
        """
        sum_ = self.get_sum_for_each_product()
        comparison = self.user_rating_comparison()

        final_weight_list = list(map(lambda x: x * sum(list(comparison.values())), sum_))

        product_id_list = self.get_product_id_list()
        final_weight_dict = dict(zip(product_id_list, final_weight_list))
        print(f"final_weight_dict: {final_weight_dict}")
        return final_weight_dict

    def print_user_table(self, matrix: list) -> None:
        """
        Printing table with users and there ratings for each product, multiplied by cosine similarity
        :return: None
        """
        user_list = list(self.orders_from_all_users_except_current_user.keys())
        for i in range(len(matrix)):
            print(f"{user_list[i]:<5}: {matrix[i]}")

    def define_recommended_product(self) -> Optional[list]:
        """
        Defines the product with the most weight and its number
        # :param weight_list: list of final weights for each product
        :return: recommendation
        """
        if self.current_user_id is None:
            return None

        final_weight_dict = {key:value for key, value in self.get_final_weight_for_each_product(self.matrix_filling()).items()
                             if f"{value}" != f"{np.NAN}"}
        sorted_weight_dict = dict(sorted(final_weight_dict.items(), key=lambda x: x[1], reverse=True)[:5])
        print(f"sorted_weight_dict: {sorted_weight_dict}")
        print(f"Dict of 5 recommended products: {sorted_weight_dict}")
        return list(sorted_weight_dict.keys())

    @staticmethod
    def print_sum_for_each_product(sum_list: list) -> None:
        """
        Printing sums of rating multiplied by cosine similarity for each product
        :return: None
        """
        print(f"sum: {sum_list:<5}")
