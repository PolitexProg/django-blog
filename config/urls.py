from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from posts.views import PostListView

urlpatterns = [
    path('', PostListView.as_view(), name="home_page"),
    path('admin/', admin.site.urls),
    path('users/', include('users.urls'), name='users'),
    path('post/', include('posts.urls'), name='post')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)