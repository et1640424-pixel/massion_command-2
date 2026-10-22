import serializers
from django.contrib.auth.models import AnonymousUser
from rest_framework import viewsets, generics, status, permissions, serializers
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .models import UserProfile, Restaran, Category, Product, book_a_table, Cart, CartItem, FavoriteItem, Favorite
from .serializers import RegisterSerializer, CustomLoginSerializer, LogoutSerializer,\
    UserProfileListSerializer, UserProfileDefaultSerializer, RestaranListSerializer,\
    RestaranDefaultSerializer, CategoryListSerializer, CategoryDefaultSerializer,\
    ProductListSerializer, ProductDetailSerializer, BookATableListSerializer,\
    BookATableDefaultSerializer, CartSerializer, CartItemSerializer,\
    FavoriteSerializer, FavoriteItemSerializer
from django_filters.rest_framework import DjangoFilterBackend
from .filter import ProductFilter
from rest_framework.filters import SearchFilter, OrderingFilter
from .pagination import ProductPagination

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class CustomLoginView(generics.GenericAPIView):
    serializer_class = CustomLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class LogoutView(generics.GenericAPIView):
    serializer_class = LogoutSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            refresh_token = serializer.validated_data['refresh']
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response({'detail': 'Невалидный токен'}, status=status.HTTP_400_BAD_REQUEST)

class UserProfileListView(generics.ListAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileListSerializer

class UserProfileDefaultView(generics.RetrieveAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileDefaultSerializer

class RestaranListView(generics.ListAPIView):
    queryset = Restaran.objects.all()
    serializer_class = RestaranListSerializer

class RestaranDefaultView(generics.RetrieveAPIView):
    queryset = Restaran.objects.all()
    serializer_class = RestaranDefaultSerializer

class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryListSerializer

class CategoryDefaultView(generics.RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryDefaultSerializer

class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ProductFilter
    search_fields = ['product_name']
    ordering_fields = ['price', 'create_date']
    pagination_class = ProductPagination

class ProductDefaultView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductDetailSerializer

class BookATableListView(generics.ListAPIView):
    queryset = book_a_table.objects.all()
    serializer_class = BookATableListSerializer

class BookATableDefaultView(generics.RetrieveAPIView):
    queryset = book_a_table.objects.all()
    serializer_class = BookATableDefaultSerializer

class CartAPIView(generics.RetrieveAPIView):
    serializer_class = CartSerializer

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)

    def retrieve(self, request, *args, **kwargs):
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        serializer = self.get_serializer(cart)
        return Response(serializer.data)

class CartItemViewSet(viewsets.ModelViewSet):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        if isinstance(self.request.user, AnonymousUser):
            return CartItem.objects.none()

        return CartItem.objects.filter(cart__user=self.request.user)

    def perform_create(self, serializer):
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        serializer.save(cart=cart)

class FavoriteAPIView(generics.RetrieveAPIView):
    serializer_class = FavoriteSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user)


    def retrieve(self, request, *args, **kwargs):
        favorite, created = Favorite.objects.get_or_create(user=self.request.user)
        serializer = self.get_serializer(favorite)
        return Response(serializer.data)


class FavoriteItemViewSet(viewsets.ModelViewSet):
    queryset = Favorite.objects.all()
    serializer_class =  FavoriteItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if isinstance(self.request.user, AnonymousUser):
            return FavoriteItem.objects.none()

        return FavoriteItem.objects.filter(favorite__user=self.request.user)


    def perform_create(self, serializer):
        favorite, created = Favorite.objects.get_or_create(user=self.request.user)
        product = serializer.validated_data['product']

        if FavoriteItem.objects.filter(favorite=favorite, product=product).exists():
            raise serializers.ValidationError('Товар кошулган')

        serializer.save(favorite=favorite)
