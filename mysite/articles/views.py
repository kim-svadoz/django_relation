from django.shortcuts import render, redirect, get_object_or_404
# DVDH -> django가 주는 views에서 쓸 decorations http를 위한 
from django.views.decorators.http import require_POST

from django.contrib.auth.decorators import login_required

from .models import Article, Comment
from .forms import ArticleForm, CommentForm
from IPython import embed

from django.contrib import messages
from django.http import JsonResponse

# Create your views here.

def index(request):
    articles = Article.objects.all()
    context = {
        'articles': articles
    }
    return render(request, 'articles/index.html', context)

def detail(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    # 1은 N을 보장할 수 없기 때문에 querySet(comment_set) 형태로 조회해야한다.
    comments = article.comment_set.all()
    comment_form = CommentForm()
    context = {
        'article': article,
        'comment_form': comment_form,
        'comments': comments,
    }
    return render(request, 'articles/detail.html', context)

@login_required
def create(request):
    if request.method == "POST":
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save(commit=False)
            article.user = request.user
            article.save()
            messages.success(request, '게시글 작성 완료')
            return redirect('articles:detail', article.pk)
        else:
            messages.error(request, ' 너 잘못된 데이터를 넣었어!! ')
    else:
        form = ArticleForm()
    context = {
        'form': form
    }
    return render(request, 'articles/form.html', context)

@login_required
def update(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    if article.user.username == request.user.username:
        if request.method == "POST":
            form = ArticleForm(request.POST, request.FILES, instance=article)
            if form.is_valid():
                article = form.save()
                return redirect('articles:detail', article.pk)
        else:
            form = ArticleForm(instance=article)
        context = {
            'form': form
        }
        return render(request, 'articles/form.html', context)

@require_POST
def delete(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    if article.user.username == request.user.username:
        article.delete()
        return redirect('articles:index')

@login_required
def comment_create(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.user = request.user
            #comment.article = article
            comment.article_id = article_pk
            comment.save()    
            return redirect('articles:detail', article.pk)
        else:
            context = {
                'comment_form': comment_form,
                'article': article,
            }
    return redirect('articles:detail', context)

@login_required
@require_POST
def comment_delete(request, article_pk, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)
    if comment.user.username == request.user.username:
        comment.delete()
        return redirect('articles:detail', article_pk)

@login_required
def like(request, article_pk):
    # 특정 게시물에 대한 정보
    article = get_object_or_404(Article, pk=article_pk)
    # 좋아요를 누른 유저에 대한 정보
    user = request.user
    # 사용자가 게시글의 좋아요 목록에 있으면 지우고 없으면 추가한다.
    if user in article.like_users.all():
        article.like_users.remove(user)
        liked = False
    else:
        article.like_users.add(user)
        liked = True
    context = {
        'liked' : liked,
        'count' : article.like_users.count()
    }
    return JsonResponse(context)

@login_required
def recommend(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    user = request.user
    if user in article.recommend_users.all():
        article.recommend_users.remove(user)
    else:
        article.recommend_users.add(user)
    return redirect('articles:index')