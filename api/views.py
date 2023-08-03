from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from django.contrib import auth
from user.models import UserAccount
from api.serializers import UserSerializer
from .pagination import CustomPaginations


class UserView(mixins.CreateModelMixin,
                   mixins.UpdateModelMixin,
                   GenericViewSet):
    queryset = UserAccount.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, ]
    pagination_class = CustomPaginations

    @action(methods=["post"], detail=False, permission_classes=[AllowAny])
    def login(self, request):
        '''
          posted username and password
          if username and password authenticate
          :return jwt
        '''
        user = auth.authenticate(request, email=request.data["email"], password=request.data["password"])
        if user is not None:
            refresh = RefreshToken.for_user(user)
            raw_token = str(refresh.access_token)
            return Response({"token": str(raw_token)}, status=status.HTTP_200_OK)

        return Response({"message": "user was not found"}, status=status.HTTP_404_NOT_FOUND)

    @action(methods=["get"], detail=True, permission_classes=[IsAuthenticated])
    def profile(self, request):
        serializer = self.serializer_class(self.request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
