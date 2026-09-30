from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST
from django.views.generic import (
    CreateView, DeleteView, DetailView, ListView, UpdateView,
)

from .forms import CommentForm, PostForm, PostImageFormSet
from .models import Comment, Post
from .permissions import AuthorRequiredMixin, PostOwnerMixin, is_author


# ---------- Public views ----------

class PostListView(ListView):
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    paginate_by = 6

    def get_queryset(self):
        qs = (
            Post.objects.filter(status='published')
            .select_related('author')
            .annotate(
                like_count=Count('likes', distinct=True),
                comment_count=Count(
                    'comments', filter=Q(comments__active=True), distinct=True
                ),
            )
        )
        q = self.request.GET.get('q', '').strip()
        if q:
            qs = qs.filter(Q(title__icontains=q) | Q(content__icontains=q))
        return qs


class PostDetailView(DetailView):
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'

    def get_queryset(self):
        qs = Post.objects.select_related('author').prefetch_related('images')
        user = self.request.user
        if user.is_superuser:
            return qs
        if user.is_authenticated:
            # Published posts, plus the user's own drafts
            return qs.filter(Q(status='published') | Q(author=user))
        return qs.filter(status='published')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        post, user = self.object, self.request.user
        ctx['comments'] = post.comments.filter(active=True).select_related('user')
        ctx['comment_form'] = CommentForm()
        ctx['like_count'] = post.likes.count()
        ctx['liked'] = user.is_authenticated and post.likes.filter(pk=user.pk).exists()
        ctx['can_manage'] = is_author(user) and (
            post.author_id == user.pk or user.is_superuser
        )
        return ctx


class SignUpView(CreateView):
    """Public signup for viewers/students. Never grants author rights."""
    form_class = UserCreationForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        messages.success(self.request, 'Welcome! Your account has been created.')
        return redirect(self.success_url)


# ---------- Viewer actions (login required) ----------

@login_required
@require_POST
def like_post(request, slug):
    post = get_object_or_404(Post, slug=slug, status='published')
    if post.likes.filter(pk=request.user.pk).exists():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    return redirect(post.get_absolute_url())


@login_required
@require_POST
def add_comment(request, slug):
    post = get_object_or_404(Post, slug=slug, status='published')
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.user = request.user
        comment.save()
        messages.success(request, 'Comment added.')
    else:
        messages.error(request, 'Your comment could not be posted.')
    return redirect(f'{post.get_absolute_url()}#comments')


@login_required
@require_POST
def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    user = request.user
    if user == comment.user or user == comment.post.author or user.is_superuser:
        comment.delete()
        messages.success(request, 'Comment deleted.')
    else:
        messages.error(request, 'You cannot delete that comment.')
    return redirect(f'{comment.post.get_absolute_url()}#comments')


# ---------- Author-only views ----------

class MyPostsView(AuthorRequiredMixin, ListView):
    template_name = 'blog/my_posts.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user)


class PostFormsetMixin:
    success_message = 'Article saved.'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        if 'image_formset' not in ctx:
            if self.request.method == 'POST':
                ctx['image_formset'] = PostImageFormSet(
                    self.request.POST, self.request.FILES, instance=self.object
                )
            else:
                ctx['image_formset'] = PostImageFormSet(instance=self.object)
        return ctx

    def form_valid(self, form):
        formset = PostImageFormSet(
            self.request.POST, self.request.FILES, instance=self.object
        )
        if not formset.is_valid():
            # Show the page again with the photo errors
            return self.render_to_response(
                self.get_context_data(form=form, image_formset=formset)
            )
        response = super().form_valid(form)   # saves the article
        formset.instance = self.object        # link the photos to the saved article
        formset.save()
        messages.success(self.request, self.success_message)
        return response


class PostCreateView(PostFormsetMixin, AuthorRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    success_message = 'Article saved.'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['heading'] = 'Write a New Article'
        return ctx


class PostUpdateView(PostFormsetMixin, PostOwnerMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    success_message = 'Article updated.'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['heading'] = 'Edit Article'
        return ctx


class PostDeleteView(PostOwnerMixin, DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        messages.success(self.request, 'Article deleted.')
        return super().form_valid(form)