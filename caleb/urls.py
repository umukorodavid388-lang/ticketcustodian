from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('ticket/', views.ticket_list, name='ticket'),
    path("get-account-details/", views.get_account_details, name="get_account_details"),
    path("checkout/<int:ticket_id>/", views.create_purchase_view, name="checkout"),  # ✅ FIXED
    path("seerbit/callback/<int:purchase_id>/", views.seerbit_callback, name="seerbit_callback"),
]