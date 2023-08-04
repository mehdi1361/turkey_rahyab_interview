from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from django.contrib import auth
from user.models import UserAccount
from post.models import Announcement
from api.serializers import UserSerializer, AnnouncementSerializer
from .pagination import CustomPaginations
from django_filters.rest_framework import DjangoFilterBackend


class UserView(mixins.CreateModelMixin,
                   mixins.UpdateModelMixin,
                   viewsets.GenericViewSet):
    queryset = UserAccount.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny, ]
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

    @action(methods=["get"], detail=False, permission_classes=[IsAuthenticated])
    def profile(self, request):
        serializer = self.serializer_class(self.request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

class AnnouncementView(
                   mixins.ListModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.DestroyModelMixin,
                   mixins.UpdateModelMixin,
                   viewsets.GenericViewSet
):
    queryset = Announcement.objects.all()
    serializer_class = AnnouncementSerializer
    permission_classes = [IsAuthenticated, ]
    pagination_class = CustomPaginations
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['title', 'content']

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        else:
            return super().get_permissions()

    def retrieve(self, request, pk=None):
        announcement = Announcement.objects.filter(pk=pk).first()
        announcement.views_count += 1
        announcement.save()
        serializer = self.serializer_class(announcement)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        picture = request.FILES.get("picture")
        announcement = Announcement.objects.create(
            title=request.data["title"],
            content=request.data["title"],
            owner=request.user,
            picture=picture
        )
        serializer = self.serializer_class(announcement)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(methods=["post"], detail=True, permission_classes=[IsAuthenticated])
    def accept(self, request,pk=None):
        announcement = Announcement.objects.filter(pk=pk).first()
        announcement.accept = True
        announcement.save()
        serializer = self.serializer_class(announcement)

        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=["get"], detail=False, permission_classes=[IsAuthenticated])
    def my_announcement(self, request,pk=None):
        announcements = Announcement.objects.filter(owner=request.user)
        serializer = self.serializer_class(announcements, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
