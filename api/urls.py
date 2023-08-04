from api.views import UserView, AnnouncementView
from rest_framework import routers


app_urls = routers.DefaultRouter()

app_urls.register(r"user", viewset=UserView, basename="user")
app_urls.register(r"announcement", viewset=AnnouncementView, basename="announcement")
