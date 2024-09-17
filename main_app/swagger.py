from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from dotenv import load_dotenv
import os
load_dotenv()


swagger_url = os.environ.get('SWAGGER_URL', 'http://localhost:8001')


schema_view = get_schema_view(
    openapi.Info(
        title="Your API Title",
        default_version='v1',
        description="API documentation",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@example.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
    url=swagger_url
)
