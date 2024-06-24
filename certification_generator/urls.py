from django.urls import path, include
from rest_framework.documentation import include_docs_urls
from rest_framework import routers
from .views import EmployeeView

router = routers.DefaultRouter()
router.register(r'certifications', EmployeeView, 'certifications')
urlpatterns = [
    path('api/', include(router.urls)),
    path('docs/', include_docs_urls(title='Certifications API')),
]