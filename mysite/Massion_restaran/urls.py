from rest_framework import routers
from .views import RegisterView, CustomLoginView, LogoutView, UserProfileListView,\
    UserProfileDefaultView, RestaranListView, RestaranDefaultView, CategoryListView,\
    CategoryDefaultView, ProductListView, ProductDefaultView, BookATableListView,\
    BookATableDefaultView, CartAPIView, CartItemViewSet, FavoriteAPIView,\
    FavoriteItemViewSet
from django.urls import path, include

router = routers.DefaultRouter()

urlpatterns = [
    include('', include(router.urls)),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('userprofile/', UserProfileListView.as_view(), name='userprofile'),
    path('userprofile/<int:pk>/', UserProfileDefaultView.as_view(), name='userprofile_default'),
    path('restaran/', RestaranListView.as_view(), name='restaran'),
    path('restaran/<int:pk>/', RestaranDefaultView.as_view(), name='restaran_default'),
    path('category/', CategoryListView.as_view(), name='category'),
    path('category/<int:pk>/', CategoryDefaultView.as_view(), name='category_default'),
    path('product/', ProductListView.as_view(), name='product'),
    path('product/<int:pk>/', ProductDefaultView.as_view(), name='product_default'),
    path('book/', BookATableListView.as_view(), name='book'),
    path('book/<int:pk>/', BookATableDefaultView.as_view(), name='book_default'),
    path('cart/', CartAPIView.as_view(), name='cart'),
    path('cartitem/', CartItemViewSet.as_view(), name='cartitem'),
    path('favorite/', FavoriteAPIView.as_view(), name='favorite'),
    path('favoriteitem/', FavoriteItemViewSet.as_view(), name='favoriteitem'),
]