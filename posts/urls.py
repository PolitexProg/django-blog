from django.urls import path
from .views import PostListView, PostListByTagView,PostDetailView, PostCreateView, pending_approval_view

app_name = 'post'

urlpatterns = [
    path('', PostListView.as_view(), name='list'),
    path('new/', PostCreateView.as_view(), name='create'),
    path('pending/', pending_approval_view, name='pending_approval'),
    path('<int:pk>/', PostDetailView.as_view(), name='detail'),
    path('tag/<slug:tag_slug>/', PostListByTagView.as_view(), name='list_by_tag')
]
