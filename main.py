import pandas as pd
import json
from pandas.io.json import json_normalize

from CosineSimilarity import CosineSimilarity
from LiftSort import LiftSort

if __name__ == '__main__':

    # CURRENT_USER = 'ivan'
    # FILE_NAME = "C:\\Users\\Vladimir\\Python\\pythonProject\\recommendation_module\\venv\\data.csv"
    #
    # user_ivan_comparison = CosineSimilarity('ivan', "C:\\Users\\danpr\\PycharmProjects\\recommendation_module\\venv\\data.csv")
    #
    # empty_matrix = user_ivan_comparison.empty_matrix_creating()
    # user_ivan_comparison.print_matrix(empty_matrix)
    #
    # filled_matrix = user_ivan_comparison.matrix_filling()
    # user_ivan_comparison.print_matrix(filled_matrix)
    # user_ivan_comparison.print_user_table(filled_matrix)
    # CosineSimilarity.print_matrix()
    #
    # weight_list = user_ivan_comparison.get_final_weight_for_each_product(filled_matrix)
    # user_ivan_comparison.define_recommended_product(weight_list)
    #
    # LiftSort.list_of_all_products()

    second_method = LiftSort()

    second_method.get_products_from_customer()

    second_method.get_appearance_from_orders_separated()
    second_method.get_combinations_from_orders()
    second_method.use_formula()









