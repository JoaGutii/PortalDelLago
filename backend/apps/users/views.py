from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.conf import settings
from .serializers import RegisterSerializer, LoginSerializer, UserSerializer

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def login_view(request):
    serializer = LoginSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.validated_data['user']
    refresh = RefreshToken.for_user(user)
    return Response({
        'access': str(refresh.access_token),
        'refresh': str(refresh),
        'user': UserSerializer(user).data
    })

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def password_reset_request(request):
    email = request.data.get('email')
    if not email:
        return Response({'detail':'Email requerido'}, status=400)
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response({'detail':'Si el email existe, enviaremos un enlace'}, status=200)

    token = default_token_generator.make_token(user)
    reset_link = f"{request.build_absolute_uri('/')}reset-password?uid={user.pk}&token={token}"
    send_mail(
        'Recuperación de contraseña',
        f'Usa este enlace para restablecer tu contraseña: {reset_link}',
        settings.DEFAULT_FROM_EMAIL,
        [email],
        fail_silently=True
    )
    return Response({'detail':'Si el email existe, enviaremos un enlace'}, status=200)
