from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer,LoginSerializer,UserProfileSerialize, UpdateProfileSerializer
from .models import User,Profile
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from django.views.decorators.csrf import csrf_exempt


@api_view(['POST'])
@permission_classes([AllowAny])
# @authentication_classes([SessionAuthentication, BasicAuthentication])
def signup_view(request):
    if request.method == 'POST':
        reg_serializer = UserSerializer(data=request.data)
        if reg_serializer.is_valid():
            new_user = reg_serializer.save()
            refresh = RefreshToken.for_user(new_user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_200_OK)
        return Response(reg_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response({'message': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['POST'])
@csrf_exempt
@permission_classes([AllowAny])
# @authentication_classes([SessionAuthentication])
def login_view(request):
    if request.method == 'POST':
        mutable_data = request.data.copy()
        email = mutable_data.get('email')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'error': 'User with this email does not exist.'}, status=status.HTTP_404_NOT_FOUND)

        mutable_data['username'] = user.username
        serializer = LoginSerializer(data=mutable_data, context={'request': request})

        if serializer.is_valid():
            user = serializer.validated_data
            refresh = RefreshToken.for_user(user)
            response = {
                'refresh': str(refresh),
                'access': str(refresh.access_token)
            }
            return Response(response, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response({'message': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['POST'])
@permission_classes([AllowAny])
def logout_view(request):
    try:
        refresh_token = request.data.get("refresh_token")
        token = RefreshToken(refresh_token)
        token.blacklist()
        return Response({'message': 'Logged out successfully'})
    except Exception as e:
        return Response(status=status.HTTP_200_OK)
    
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile_view(request):
        try :
            user_id=request.user.id
            userprofile = Profile.objects.get(user_id=user_id)
            serializer = UserProfileSerialize(userprofile)
            return Response(serializer.data,status=status.HTTP_200_OK)
        except Profile.DoesNotExist :
            return Response('No Profile Found', status=status.HTTP_404_NOT_FOUND)
        except Exception as e :
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
   
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_profile_view(request):
        try :
            user_id=request.user.id
            data = request.data.copy()
            data['user']=user_id
            userprofile_instance = Profile.objects.get(user_id=user_id)
            serializer = UpdateProfileSerializer(instance=userprofile_instance, data=data)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'Profile updated successfully'},status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Profile.DoesNotExist :
            return Response('No Profile Found', status=status.HTTP_404_NOT_FOUND)
        except Exception as e :
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)