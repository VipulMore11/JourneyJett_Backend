from rest_framework import serializers
from .models import *
from Reviews.serializers import ReviewSerializer


class Base64ImageField(serializers.ImageField):
    """
    A Django REST framework field for handling image-uploads through raw post data.
    It uses base64 for encoding and decoding the contents of the file.

    Heavily based on
    https://github.com/tomchristie/django-rest-framework/pull/1268

    Updated for Django REST framework 3.
    """

    def to_internal_value(self, data):
        from django.core.files.base import ContentFile
        import base64
        import six
        import uuid

        # Check if this is a base64 string
        if isinstance(data, six.string_types):
            # Check if the base64 string is in the "data:" format
            if 'data:' in data and ';base64,' in data:
                # Break out the header from the base64 content
                header, data = data.split(';base64,')

            # Try to decode the file. Return validation error if it fails.
            try:
                decoded_file = base64.b64decode(data)
            except TypeError:
                self.fail('invalid_image')

            # Generate file name:
            file_name = str(uuid.uuid4())[:12] # 12 characters are more than enough.
            # Get the file name extension:
            file_extension = self.get_file_extension(file_name, decoded_file)

            complete_file_name = "%s.%s" % (file_name, file_extension, )

            data = ContentFile(decoded_file, name=complete_file_name)

        return super(Base64ImageField, self).to_internal_value(data)

    def get_file_extension(self, file_name, decoded_file):
        import imghdr

        extension = imghdr.what(file_name, decoded_file)
        extension = "jpg" if extension == "jpeg" else extension

        return extension

class PlacesImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlacesImage
        fields = ['id', 'places_image']


class FestivalSerializer(serializers.ModelSerializer):

    class Meta:
        model = Festivals
        fields = '__all__'


class PlaceSerializer(serializers.ModelSerializer):
    images = PlacesImageSerializer(many=True, read_only = True)
    festivals = FestivalSerializer(many=True, read_only = True)
    reviews = ReviewSerializer(many=True, read_only = True)

    class Meta:
        model = Places
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        cast_images = representation.get('images', [])
        
        # Assign custom IDs starting from 1 for each event's cast images
        for index, cast_image in enumerate(cast_images, start=1):
            cast_image['id'] = index

        location_str = representation.get('location', '')
        if location_str:
            # Clean up the string value
            location_str = location_str.replace('[', '').replace(']', '').replace('"', '')  # Remove brackets and quotation marks
            # Split the cleaned location string by comma and convert each coordinate to float
            location_list = [float(coord.strip()) for coord in location_str.split(',') if coord.strip()]
        else:
            # If location is None, set it as an empty list
            location_list = []

        # Update the representation with the location list
        representation['location'] = location_list

        return representation
    
class DestinationSerializer(serializers.ModelSerializer):
    images = PlacesImageSerializer(many=True, read_only = True)
    festivals = FestivalSerializer(many=True, read_only = True)
    reviews = ReviewSerializer(many=True, read_only = True)
    class Meta:
        model = Places
        fields = '__all__'

class SavedPlaceSerializer(serializers.ModelSerializer):
    class Meta:
        depth = 1
        model = SavedPlaces
        fields = ['id','user', 'place']