from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('start/', views.test_request, name='test_request'),
    path('api/recommend_data/<str:username>/', views.get_request_from_front),
    # path('about/', views.IndexView.as_view()),
]