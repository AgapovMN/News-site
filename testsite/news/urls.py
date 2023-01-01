from django.urls import path
from news.views import *


urlpatterns = [
    path('mail/', user_send_mail, name='send_mail'),
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('category/<int:category_id>/', GetCategory.as_view(), name = 'category'),
    path('news/<int:pk>', ViewNews.as_view(), name='view_news'),
    path('news/add-news/', CreateNews.as_view(), name='add-news'),
    path('search/', Search.as_view(), name = 'search')
]

    