from django.urls import path

from .views import UserListView, UserCreateView, UserUpdateView, UserDeleteView

urlpatterns = [
    path('user/', UserListView.as_view(), name='user_list'),
    path('user/create/', UserCreateView.as_view(), name='create_user'),
    path('user/<int:pk>/update/', UserUpdateView.as_view(), name='update_user'),
    path('user/<int:pk>/delete/', UserDeleteView.as_view(), name='delete_user'),
]