
from django.contrib import admin
from django.urls import path
from .views import EstimateCal, MonthlyCal, delete, user_login, user_logout, user_signup , delete_all_expenses


app_name = 'calculate'

urlpatterns = [

    # path('', index, name='base'),
    path('', user_login, name='login'),
    path('signup/', user_signup, name='signup'),
    path('logout/', user_logout, name='logout'),
    path('exp/',EstimateCal.as_view(),name = 'exp_post'),
    path('total/',MonthlyCal.as_view(),name='total_amount'),
    path('expenses/<int:id>/', delete, name='delete-expense'),
    path('clearall/',delete_all_expenses,name='delete-all')

]

