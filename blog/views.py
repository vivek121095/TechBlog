from django.shortcuts import render,get_object_or_404,redirect
from django.utils import timezone
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import (ListView,DetailView,CreateView,UpdateView,DeleteView)
from blog.models import Post, Comment ,Profile
from blog.forms import PostForm,CommentForm,UserForm,ProfileForm
from django.urls import reverse_lazy
from django.db import transaction
from django.contrib import messages
from django.http import HttpResponseRedirect

def PostListView(request):
    post_list = Post.objects.filter(published_date__lte = timezone.now()).order_by('-published_date')
    paginator = Paginator(post_list,5)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    return render(request, 'post_list.html', {'posts': posts})

class PostDetailView(DetailView):
    model = Post

class CreatePostView(LoginRequiredMixin,CreateView):
    login_url = '/login/'
    model = Post
    form_class = PostForm
    def form_valid(self,form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

class PostUpdateView(LoginRequiredMixin,UpdateView):
    login_url = '/login/'
    model = Post
    form_class = PostForm
    def form_valid(self,form):
        self.object = form.save(commit=False)
        self.object.published_date = None
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

class PostDeleteView(LoginRequiredMixin,DeleteView):
    model = Post
    success_url = reverse_lazy('post_list')

class DraftListView(LoginRequiredMixin,ListView):
    login_url = '/login/'
    redirect_field_name = 'blog/post_list.html'
    model = Post

    def get_queryset(self):
        return Post.objects.filter(published_date__isnull=True,author=self.request.user).order_by('create_date')

#################################################################
################################################################
@login_required
def post_publish(request,pk):
    post = get_object_or_404(Post,pk=pk)
    post.publish()
    return redirect('post_detail',pk=post.pk)

@login_required
def add_comment_to_post(request,pk):
    post = get_object_or_404(Post,pk=pk)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit = False)
            comment.post = post
            comment.author = request.user.username
            comment.save()
            return redirect('post_detail',pk=post.pk)
    else:
        form = CommentForm()
        return render(request,'blog/comment_form.html',{'form':form})

@login_required
def comment_approve(request,pk):
    comment = get_object_or_404(Comment,pk=pk)
    comment.approve()
    return redirect('post_detail',pk=comment.post.pk)

@login_required
def comment_remove(request,pk):
    comment = get_object_or_404(Comment,pk=pk)
    post_pk = comment.post.pk
    comment.delete()
    return redirect('post_detail',pk=post_pk)

@login_required
def home(request):
    return render(request,'blog/index.html')

@login_required
@transaction.atomic
def update_profile(request):
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "'Your profile was successfully updated!'")
            return redirect('profile',user_id=request.user.id)
        else:
            messages.error(request,"Please correct the error below.'")
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, 'profiles/profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })

@login_required
def profile(request,user_id):
    profile = get_object_or_404(Profile,user_id=user_id)
    return render(request,'profiles/profileview.html',{'profile':profile.user})
