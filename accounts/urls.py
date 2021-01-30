from . import views
from django.urls import path

urlpatterns = [
    path('',views.home,name="home"),
    path('product/',views.products,name="product"),
    path('customer/<str:pk_test>',views.customer,name="customer"),
    path('create_order/<str:pk>/',views.createOrder,name="create"),
    path('update_order/<str:pk>/',views.updateOrder,name="update"),
    path('delete_order/<str:pk>/',views.deleteOrder,name="delete"),

]
