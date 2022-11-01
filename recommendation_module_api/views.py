from django.http import HttpResponse, JsonResponse
import requests
import time
from src.cosine_similarity import CosineSimilarity


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


def test_request(request):
    print("test-request запущен")
    # while True:
    result = requests.get('http://localhost:9090/purchase-data')
    print(f"result.text: {result.text}")
    print("после выполнения запроса")
    print(f"result: {result}")
    # products = [product for product in response]

    return JsonResponse(result.text, safe=False)
    # time.sleep(3)


def get_request_from_front(request, username):
    # data = request.data
    print(f"username: {username}")
    calculation = CosineSimilarity(username, request_to_database)
    recommended_product = calculation.define_recommended_product()
    print(recommended_product)
    return JsonResponse(recommended_product, safe=False)

def request_to_database():
    data_from_database = requests.get('http://localhost:9090/data_from_database')
    print(f"data from database: {data_from_database.text}")
    return data_from_database.text


def loop_func() -> None:
    """
    Зацикленный запрос к базе, запускается в отдельном потоке
    :return: None
    """
    count = 0
    while True:
        request_to_database()
        time.sleep(5)
        count += 1
        if count == 100:
            print("Loop stopped")
            break
