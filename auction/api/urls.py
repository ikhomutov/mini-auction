from django.urls import path
from rest_framework.routers import SimpleRouter

from . import views

app_name = 'api'

router = SimpleRouter()
router.register(r'lots', views.LotViewSet)
router.register(r'bids', views.BidViewSet)

urlpatterns = [
    path('pets/', views.PetListView.as_view()),
] + router.urls
