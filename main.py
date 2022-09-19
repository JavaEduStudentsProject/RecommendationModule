import pandas as pd
import json
from pandas.io.json import json_normalize

from CosineSimilarity import CosineSimilarity
from Request import Request

if __name__ == '__main__':

    user_ivan_comparison = CosineSimilarity('ivan', "C:\\Users\\Vladimir\\Python\\pythonProject\\recommendation_module\\venv\\data.csv")

    empty_matrix = user_ivan_comparison.empty_matrix_creating()
    CosineSimilarity.print_matrix(empty_matrix)

    filled_matrix = user_ivan_comparison.matrix_filling()
    # CosineSimilarity.print_matrix(filled_matrix)
    user_ivan_comparison.print_user_table(filled_matrix)

    # weight_list = user_ivan_comparison.get_final_weight_for_each_product(filled_matrix)
    user_ivan_comparison.define_recommended_product()

    # new_request = Request('https://dummyjson.com/carts')
    # new_request.make_json_from_data()

    # rest_api_request = Request('http://localhost:9090/order-data')
    # rest_api_request.test_request()
