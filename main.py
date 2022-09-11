from CosineSimilarity import CosineSimilarity

if __name__ == '__main__':
    # CURRENT_USER = 'ivan'
    # FILE_NAME = "C:\\Users\\Vladimir\\Python\\pythonProject\\recommendation_module\\venv\\data.csv"
    user_ivan_comparison = CosineSimilarity('ivan', "C:\\Users\\Vladimir\\Python\\pythonProject\\recommendation_module\\venv\\data.csv")

    empty_matrix = user_ivan_comparison.empty_matrix_creating()
    user_ivan_comparison.print_matrix(empty_matrix)

    filled_matrix = user_ivan_comparison.matrix_filling()
    user_ivan_comparison.print_matrix(filled_matrix)
    user_ivan_comparison.print_user_table(filled_matrix)

    weight_list = user_ivan_comparison.get_final_weight_for_each_product(filled_matrix)
    user_ivan_comparison.define_recommended_product(weight_list)