from rest_framework import serializers
from .models import UserProfile, Restaran, Category, Product, book_a_table, Cart, CartItem, FavoriteItem, Favorite
from rest_framework_simplejwt.tokens import RefreshToken

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('email', 'username', 'password', 'phone_number', 'age')
        extra_kwargs = {'password': {'write_only': True}}

    def validate_email(self, value):
        if UserProfile.objects.filter(email=value).exists():
            raise serializers.ValidationError("Пользователь с таким email уже существует")
        return value

    def create(self, validated_data):
        password = validated_data.pop('password')
        email = validated_data.pop('email')
        username = validated_data.pop('username')
        user = UserProfile(email=email, username=username, **validated_data)
        user.set_password(password)
        user.save()
        return user

class CustomLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        try:
            user = UserProfile.objects.get(email=email)
        except UserProfile.DoesNotExist:
            raise serializers.ValidationError({"email": "Пользователь с таким email не найден"})

        if not user.check_password(password):
            raise serializers.ValidationError({"password": "Неверный пароль"})



        self.context['user'] = user
        return data

    def to_representation(self, instance):
        user = self.context['user']
        refresh = RefreshToken.for_user(user)

        return {
            'user': {
                'username': user.username,
                'email': user.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def validate(self, attrs):
        token = attrs.get('refresh')
        try:
            RefreshToken(token)
        except Exception:
            raise serializers.ValidationError({"refresh": "Невалидный токен"})
        return attrs

#------users
class UserProfileListSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'

class UserProfileDefaultSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'


#-------restaurant--------
class RestaranListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaran
        fields = '__all__'

class RestaranDefaultSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaran
        fields = '__all__'

#-------category---------
class CategoryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class CategoryDefaultSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


# ---------product--------
class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class ProductDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

#------book a table-------
class BookATableListSerializer(serializers.ModelSerializer):
    class Meta:
        model = book_a_table
        fields = '__all__'

class BookATableDefaultSerializer(serializers.ModelSerializer):
    class Meta:
        model = book_a_table
        fields = '__all__'


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductListSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(),
                                                    write_only=True, source='product')
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'product_id', 'quantity', 'total_price']

    def get_total_price(self, obj):
        return obj.get_total_price()


class CartSerializer(serializers.ModelSerializer):
    item = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['id', 'user', 'item', 'total_price']

    def get_total_price(self, obj):
        return obj.get_total_price()


class FavoriteItemSerializer(serializers.ModelSerializer):
    product = ProductListSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(),
                                                    write_only=True, source='product')
    class Meta:
        model = FavoriteItem
        fields = ['id', 'product', 'product_id']

class FavoriteSerializer(serializers.ModelSerializer):
    favorite_item = FavoriteItemSerializer(read_only=True, many=True)
    class Meta:
        model = Favorite
        fields = ['id', 'user', 'favorite_item']
