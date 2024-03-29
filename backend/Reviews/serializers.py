from rest_framework import serializers
from .models import Reviews

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reviews
        fields = '__all__'

class GetReviewSerializer(serializers.ModelSerializer):
    class Meta:
        depth = 1
        model = Reviews
        fields = '__all__'
