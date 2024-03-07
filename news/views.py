
from datetime import datetime, timedelta
from django.core.paginator import Paginator
from django.db.models import Q
from .forms import EmailPostForm, CommentForm, NewsForm
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from .models import News
from .forms import CommentForm
from django.contrib.auth.decorators import login_required


def news_list(request):
    news = News.objects.all()
    trend_10 = News.objects.filter(created_at__gte=datetime.now().date() - timedelta(days=10)).order_by('-view')
    paginator = Paginator(news, 3)
    page_number = request.GET.get('page',1)
    posts_pagination = paginator.get_page(page_number)
    end_date_month = datetime.now().date()
    start_date_month = end_date_month - timedelta(days=30)
    trend_month = News.objects.filter(created_at__gte=start_date_month, comments__created_at__lte=end_date_month).order_by('-view')
    return render(request, 'news/home.html', {
        'news':news,
        'trend_10':trend_10,
        'trend_month':trend_month,
        'posts_pagination':posts_pagination
    })


def news_detail(request, id):
    news = get_object_or_404(News, id=id, status=News.Status.PUBLISHED)
    viewed_news = set(request.session.get('viewed_news', []))
    if id not in viewed_news:
        # Если новость еще не просматривалась, увеличиваем счетчик просмотров и добавляем ID в множество
        news.increase_view()  # Это метод, который вы должны добавить в вашу модель News
        viewed_news.add(id)
        request.session['viewed_news'] = list(viewed_news)

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

