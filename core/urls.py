from django.urls import path
from core.views import index

app_name = 'core'

urlpattens = [
    path("bananas/", views.index)
]