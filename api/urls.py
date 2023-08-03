from api.views import UserView
from rest_framework import routers


app_urls = routers.DefaultRouter()

app_urls.register(r"user", viewset=UserView, basename="user")
