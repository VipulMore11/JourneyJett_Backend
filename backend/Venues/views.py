from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from django.http import JsonResponse
from .serializers import *
from .models import Places, PlacesImage, UserVisits
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from django.db.models import Count, Q

@api_view(['POST'])
@permission_classes([AllowAny])
def places_view(request):
    if request.method == 'POST':
        serializer = PlaceSerializer(data=request.data)
        if serializer.is_valid():
            place = serializer.save()

            # Handle place images
            place_images_data = request.FILES.getlist('places_image', [])
            for place_image_data in place_images_data:
                PlacesImage.objects.create(place=place, places_image=place_image_data)

            return Response(serializer.data, status=status.HTTP_201_CREATED)    
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_places_view(request):
    if request.method == 'GET':
        place_id = request.GET.get('id')
        getfilter = request.query_params.get('filter')
        user = request.user
        
        try:
            if user.is_authenticated:
                if place_id:
                    venue = Places.objects.get(id=place_id)
                    UserVisits.objects.create(user=user, place=venue)

            if place_id:
                place = Places.objects.get(id=place_id)
                serializer = PlaceSerializer(place)
                return Response(serializer.data, status=status.HTTP_200_OK)
            
            elif getfilter:
                getfilter = getfilter.split(',')
                if getfilter == 'empty':
                    filters = Places.objects.filter.all()
                elif getfilter == 'trending':
                    trending_places = UserVisits.objects.values('place').annotate(visit_count=Count('place')).order_by('-visit_count')[:10]
                    trending_place_ids = [place['place'] for place in trending_places]
                    trending_places_data = Places.objects.filter(id__in=trending_place_ids)
                    serializer = PlaceSerializer(trending_places_data, many=True)
                else: 
                    filters = Places.objects.filter(category__in=getfilter)
                    serializer = PlaceSerializer(filters, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                places = Places.objects.all().order_by('-id')
                serializer = PlaceSerializer(places, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
        except Places.DoesNotExist:
            return Response({'error': 'Place not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_destination_view(request):
    if request.method == 'GET':
        state = request.GET.get('state')
        try:
            if state:
                    destinations = Places.objects.filter(Q(city__icontains=state) | Q(state__icontains=state) | Q(name__icontains=state) | Q(info__icontains=state))
                    serializer = DestinationSerializer(destinations, many=True)
                    return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                destinations = Places.objects.all()
                serializer = DestinationSerializer(destinations, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
        except Places.DoesNotExist:
            return Response( {'Error':'Destination does not exist'} , status=status.HTTP_404_NOT_FOUND )  
        except Exception as e:
            return Response( { 'Error':str(e)} , status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def personalize_recommendations(request):
    user_id = request.user.id

    user_visits = UserVisits.objects.filter(user_id=user_id).values_list('place_id', flat=True)
    print(user_visits)
    visited_places = Places.objects.filter(id__in=user_visits)
    # print(visited_places)
    feature_texts = [' '.join([str(place.id), place.info, place.best_time, place.city, place.state]) for place in visited_places]
    # print(feature_texts)
    vectorizer = TfidfVectorizer()
    feature_vectors = vectorizer.fit_transform(feature_texts)

    all_places_in_india = Places.objects.all()
    all_feature_texts = [' '.join([str(place.id), place.info, place.best_time, place.city, place.state]) for place in all_places_in_india]
    all_feature_vectors = vectorizer.transform(all_feature_texts)
    similarity_matrix = cosine_similarity(feature_vectors, all_feature_vectors)
    # print(similarity_matrix)
    N = 5  
    personalized_recommendations = set()  # Use a set to store unique recommendations
    for i in range(len(visited_places)):
        similar_places_indices = similarity_matrix[i].argsort()[::-1][1:N+1]
        for index in similar_places_indices:
            index = int(index)
            similar_place = all_places_in_india[index]
            # print(all_places_in_india[index])
            # print(similar_place)
            place_id = similar_place.id
            # print(place_id)
            if place_id != visited_places[i].id:
                personalized_recommendations.add(place_id)

    recommendations_list = list(personalized_recommendations)  # Convert set to list
    recommendations_list = [str(place_id) for place_id in recommendations_list]  # Convert place IDs to strings
    # print(recommendations_list)
    return JsonResponse({'recommendations': recommendations_list})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def saved_places(request):
    try:
        user = request.user
        place_id = request.data.get('id')  # Retrieve place_id from request data
        serializer = SavedPlaceSerializer(data={'user': user.id, 'place': place_id})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)    
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'Error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_saved_places(request):
    try:
        user = request.user.id
        saved = SavedPlaces.objects.filter(user=user)
        serializers = SavedPlaceSerializer(saved, many=True)
        return Response(serializers.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'Error': str(e)}, status=status.HTTP_400_BAD_REQUEST)