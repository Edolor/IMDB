from django.contrib.auth.models import User
from rest_framework import serializers

class RegistrationSerializer(serializers.ModelSerializer):
    """
    Handles the user creation process
    """
    password2 = serializers.CharField(style={"input_type": "password"}, write_only=True) # Cannot read write only password

    class Meta:
        model = User
        fields = ["username", "email", "password", "password2"]
        extra_kwargs = {
            "password": {"write_only": True}
        }

    def save(self):
        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        # Check if passwords match
        if password != password2:
            raise serializers.ValidationError({"error": "p1 and p2 must be same"})
        
        # Check if user email exists
        if User.objects.filter(email=self.validated_data["email"]).exists():
            raise serializers.ValidationError({"error": "Email already exists."})

        
        # Create account manually
        account = User(email=self.validated_data["email"], username=self.validated_data["username"])
        account.set_password(password)
        account.save()

        return account
