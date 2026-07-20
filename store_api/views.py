from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.authtoken.models import Token
from .models import User, Category, Product, ProductView, Order, Chat
from .serializers import (
    UserSerializer, RegisterSerializer, LoginSerializer,
    CategorySerializer, ProductSerializer, OrderSerializer, ChatSerializer
)

# Authentication Views
@api_view(['POST'])
def register_user(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            "id": user.id,
            "username": user.username,
            "name": user.first_name,
            "token": token.key
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login_user(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            "id": user.id,
            "username": user.username,
            "name": user.first_name,
            "token": token.key
        }, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def create_checkout(request):
    import json
    import urllib.request
    
    # In production, replace with your actual Yoco Secret Key from environment variables
    YOCO_SECRET_KEY = "sk_test_45bc50000eD08xge47f4626a3b47"
    
    amount = request.data.get('amount', 4900)
    currency = request.data.get('currency', 'ZAR')
    success_url = request.data.get('successUrl')
    cancel_url = request.data.get('cancelUrl')
    
    payload = {
        "amount": amount,
        "currency": currency,
        "successUrl": success_url,
        "cancelUrl": cancel_url
    }
    
    req = urllib.request.Request('https://payments.yoco.com/api/checkouts')
    req.add_header('Content-Type', 'application/json')
    req.add_header('Authorization', f'Bearer {YOCO_SECRET_KEY}')
    req.add_header('User-Agent', 'Mozilla/5.0')
    
    try:
        response = urllib.request.urlopen(req, json.dumps(payload).encode('utf-8'))
        response_data = json.loads(response.read().decode('utf-8'))
        return Response({"redirectUrl": response_data.get('redirectUrl')})
    except urllib.error.HTTPError as e:
        error_data = e.read().decode('utf-8')
        try:
            parsed = json.loads(error_data)
            return Response({"error": "Yoco Payment API Error", "details": parsed}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({"error": "Yoco Payment Error", "details": error_data}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# User ViewSet
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]
    
    def update(self, request, *args, **kwargs):
        user = self.get_object()
        if request.user.id != user.id and not request.user.is_staff:
            return Response({"error": "Forbidden"}, status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        user = self.get_object()
        if request.user.id != user.id and not request.user.is_staff:
            return Response({"error": "Forbidden"}, status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)

# Category ViewSet
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAdminUser()]
        return [permissions.AllowAny()]

# Product ViewSet
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all().order_by('-createdAt')
    serializer_class = ProductSerializer

    def get_queryset(self):
        user = self.request.user
        if user and user.is_staff:
            return Product.objects.all().order_by('-createdAt')
        # If authenticated, user sees approved + their own pending/rejected
        if user and user.is_authenticated:
            from django.db.models import Q
            return Product.objects.filter(Q(status='approved') | Q(seller=user)).order_by('-createdAt')
        return Product.objects.filter(status='approved').order_by('-createdAt')

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    def perform_create(self, serializer):
        serializer.save(seller=self.request.user)

    def update(self, request, *args, **kwargs):
        product = self.get_object()
        if request.user.id != product.seller.id and not request.user.is_staff:
            return Response({"error": "Forbidden"}, status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        product = self.get_object()
        if request.user.id != product.seller.id and not request.user.is_staff:
            return Response({"error": "Forbidden"}, status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAdminUser])
    def approve(self, request, pk=None):
        product = self.get_object()
        product.status = 'approved'
        product.save()
        return Response({"status": "approved"})

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAdminUser])
    def reject(self, request, pk=None):
        product = self.get_object()
        product.status = 'rejected'
        product.save()
        return Response({"status": "rejected"})

    @action(detail=False, methods=['post'], permission_classes=[permissions.AllowAny])
    def upload(self, request):
        import cloudinary
        import cloudinary.uploader
        
        # Configure Cloudinary (in production, use environment variables)
        cloudinary.config( 
          cloud_name = "finttein", 
          api_key = "837699919773594", 
          api_secret = "vqU32ikakYbmhKTCTVSlrgENyTM" 
        )
        
        main_images = request.FILES.getlist('main_images')
        extra_images = request.FILES.getlist('extra_images')
        
        uploaded_main = []
        for f in main_images:
            try:
                upload_result = cloudinary.uploader.upload(f)
                # Generate optimized URL using f_auto,q_auto
                optimized_url, _ = cloudinary.utils.cloudinary_url(
                    upload_result.get('public_id'),
                    fetch_format="auto",
                    quality="auto",
                    secure=True
                )
                uploaded_main.append(optimized_url)
            except Exception as e:
                return Response({'error': str(e)}, status=400)
            
        uploaded_extra = []
        for f in extra_images:
            try:
                upload_result = cloudinary.uploader.upload(f)
                optimized_url, _ = cloudinary.utils.cloudinary_url(
                    upload_result.get('public_id'),
                    fetch_format="auto",
                    quality="auto",
                    secure=True
                )
                uploaded_extra.append(optimized_url)
            except Exception as e:
                return Response({'error': str(e)}, status=400)
            
        return Response({
            'main_images': uploaded_main,
            'extra_images': uploaded_extra
        })

    @action(detail=True, methods=['post'], permission_classes=[permissions.AllowAny])
    def view(self, request, pk=None):
        product = self.get_object()
        from django.utils import timezone
        ProductView.objects.create(
            product=product,
            dateString=timezone.now().strftime('%Y-%m-%d')
        )
        return Response({"success": True})

# Order ViewSet
class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_permissions(self):
        if self.action in ['create']:
            return [permissions.IsAuthenticated()]
        if self.action in ['update', 'partial_update', 'destroy']:
            return [permissions.IsAdminUser()]
        return [permissions.AllowAny()]

# Chat ViewSet
class ChatViewSet(viewsets.ModelViewSet):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer

    def get_permissions(self):
        return [permissions.IsAuthenticated()]
