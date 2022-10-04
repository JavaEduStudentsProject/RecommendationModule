from django.apps import AppConfig
from threading import Thread

from . import views


class RecommendationModuleApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'recommendation_module_api'
    verbose_name = "Recommendations"

#todo раскомментировать. Асинхронные зацикленные запросы к оркестратору и базе (получение постоянного обновления какой-то информации)
    # def ready(self):
    #     th = Thread(target=views.loop_func, args=())
    #     th.start()