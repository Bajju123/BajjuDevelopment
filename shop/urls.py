from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    path('', views.product_list, name="product_list"),
    path('department', views.department, name="department"),
    path('<str:category_slug>', views.product_list, name="product_list_by_category"),
    path('<int:id>/<str:slug>', views.product_detail, name="product_detail"),
    path('register/', views.register, name="register"),
    path('login/', views.login, name="login"),
    path('logout/', views.logout, name="logout"),
    path('about/', views.about, name="AboutUs"),
    path('contact/', views.contact, name="ContactUs"),
    path('search/', views.search, name="Search"),
    path('CheckOrder/', views.check_order, name="CheckOrder"),
    path('CancleOrder/', views.cancle_order, name="CancleOrder"),
    path('OrderDetail/', views.order_detail, name="OrderDetail"),

]