"""
User's serializers
"""

from django.contrib.auth import authenticate, get_user_model
from django.utils.translation import gettext as translate
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    """Serializers for user"""

    class Meta:
        model = get_user_model()
        fields = ["email", "password", "first_name", "last_name"]
        extra_kwargs = {"password": {"write_only": True, "min_length": 5}}

    def create(self, validated_data):
        """Create and return new user with encrpyted password"""
        return get_user_model().objects.create_user(**validated_data)
    
    def update(self, instance, validated_data):
        """Update User details"""
        # Check if user passed in new password if not set to None # noqa
        password = validated_data.pop("password",None)
        # Update user instance with new details
        user = super().update(instance, validated_data)
        
        if password: 
            user.set_password(password)
            user.save()
            
        return user


class AuthTokenSerializer(serializers.Serializer):
    """Token Serializer for user login token"""
    email = serializers.EmailField()
    password = serializers.CharField(
        style={"input_type": "password"},
        trim_whitespace=False,
    )

    def validate(self, attrs):
        """Validate and authenticate User"""
        # Get email and password provided by the user
        email = attrs.get("email")
        password = attrs.get("password")
        # Use Django authenication function to check username and password # noqa
        user = authenticate(
            request=self.context.get("request"),
            username=email,
            password=password,
        )
        # Raise error if authentication function returns no user
        if not user:
            msg = translate(
                "Unable to authenticate with the provided credentials"
            )
            raise serializers.ValidationError(msg, code="authorization")

        attrs["user"] = user
        return attrs
