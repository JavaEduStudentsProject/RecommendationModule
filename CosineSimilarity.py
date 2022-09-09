import csv
import math


def read_file(file_name: str) -> dict:
    """
    CSV-file parsing
    :param file_name: path to csv-file
    :return: dictionary with users with dictionaries {product: rating}
    """
    with open(file_name, "r", encoding='utf-8') as f:
        data = csv.reader(f)

        ratings = dict()

        for line in data:
            user = line[0]
            product = line[1]
            rate = float(line[2])
            if not user in ratings:
                ratings[user] = dict()

            ratings[user][product] = rate
    # print(ratings)
    return ratings


def distCosine(vector_one: dict, vector_two: dict) -> float:
    """
    Calculation of cosine similarity between two users
    :param vecA: dictionary of first user's ratings
    :param vecB: dictionary of second user's ratings
    :return: coefficient of cosine similarity
    """
    def dotProduct(vector_one, vector_two):
        d = 0.0
        for dim in vector_one:
            if dim in vector_two:
                d += vector_one[dim] * vector_two[dim]
        return d

    return dotProduct(vector_one, vector_two) / (math.sqrt(dotProduct(vector_one, vector_one)) * math.sqrt(dotProduct(vector_two, vector_two)))


def user_rating_comparison(current_user: str, file_name: str) -> list:
    """
    Comparsion between current user and other users
    :param current_user: user for comparsion
    :param file_name: path to the csv-file
    :return: list of cosine similarities between current user and other users
    """
    rating_dict = read_file(file_name)

    matching_factor_list = []
    for user in rating_dict:
        print(user, rating_dict[user])
        if user != current_user:
            matching_factor_list.append(distCosine(rating_dict[current_user], rating_dict[user]))
    print(f"matching_factor_list: {matching_factor_list}")
    matching_factor_list.append(sum(matching_factor_list))

    return matching_factor_list


def matrix_creating(current_user: str, file_name: str) -> list:
    """

    :param current_user:
    :param file_name:
    :return:
    """
    comparison = user_rating_comparison(current_user, file_name)
    rating_dict = read_file(file_name)
    matrix = []
    rating_dict.pop(current_user)
    for user, object in rating_dict.items():
        # index = list(rating_dict.keys()).index(user)
        matrix.append([0 for i in range(9)])
    for i in range(len(matrix)):
        print(matrix[i])
    rating_dict_1 = read_file(file_name)

    user_list = list(rating_dict.keys())
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if str(j + 1) in rating_dict_1[current_user].keys():
                matrix[i][j] = False
            elif str(j + 1) in rating_dict[user_list[i]].keys():
                matrix[i][j] = rating_dict[user_list[i]][f"{j + 1}"] * comparison[i]

    return matrix

def print_matrix(current_user: str, matrix: list, file_name: str) -> None:
    comparison = user_rating_comparison(current_user, file_name)
    rating_dict = read_file(file_name)
    rating_dict.pop(current_user)
    x = list(rating_dict.keys())
    for i in range(len(matrix)):
        print(f"{x[i]:<5}: {matrix[i]}")
    sum_ = [matrix[0][i] + matrix[1][i] + matrix[2][i] for i in range(len(matrix[i]))]
    result_ = [sum_[i] / sum(comparison[0:3]) for i in range(len(matrix[i]))]
    print(f"sum:   {sum_}")
    print(f"result:{result_}")
    return result_


def define_recommended_product(final_list):
    max_ = 0
    product_number = None
    for index, rating in enumerate(final_list):
        if rating > max_:
            max_ = rating
            product_number = index + 1

    print(f"We recommend you product {product_number} with rating {max_}")

if __name__ == '__main__':
    file_name = "C:\\Users\\Vladimir\\Python\\pythonProject\\recommendation_module\\venv\\data.csv"
    current_user = 'ivan'

    matrix = matrix_creating(current_user, file_name)
    for i in range(len(matrix)):
        print(matrix[i])

    final_list = print_matrix(current_user, matrix, file_name)

    define_recommended_product(final_list)



