import csv
import json
import math
import copy

from pandas.io.json import json_normalize


class CosineSimilarity:

    def __init__(self, current_user, file_name):
        self.current_user = current_user
        self.file_name = file_name

        self.ratings_from_all_users = self.read_file()
        self.ratings_from_all_users_except_current_user = self.set_ratings_from_all_users_except_current_user()

    # @property
    # def ratings_from_all_users(self):
    #     return self.ratings_from_all_users
    #
    # @ratings_from_all_users.setter
    # def ratings_from_all_users(self):
    #     self.ratings_from_all_users = self.read_file()
    #
    # @property
    # def ratings_from_all_users_except_current_user(self):
    #     return self.ratings_from_all_users_except_current_user
    #
    # @ratings_from_all_users_except_current_user.setter
    # def ratings_from_all_users_except_current_user(self):
    #     dict_without_current_user = self.ratings_from_all_users.pop(self.current_user)
    #     self.ratings_from_all_users_except_current_user = dict_without_current_user

    def read_file(self) -> dict:
        """
        CSV-file parsing
        :return: dictionary with users with dictionaries {product: rating}
        """
        ratings = eval(self.file_name())
        print(f"ratings: {ratings}")
        # with open(self.file_name, "r", encoding='utf-8') as f:
        #     # string = f.read()
        #     # print(f"string: {string}")
        #     ratings = json.loads(f)
        #     print(f"ratings: {ratings}")
            # data = csv.reader(f)
            # print("test")
            # print(data)
            # ratings = dict()
            #
            # for line in data:
            #     user = line[0]
            #     product = line[1]
            #     rate = float(line[2])
            #     if user not in ratings:
            #         ratings[user] = dict()
            #
            #     ratings[user][product] = rate


        self.anomaly_deleting(ratings)
        print(ratings)
        return ratings

    def anomaly_deleting(self, ratings: dict) -> None:
        """
        Deletes those users' rating sets, which are likely to be strange - all rates are similar
        :param ratings: Dict of all users with their rating sets
        :return: None
        """
        temp_rating_set = copy.deepcopy(ratings)
        for user, rates in temp_rating_set.items():
            if len(list(rates.values())) > 5 and sum(list(rates.values())) / len(list(rates.values())) == list(rates.values())[0]:
                ratings.pop(user)

    def set_ratings_from_all_users_except_current_user(self) -> dict:
        """
        Sets dictionary of all users except current user
        :return: dict of users with dicts of their product ratings
        """
        dict_without_current_user = copy.deepcopy(self.ratings_from_all_users)
        dict_without_current_user.pop(self.current_user)
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

    def user_rating_comparison(self) -> list:
        """
        Comparison between current user and other users
        :return: list of cosine similarities between current user and other users
        """
        matching_factor_list = []
        for user in self.ratings_from_all_users_except_current_user:
            matching_factor_list.append(self.dist_cosine(self.ratings_from_all_users[self.current_user],
                                                         self.ratings_from_all_users_except_current_user[user]))

        return matching_factor_list

    def empty_matrix_creating(self) -> list:
        """
        Creating empty matrix
        :return: list of lists, matrix
        """
        matrix = []
        for _ in self.ratings_from_all_users_except_current_user.items():
            matrix.append([0 for _ in range(9)])

        return matrix

    def matrix_filling(self) -> list:
        """
        Fills empty matrix with ratings multiplied by cosine similarity
        :return:
        """
        comparison = self.user_rating_comparison()
        matrix = self.empty_matrix_creating()

        user_list = list(self.ratings_from_all_users_except_current_user.keys())
        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                if str(j + 1) in self.ratings_from_all_users[self.current_user].keys():
                    matrix[i][j] = False
                elif str(j + 1) in self.ratings_from_all_users_except_current_user[user_list[i]].keys():
                    matrix[i][j] = self.ratings_from_all_users_except_current_user[user_list[i]][f"{j + 1}"] * \
                                   comparison[i]

        return matrix

    def get_sum_for_each_product(self) -> list:
        """
        Calculating sum of all rates for each product, multiplied by cosine similarity
        :return: list of sums
        """
        matrix = self.matrix_filling()

        sum_ = [matrix[0][i] + matrix[1][i] + matrix[2][i] for i in range(len(matrix[0]))]
        return sum_

    # matrix = self.matrix_filling()
    # sum_list = []
    # for i in range(len(matrix)):
    #     for j in range(len(matrix[i])):
    #         sum_list[j] += matrix[i][j]
    #
    # return sum_list

    def get_final_weight_for_each_product(self, matrix: list) -> list:
        """
        Calculating final weights for each product by subtracting sum on sum of all users' cosine similarities
        :param matrix:
        :return: list of weights for each product
        """
        sum_ = self.get_sum_for_each_product()
        comparison = self.user_rating_comparison()
        print(f"matching_factor_list: {comparison}")
        weight_list = [sum_[i] / sum(comparison[0:3]) for i in range(len(matrix[0]))]

        return weight_list

    def print_user_table(self, matrix: list) -> None:
        """
        Printing table with users and there ratings for each product, multiplied by cosine similarity
        :return: None
        """
        user_list = list(self.ratings_from_all_users_except_current_user.keys())
        for i in range(len(matrix)):
            print(f"{user_list[i]:<5}: {matrix[i]}")

    def define_recommended_product(self) -> str:
        """
        Defines the product with the most weight and its number
        # :param weight_list: list of final weights for each product
        :return: recommendation
        """
        weight_list = self.get_final_weight_for_each_product(self.matrix_filling())
        max_ = 0
        product_number = None
        for index, rating in enumerate(weight_list):
            if rating > max_:
                max_ = rating
                product_number = index + 1

        print(f"We recommend you product {product_number} with rating {max_}")
        return f"We recommend you product {product_number} with rating {max_}"

    @staticmethod
    def print_matrix(matrix: list) -> None:
        """
        Printing the existing matrix
        :return: None
        """
        for i in range(len(matrix)):
            print(matrix[i])

    @staticmethod
    def print_sum_for_each_product(sum_list: list) -> None:
        """
        Printing sums of rating multiplied by cosine similarity for each product
        :return: None
        """
        print(f"sum: {sum_list:<5}")

    @staticmethod
    def print_weight_of_each_product(weight_list: list) -> None:
        """
        Printing the final result
        :return: None
        """
        print(f"result: {weight_list}")
