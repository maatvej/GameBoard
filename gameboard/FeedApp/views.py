from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.urls import reverse_lazy
from django.shortcuts import redirect, render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView
from .models import *
from .forms import PostForm, ReplyForm
from datetime import datetime
from .filters import PostFilter


class PostsList(ListView):
    model = Post
    ordering = '-postingDate'
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['next_post'] = None
        return context


class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        replies = Reply.objects.filter(post_id=self.kwargs['pk'])
        context['replies'] = replies
        return context


class MyPosts(LoginRequiredMixin, ListView):
    model = Post
    ordering = '-postingDate'
    template_name = 'my_posts.html'
    context_object_name = 'my_posts'
    paginate_by = 5

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user)


class RepliesList(ListView):
    model = Reply
    ordering = '-postingDate'
    template_name = 'replies_to_posts.html'
    context_object_name = 'replies'
    paginate_by = 3

    def get_queryset(self):
        user = self.request.user
        queryset = super().get_queryset().filter(post__author=user)
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['filterset'] = self.filterset
        return context


class ReplyDetail(DetailView):
    model = Reply
    template_name = 'reply.html'
    context_object_name = 'reply_id'

    def reply_detail_view(self, request, pk):
        try:
            reply_id = Reply.objects.get(pk=pk)
        except Reply.DoesNotExist:
            raise Http404("React does not exist!")

        return render(
            request, 'reply.html', context={'reply': reply_id, }
                  )


class PostCreate(LoginRequiredMixin, CreateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    success_url = reverse_lazy('post_list')

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            form = PostForm(request.POST, request.FILES)
            if form.is_valid():
                f = form.save(commit=False)
                f.author_id = self.request.user.id
                form.save()
                return redirect(f'/newsfeed/')
            else:
                return render(request, 'post_edit.html', {'form': form})
        else:
            form = PostForm()
            return render(request, 'post_edit.html', {'form': form})


class ReplyCreate(LoginRequiredMixin, CreateView):
    permission_required = ('FeedApp.add_reply',)
    form_class = ReplyForm
    model = Reply
    template_name = 'reply_edit.html'
    success_url = reverse_lazy('post_list')

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            form = ReplyForm(request.POST)
            post_pk = self.kwargs['pk']

            if form.is_valid():
                f = form.save(commit=False)
                f.author_id = self.request.user.id
                f.post = Post.objects.get(pk=post_pk)
                form.save()
                return redirect(f'/newsfeed/')
            else:
                return render(request, 'reply_edit.html', {'form': form})
        else:
            form = PostForm()
            return render(request, 'reply_edit.html', {'form': form})


def reply_accept(request, reply_id, post_id):
    reply = get_object_or_404(Reply, id=reply_id)
    reply.status = True
    reply.save()
    return redirect('post_detail', pk=post_id)
