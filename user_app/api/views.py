from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token
from .serializers import RegistrationSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated

@api_view(["POST"])
def registration_view(request):
    """
    Handle User creation process
    """
    if request.method == "POST":
        serializer = RegistrationSerializer(data=request.data)
        
        data = {}

        if serializer.is_valid():
            account = serializer.save()

            data["response"] = "Registration successful."
            data["username"] = account.username
            data["email"] = account.email

            token = Token.objects.get(user=account) # Fetch token

            data["token"] = token.key

            return Response(data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def logout_view(request):
    if request.method == "POST":
        request.user.auth_token.delete()
        return Response({"message": "Logout successful!"}, status=status.HTTP_200_OK)