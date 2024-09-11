from django.contrib import admin
from django.urls import path
from visibility.views import CustomVisibilityGraphQLView
from visibility.schema import schema
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('admin/', admin.site.urls),
    path(
        'graphql/', csrf_exempt(
            CustomVisibilityGraphQLView.as_view(graphiql=True, schema=schema)
        )
    ),
]
