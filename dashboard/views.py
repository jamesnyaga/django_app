# dashboard/views.py
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from blog.models import Posts
from dashboard.models import PostView
from django.db.models import Count

class DashboardHomeView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'dashboard/home.html'

    def test_func(self):
        return self.request.user.is_staff

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Basic stats
        context['total_posts'] = Posts.objects.count()
        context['total_views'] = PostView.objects.count()

        # Top 5 most viewed posts
        top_posts = Posts.objects.annotate(view_count=Count('postview')).order_by('-view_count')[:5]
        context['top_post_titles'] = [post.title for post in top_posts]
        context['top_post_views'] = [post.view_count for post in top_posts]

        # Posts per category
        categories = Posts.objects.values('category').annotate(num_posts=Count('id'))
        context['category_names'] = [cat['category'] for cat in categories]
        context['category_counts'] = [cat['num_posts'] for cat in categories]

        return context
