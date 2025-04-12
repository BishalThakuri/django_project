from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('', views.home, name='home'),
    path('add/', views.add_items, name='add_items'),
    path('delete/<int:id>/', views.delete_item, name='delete_item'),
    path('register/', views.register_page, name='register'),
    path('edit/<int:id>/', views.edit_item, name='edit_item'),
]
