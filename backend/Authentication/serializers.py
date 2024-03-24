from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from rest_framework.parsers import MultiPartParser, FormParser
from .models import User, Profile
from rest_framework import serializers    
from django.contrib.auth import authenticate
from rest_framework.exceptions import ValidationError
from django.contrib.auth import get_user_model

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

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'username', 'password', 'phone_no')

    def create(self, validated_data):
        email = validated_data.get('email')
        username = validated_data.get('username')
        password = validated_data.get('password')
        phone_no = validated_data.get('phone_no')
        if not email:
            raise ValueError(_('The Email must be set'))
        User = get_user_model()
        user = User(email=email, username=username, phone_no=phone_no)
        user.set_password(password)  # Set the password using set_password method
        user.is_active= True
        user.save()
        Profile.objects.create(user=user,email=email, username=username, phone_number=phone_no)
        return user

from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.contrib.auth import authenticate

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
        if email and password:
            user = authenticate(request=self.context.get('request'), email=email, password=password)
            if user is not None:
                if user.is_active:
                    return user
                else:
                    raise ValidationError("User account is not active.")
            else:
                raise ValidationError("Invalid credentials. Please try again.")
        raise ValidationError("Both email and password are required.")


class UserProfileSerialize(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'

class UpdateProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['username', 'phone_number', 'profile_image']