from django.urls import path
from . import views

urlpatterns = [
    path('', views.travels),
    path('add', views.add),
    path('add_plan', views.add),
    path('destination/<travel_id>', views.destination),
    path('add_travel/<travel_id>', views.join_travel)
]
