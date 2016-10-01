__author__ = 'msorescu'

from django.conf.urls import url, include
from bliss import views
from rest_framework.routers import DefaultRouter

# Create a router and register our viewsets with it.
router = DefaultRouter()

# router.register(r'api/v1/callback',views.SubmissionResultViewSet)

# The API URLs are now determined automatically by the router.
# Additionally, we include the login URLs for the browseable API.
urlpatterns = [
    url(r'^api/v1/imageUpload/', views.FileUploadView.as_view()),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
