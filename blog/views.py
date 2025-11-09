"""#new version
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import BlogPosts, Comment
from parents.models import Parent
from .forms import CommentForm
from teachers.models import Teacher
# Create your views here.
def Post_list(request):
    posts = BlogPosts.objects.all().order_by('-date_posted')
    context = {
        'posts':posts
    }
    return render(request, 'blog/blog_posts.html',context)
def get_profile_pic(self):
    if hasattr(self, 'parent'):
        return self.parent.profile.image.url
    elif hasattr(self, 'teacher'):
        return self.teacher.profile.image.url
    else:
        return self.profile.image.url if hasattr(self, 'profile')else 'media/parents_default_image.jpg'
User.add_to_class('get_profile_pic',get_profile_pic)

def PostDetails(request, id):
    post = get_object_or_404(BlogPosts, id=id)
    comments = post.comments.all().order_by('-created_at')

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.post = post
            new_comment.user = request.user
            new_comment.save()
            messages.success(request, 'comment added successifully!')
            return redirect('blog-detail', id=post.id)
    else:
        form = CommentForm()

    context = {
        'post': post,
        'comments': comments,
        'form': form,
    }
    return render(request, 'blog/blog_detail.html', context)

@login_required
def add_comment(request, id):
    post = get_object_or_404(BlogPosts, id=id)
    body = request.POST.get('body')

    if body:
        comment = Comment.objects.create(post=post, user=request.user, body=body)
        return JsonResponse({
            'user': comment.user.username,
            'body': comment.body,
            'created_at_time': comment.created_at.strftime('%I:%M %p'),
            'created_at_date': comment.created_at.strftime('%b %d, %Y'),
            'total_comments': post.comments.count(),
            'comment_id': comment.id,
            'profile_pic': comment.user.profile.get_profile_pic()
        })
    return JsonResponse({'error': 'Empty comment'}, status=400)

@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if comment.user == request.user or request.user.is_superuser:
        post_id = comment.post.id
        comment.delete()
        messages.success(request, "Comment deleted successfully!")
        return redirect('blog-detail', id=post_id)
    else:
        messages.error(request, "You’re not authorized to delete this comment.")
    return redirect('blog-detail', id=comment.post.id)


"""

#old version
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import Posts, Comment
from .forms import CommentForm
from dashboard.models import PostView

def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'blog/home.html', context)


class PostListView(ListView):
    model = Posts
    template_name = 'blog/home.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5


class userPostListView(ListView):
    model = Posts
    template_name = 'blog/user_posts.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Posts.objects.filter(author=user).order_by('-date_posted')


class PostDetailView(DetailView):
    model = Posts

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        context['comments'] = post.comments.all().order_by('-created_at')
        context['form'] = CommentForm()
        context['meta_description'] = post.meta_description if post.meta_description else post.content[:150]
        # Track view
        ip = self.request.META.get('REMOTE_ADDR')
        if ip:  # optional: avoid empty IP
            PostView.objects.get_or_create(post=post, ip_address=ip)
        return context

    def get_object(self, queryset=None):
        return Posts.objects.get(slug=self.kwargs['slug'])




class PostCreateView(LoginRequiredMixin, CreateView):
    model = Posts
    fields = ['title', 'content', 'image','category']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Posts
    fields = ['title', 'content', 'image']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Posts
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False
def category_posts(request, category_name):
    posts = Posts.objects.filter(category=category_name).order_by('-date_posted')
    seo_data = {
    'football': {
        'title': "Rolling Football — Latest Scores, Analysis & News from Kenya",
        'description': "Stay updated with football news, live scores, and in-depth match analysis from Kenya and beyond. Rolling Football brings you every goal, every story, every match that matters.",
        'keywords': "Football Kenya, Rolling Football, KPL, Premier League, Sports Kenya, Football News, Rolling, Voices That Matter",
        },
    'education': {
        'title': "Rolling Education — Student Life, Career Tips & Academic News in Kenya",
        'description': "Explore student life, university updates, and educational opportunities in Kenya. Rolling Education empowers learners through knowledge and stories that inspire.",
        'keywords': "Education Kenya, Students, Universities, Career Tips, Rolling Education, Learning, Academic News, Rolling Blog",
        },
    'entertainment': {
        'title': "Rolling Entertainment — Trending Stories, Celebrities & Lifestyle in Kenya",
        'description': "Get the latest entertainment updates, celebrity news, and lifestyle stories from Kenya. Rolling Entertainment keeps you connected to the trends and voices that matter.",
        'keywords': "Entertainment Kenya, Celebrities, Rolling Entertainment, Gossip, Kenyan Lifestyle, Music, Movies, Rolling Blog",
        },
    'news': {
        'title': "Rolling News — Breaking News & Stories That Matter in Kenya",
        'description': "Breaking news, politics, and community stories from across Kenya — told with truth and purpose. Rolling News brings you the voices that shape our nation.",
        'keywords': "Kenya News, Breaking News, Politics Kenya, Rolling News, Voices That Matter, Kenyan Stories, Current Affairs",
        },
    'voices': {
        'title': "Rolling Voices — Opinions, Features & Stories That Matter",
        'description': "Read powerful opinions and inspiring stories written by young voices across Kenya. Rolling Voices is where perspective meets purpose.",
        'keywords': "Opinions, Rolling Voices, Kenya Features, Inspiring Stories, Youth Blog, Rolling Media",
        },
    }

    # Default SEO data if category not found
    seo = seo_data.get(category_name.lower(), {
        'title': "Rolling — Voices That Matter | News, Football, Education & Entertainment in Kenya",
        'description': "Rolling is a youth-driven digital platform sharing real stories, news, football updates, and educational insights from across Kenya — crafted with care by James Muchiri and the Rolling Team.",
        'keywords': "Rolling, Kenya News, Football, Education, Entertainment, Blog, Voices That Matter, James Muchiri, Youth Media",
    })

    context = {
        'posts': posts,
        'category': category_name,
        'seo_title': seo['title'],
        'seo_description': seo['description'],
        'seo_keywords': seo['keywords'],
    }

    return render(request, 'blog/category_posts.html', context)

@login_required
def add_comment(request, pk):
    post = get_object_or_404(Posts, pk=pk)
    form = CommentForm(request.POST)

    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.user = request.user
        comment.save()
        messages.success(request, 'Comment added successfully!')
    else:
        messages.error(request, 'Failed to add comment.')

    return redirect('post-detail', pk=pk)


@login_required
def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if comment.user == request.user or request.user.is_superuser:
        post_id = comment.post.id
        comment.delete()
        messages.success(request, 'Comment deleted successfully!')
        return redirect('post-detail', pk=post_id)
    else:
        messages.error(request, "You're not authorized to delete this comment.")
        return redirect('post-detail', pk=comment.post.pk)


def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})

