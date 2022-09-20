from django.shortcuts import render
from django.http import HttpResponse, HttpRequest, JsonResponse
from django.views import View
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response
import requests
import time
from CosineSimilarity import CosineSimilarity


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


def cycle_request(request):
    print("cycle-request запущен")
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
    # write_data_to_file_from_database()
    calculation = CosineSimilarity(username, get_request_to_database)
    recommended_product = calculation.define_recommended_product()
    print(recommended_product)
    return JsonResponse(recommended_product, safe=False)

def get_request_to_database():
    data_from_database = requests.get('http://localhost:9090/data_from_database')
    print(f"data from database: {data_from_database.text}")
    return data_from_database.text

def write_data_to_file_from_database():
    data_from_database = get_request_to_database()
    with open('file.txt', 'w', encoding='utf-8') as f:
        f.write(data_from_database)


#зацикленный запрос к базе, запускается в отдельном потоке
def loop_func():
    count = 0
    while True:
        get_request_to_database()
        time.sleep(5)
        count += 1
        if count == 100:
            print("Loop stopped")
            break

    # return Response(id, status=status.HTTP_200_OK)
    # return Response(render, id, status=status.HTTP_201_CREATED)

    # comment = Comment(todonote_id=data["todonote"], message=data["message"], author=request.user)
    # # comment.save(force_insert=True)
    # # return Response(serializers.serialize_comment_created(comment), status=status.HTTP_201_CREATED)
    # if comment.todonote.public:
    #     comment.save(force_insert=True)
    #     return Response(serializers.serialize_comment_created(comment), status=status.HTTP_201_CREATED)
    # else:
    #     return Response("Запись не публичная")

# serializer = serializers.NoteSerializer(data=request.data)
#
#        if not serializer.is_valid():
#            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#        serializer.save(author=request.user)
#        return Response(serializer.data, status=status.HTTP_201_CREATED)


# class IndexView(View):
#     def get(self, request: HttpRequest) -> HttpResponse:
#         params = {
#             "user": request.user,
#             "test_param": "this is test param"
#             # "server_version": settings_local.SERVER_VERSION,
#         }
#         return render(request, "recommendation_module/about.html", params)
