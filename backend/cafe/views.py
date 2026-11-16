
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import ComputerType, Computer, Pricing, Service
from .serializers import (
    ComputerTypeSerializer,
    ComputerSerializer,
    PricingSerializer,
    ServiceSerializer,
)


@api_view(['GET'])
def home(request):
    return Response({
        "app": "CyberCafe Manager",
        "status": "success",
        "message": "Internet Cafe API ажиллаж байна!"
    })


@api_view(['GET'])
def computer_types(request):
    data = ComputerType.objects.all()
    return Response(
        ComputerTypeSerializer(data, many=True).data
    )


@api_view(['GET'])
def computers(request):
    data = Computer.objects.select_related(
        'computer_type'
    ).all()

    name = request.query_params.get('name')
    computer_type = request.query_params.get('type')
    status = request.query_params.get('status')

    if name:
        data = data.filter(name__icontains=name)

    if computer_type:
        data = data.filter(
            computer_type__name__icontains=computer_type
        )

    if status:
        data = data.filter(status=status)

    return Response(
        ComputerSerializer(data, many=True).data
    )


@api_view(['GET'])
def pricings(request):
    data = Pricing.objects.all()
    return Response(
        PricingSerializer(data, many=True).data
    )


@api_view(['GET'])
def services(request):
    data = Service.objects.all()

    name = request.query_params.get('name')
    category = request.query_params.get('category')
    min_price = request.query_params.get('min_price')
    max_price = request.query_params.get('max_price')

    if name:
        data = data.filter(name__icontains=name)

    if category:
        data = data.filter(category__icontains=category)

    try:
        if min_price:
            data = data.filter(price__gte=min_price)
        if max_price:
            data = data.filter(price__lte=max_price)
    except (ValueError, TypeError):
        return Response(
            {"error": "Үнийн утга буруу байна"},
            status=400
        )

    return Response(
        ServiceSerializer(data, many=True).data
    )

from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import permission_classes
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegisterSerializer


@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    serializer = RegisterSerializer(data=request.data)

    if serializer.is_valid():
        user = serializer.save()

        refresh = RefreshToken.for_user(user)

        return Response({
            "message": "Амжилттай бүртгэгдлээ",
            "username": user.username,
            "role": "user",
            "access": str(refresh.access_token),
            "refresh": str(refresh),
        }, status=status.HTTP_201_CREATED)

    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST
    )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_profile(request):
    user = request.user

    return Response({
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "role": "admin" if user.is_staff else "user",
    })
