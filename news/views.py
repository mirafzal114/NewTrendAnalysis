from datetime import  timedelta
from django.utils import timezone

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from .forms import EmailPostForm, CommentForm, NewsForm
from news.models import News
from django.contrib import messages

# Create your views here.


def news_list(request):
    news = News.objects.all()
    paginator = Paginator(news, 3)
    page_number = request.GET.get('page',1)
    posts = paginator.get_page(page_number)
    return render(request, 'news/home.html', {'news':news})

def news_detail(request, id):
    news = get_object_or_404(News, id=id, status=News.Status.PUBLISHED)
    return render(request, 'news/news_detail.html', {'news_detail': news})

@login_required
def post_share(request, post_id):
    post = get_object_or_404(News,
                             id=post_id,
                             status=News.Status.PUBLISHED)

    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid() :
            cd = form.cleaned_data
    else:
        form = EmailPostForm()
    return render(request, 'news/share.html', {'post':post, 'form':form, })


from django.shortcuts import render, redirect, get_object_or_404
from .models import News
from .forms import CommentForm
from django.contrib.auth.decorators import login_required
@login_required
def post_comment(request, post_id):
    post = get_object_or_404(News, id=post_id, status=News.Status.PUBLISHED)
    comments = post.comments.all()

    if request.method == 'POST':
        form = CommentForm(data=request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('news_detail', id=post_id)  # Use 'id' instead of 'post_id'

    else:
        form = CommentForm()

    return render(request, 'news/news_detail.html', {'news_detail': post, 'form_comment': form, 'comments': comments})

@login_required
def create_news(request):
    if request.method == 'POST':
        form = NewsForm(request.POST)
        if form.is_valid():
            news = form.save(commit=False)
            news.author = request.user
            news.save()
            form.save_m2m()
            return redirect('news_list')
    else:
        form = NewsForm()
    return render(request, 'news/addnews.html', {'form': form})


@login_required
def delete_news(request, pk):
    news = News.objects.get(pk=pk)
    if request.user == news.author:
        news.delete()
        messages.success(request, 'News deleted successfully!')
        return redirect('news_list')
    else:
        return redirect('news_list')




def search_product(request):
    query = request.GET.get('q')
    if query:
        results = News.objects.filter(Q(body__icontains=query) | Q(title__icontains=query))
    else:
        results = []

    return render(request, 'base.html', {'results': results, 'query': query})


def get_recent_news():
    seven_days_ago = timezone.now() - timedelta(days=7)
    recent_news = News.objects.filter(publish__gte=seven_days_ago, status=News.Status.PUBLISHED)

    return recent_news

def recent_news_view(request):
    recent_news = get_recent_news()
    return render(request, 'news/home.html', {'recent_news': recent_news})
