from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.db.models import Count 
from taggit.models import Tag # pyright: ignore[reportMissingImports]

from .models import Post, Category, Comment
from .forms import PostCreateForm, CommentForm
from datetime import timedelta
from django.utils import timezone


class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        queryset = Post.objects.filter(is_approved=True)
        sort_by = self.request.GET.get('sort', 'newest')
        
        
        if sort_by == 'newest':
            return queryset.order_by('-created_at')
        if sort_by in ['popular_week', 'popular_month', 'recommended']:
            queryset = queryset.annotate(comment_count=Count('comments', distinct=True))

        if sort_by == 'views_all':
            return queryset.order_by('-views_count')
        
        elif sort_by == 'popular_week':
            time_limit = timezone.now() - timedelta(days=7)
            return queryset.filter(created_at__gte=time_limit).order_by('-comment_count', '-created_at')
        
        elif sort_by == 'popular_month':
            time_limit = timezone.now() - timedelta(days=30)
            return queryset.filter(created_at__gte=time_limit).order_by('-comment_count', '-created_at')
        
        elif sort_by == 'recommended':
            time_limit = timezone.now() - timedelta(days=180)
            return queryset.filter(
                created_at__gte=time_limit,
                views_count__gte=50
            ).order_by('-comment_count', '-views_count', '-created_at')

        return queryset.order_by('-created_at')

class PostListByTagView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        tag_slug = self.kwargs.get('tag_slug')
        queryset = Post.objects.filter(is_approved=True, tags__slug=tag_slug).order_by('-created_at')
        try:
            self.tag = Tag.objects.get(slug=tag_slug)
        except Tag.DoesNotExist:
            self.tag = None
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.tag:
            context['title'] = f"Посты по тегу: #{self.tag.name}"
        else:
            context['title'] = "Посты (Тег не найден)"
        return context


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'

    def get_queryset(self):
        return Post.objects.filter(is_approved=True)

    def get(self, request, *args, **kwargs):
        post = self.get_object()
        post.views_count += 1
        post.save()
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        return context

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('users:login'))
        post = self.get_object()
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            return HttpResponseRedirect(reverse('post:detail', kwargs={'pk': post.pk}))
        context = self.get_context_data()
        context['comment_form'] = form
        return self.render_to_response(context)


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'blog/post_create.html'
    form_class = PostCreateForm
    success_url = reverse_lazy('post:pending_approval')

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.is_approved = False
        return super().form_valid(form)


def pending_approval_view(request):
    return render(request, 'blog/pending_approval.html')