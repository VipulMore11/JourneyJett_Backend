from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from .serializers import ReviewSerializer
from .models import Reviews
from Authentication.models import Profile  
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
            rating_avg = Reviews.objects.filter(place=place_id).aggregate(Avg('rating'))['rating__avg']
            place = Places.objects.get(id=place_id)
            place.rating = rating_avg if rating_avg is not None else 0
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
                user = request.user.id
                profile = Profile.objects.get(user=user)
                reviews = Reviews.objects.filter(user=profile)
                serializer = ReviewSerializer(reviews, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                reviews = Reviews.objects.filter(place=place_id)
                serializer = ReviewSerializer(reviews, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
        except Reviews.DoesNotExist:
            return Response({'message': 'Reviews not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
# from rest_framework.decorators import api_view, permission_classes
# from rest_framework.response import Response
# from rest_framework.permissions import AllowAny
# from django.http import JsonResponse
# import google.generativeai as genai

# @api_view(['POST'])
# @permission_classes([AllowAny])
# def chat_with_ai_api(request):
#     # Check if the request method is POST
#     if request.method == 'POST':
#         # Get the user input from the request data
#         user_input = request.data.get('user_input', '')
        
#         # Generate response using user input
#         response = get_travel_assistant_response(user_input)
        
#         # Return response
#         return JsonResponse(response)
    
#     # Return error response if method is not POST
#     return Response({'error': 'Method not allowed'}, status=405)


# def get_travel_assistant_response(user_input):
#     genai.configure(api_key="AIzaSyA4uR6gq5njTMtQXJwSpIdq_zC1LA1ugS0")  # Set up your API key

#     generation_config = {
#         "temperature": 0.9,
#         "top_p": 1,
#         "top_k": 1,
#         "max_output_tokens": 500,
#     }

#     safety_settings = [
#         {
#             "category": "HARM_CATEGORY_HARASSMENT",
#             "threshold": "BLOCK_MEDIUM_AND_ABOVE"
#         },
#         # Add other settings as needed
#     ]

#     model = genai.GenerativeModel(model_name="gemini-1.0-pro",
#                                   generation_config=generation_config,
#                                   safety_settings=safety_settings)

#     convo = model.start_chat(history=[])
#     context = "You are an AI travel assistant specializing in travel advice for India. Whether you're looking for destination recommendations, travel tips, or assistance with trip planning, I'm here to help you make the most of your travels in India."
#     message = f"{context} {user_input}"
#     response = convo.send_message(message)
    
#     text = response.text

#     data = {
#         "input": user_input,
#         "response": text
#     }

#     return data

