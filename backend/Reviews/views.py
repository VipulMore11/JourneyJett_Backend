from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from .serializers import ReviewSerializer
from .models import Reviews  
from Venues.models import Places
from django.db.models import Avg

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def review_view(request):
    try:
        user = request.user
        place_id = request.data.get('place_id')
        if not place_id:
            return Response({'error': 'Place ID is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        mutable_data = request.data.copy()
        mutable_data['place'] = place_id 
        mutable_data['user'] = user.id
        serializer = ReviewSerializer(data=mutable_data)
        if serializer.is_valid():
            serializer.save()
            place = Places.objects.get(id=place_id)
            place.rating = Reviews.objects.filter(place=place_id).aggregate(Avg('rating'), default=0)['rating__avg']
            place.save()
            return Response({'message': 'Review saved successfully'}, status=status.HTTP_201_CREATED) 
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        
@api_view(['GET'])
@permission_classes([AllowAny])
def get_reviews(request):
    if request.method == 'GET':
        try:
            place_id = request.GET.get('place_id')
            if not place_id:
                return Response({'error': 'Place ID is required'}, status=status.HTTP_400_BAD_REQUEST)
            
            reviews = Reviews.objects.filter(place=place_id)
            serializer = ReviewSerializer(reviews, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Reviews.DoesNotExist:
            return Response({'message': 'Reviews not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
