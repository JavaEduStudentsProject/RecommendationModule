"""
WSGI config for RecommendationModule project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/wsgi/
"""

import os
import asyncio

from django.core.wsgi import get_wsgi_application

from async_kafka.views import main, consume_orders_data, consume_request_for_user

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'recommendation_module.settings')

application = get_wsgi_application()
print("Server runs")

asyncio.run(main())
