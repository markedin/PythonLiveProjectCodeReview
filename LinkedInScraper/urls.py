from django.urls import path
from . import views

urlpatterns = [
    # sets the url path to home page index.html
    path('', views.lis_home, name='lis_home'),
    path('create/', views.create_user, name='create'),
    path('listall/', views.list_users, name='listall'),
    path('bs4_practice/', views.bs4_practice, name='bs4_practice'),
    path('<int:pk>/details/', views.details, name='details'),
    path('<int:pk>/delete/', views.delete, name='delete'),
    path('ScraperAPI/', views.ScraperAPI, name='ScraperAPI'),
    path('favorites/', views.show_favoriteUsers, name='favorites'),

]