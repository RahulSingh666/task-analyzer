from django.urls import path, include
from .views import frontend
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', frontend, name='frontend'),
    path('api/tasks/', include('tasks.urls')),
] + static(settings.STATIC_URL, document_root=settings.BASE_DIR / '../frontend')
