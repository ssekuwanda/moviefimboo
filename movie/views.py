from .models import Movie, Serie, Episode, Site, Season, Downloaded
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from django.views.generic import DetailView, View
import requests
from PIL import Image
from accounts.models import Profile, Amount
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Count
from taggit.models import Tag
from django.contrib.auth import get_user_model

user = get_user_model()

movie_amount = Amount.objects.all()[0]
movie_price = movie_amount.movie_amount

serie_amount = Amount.objects.all()[0]
serie_price = serie_amount.serie_amount

def average_color(img):
    width, height = img.size
    
    r_total = 0
    g_total = 0 
    b_total = 0
    
    count = 0
    for x in range(0, width):
        for y in range(0, height):
            r, g, b = img.getpixel((x,y))
            r_total += r
            g_total += g
            b_total += b
            count += 1
            
    return(r_total/count, g_total/count, b_total/count)

class DownloadedToggle(View):
    def post(self, request, *args, **kwargs):
        movie_to_toggle = request.POST.get("movie")
        movie = Movie.objects.get(name__iexact=movie_to_toggle)
        print(user.objects.all())
        return redirect('/')

def movie_list(request):
    movies = Movie.objects.all().order_by('-timestamp')[:30]
    series = Serie.objects.all().order_by('-timestamp')[:30]
    site = Site.objects.all()

    context = {'movies':movies,
                'series':series,
                'site':site,
                }
    return render(request, 'home.html', context)

def movies(request, tag_slug=None):
    movies = Movie.objects.all().order_by('-timestamp')
    tag = Movie.tags.all()
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        movies = movies.filter(tags__in=[tag])

    paginator = Paginator(movies, 60)
    page = request.GET.get('page')
    try:
        pages = paginator.page(page)
    except PageNotAnInteger:
        pages = paginator.page(1)
    except EmptyPage:
        pages = paginator.page(paginator.num_pages)

    query = request.GET.get('q')
    if query:
        movies = Movie.objects.filter(name__icontains=query)

    context = {'movies':movies,
                'page':pages,
                'tag':tag,
                }
    return render(request, 'movies.html', context)

from django.conf import settings
import os
from wsgiref.util import FileWrapper
from mimetypes import guess_type

@login_required(login_url='/accounts/login/')
def download(request, slug):
    movie = Movie.objects.filter(slug=slug)

    movie_obj = movie.first()
    filepath = movie_obj.file.path
    file_root = settings.PROTECTED_ROOT
    final_filepath = os.path.join(file_root, filepath)
    
    with open(final_filepath, 'rb') as f:
        wrapper = FileWrapper(f)
        mimetype = 'application/force-download'
        guessed_mimetype = guess_type(filepath)[0]
        mime = guessed_mimetype.split("/")[1]
        if guessed_mimetype:
            mimetype = guessed_mimetype
        response = HttpResponse(wrapper, content_type=mimetype)
        response['Content-Disposition'] = f"attachment;filename={movie_obj}(moviefibs.com).{mime}"
        response["X-SendFile"] = str(movie_obj.name)
        current_user = request.user
        current_amount = current_user.profile.acc_amount
        if int(current_amount) >= movie_price:
            remove_amount = int(current_amount) - movie_price
            user = Profile.objects.filter(user=current_user).update(acc_amount=remove_amount)
            return response
        else:
            return redirect('/accounts/makepayment/?next=%s' % request.path)

@login_required(login_url='/accounts/login/')
def download_series(request, slug, season_id, episode_id):
    series = get_object_or_404(Serie, slug__iexact=slug)
    seasons = Season.objects.filter(series__in=[series])
    season = Season.objects.get(id=season_id)
    episodes = Episode.objects.filter(season__in=[season])

    episode_obj = Episode.objects.get(id=episode_id)
    filepath = episode_obj.video_file.path
    file_root = settings.PROTECTED_ROOT
    final_filepath = os.path.join(file_root, filepath)
    
    with open(final_filepath, 'rb') as f:
        wrapper = FileWrapper(f)
        mimetype = 'application/force-download'
        guessed_mimetype = guess_type(filepath)[0]
        mime = guessed_mimetype.split("/")[1]
        if guessed_mimetype:
            mimetype = guessed_mimetype
        response = HttpResponse(wrapper, content_type=mimetype)
        response['Content-Disposition'] = f"attachment;filename={episode_obj}(moviefibs.com).{mime}"
        response["X-SendFile"] = str(episode_obj)
        current_user = request.user
        current_amount = current_user.profile.acc_amount
        if int(current_amount) >= serie_price:
            remove_amount = int(current_amount) - serie_price
            user = Profile.objects.filter(user=current_user).update(acc_amount=remove_amount)
            return response
        else:
            return redirect('/accounts/makepayment/?next=%s' % request.path)

def series(request, tag_slug=None):
    series = Serie.objects.all().order_by('-timestamp')
    tag = Serie.tags.all()
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        series = series.filter(tags__in=[tag])

    paginator = Paginator(series, 60)
    page = request.GET.get('page')
    try:
        pages = paginator.page(page)
    except PageNotAnInteger:
        pages = paginator.page(1)
    except EmptyPage:
        pages = paginator.page(paginator.num_pages)

    query = request.GET.get('q')
    if query:
        series = Serie.objects.filter(name__icontains=query)

    context = {'series':series,
                'page':pages,
                'tag':tag,
                }
    return render(request, 'series.html', context)

@login_required(login_url='/accounts/login/')
def movie_detail(request, slug):
    movies = get_object_or_404(Movie, slug__iexact=slug)
    current_user = request.user
    current_amount = current_user.profile.acc_amount
    num_visits = request.session.get('num_visits',0)
    request.session['num_visits'] = num_visits + 1
    if movies.cover_image:
        img = Image.open(movies.cover_image)
        bg_color = average_color(img)

    movie_tags_ids = movies.tags.all()
    similar_movies = Movie.objects.filter(tags__in=movie_tags_ids).exclude(slug=slug)
    similar_movies = similar_movies.annotate(same_tags=Count('tags'))\
                                .order_by('-same_tags','-timestamp')[:3]

    template_name = 'movie_detail.html'
    context = {'movies':movies, 'bg_color':bg_color, 'similar_movies':similar_movies, 'num_visits':num_visits, 'movie_price':movie_price}

    if int(current_amount) >= movie_price:
        return render(request, template_name, context)
    else:
        return redirect('/accounts/makepayment/?next=%s' % request.path)

@login_required(login_url='/accounts/login/')
def series_detail(request, slug):
    series = get_object_or_404(Serie, slug__iexact=slug)
    seasons = Season.objects.filter(series__in=[series])
    current_user = request.user
    current_amount = current_user.profile.acc_amount
    if series.cover_image:
        img = Image.open(series.cover_image)
        bg_color = average_color(img)

    serie_tags_ids = series.tags.all()
    similar_series = Serie.objects.filter(tags__in=serie_tags_ids).exclude(slug=slug)
    similar_series = similar_series.annotate(same_tags=Count('tags'))\
                                .order_by('-same_tags','-timestamp')[:3]
    template_name = 'serie_detail.html'

    context = {'series':series,
                'seasons':seasons,
                'bg_color':bg_color,
                'similar_series':similar_series,
                'serie_price':serie_price,                
                 }

    if int(current_amount) >= serie_price:
        return render(request, template_name, context)
    else:
        return redirect('/accounts/makepayment/?next=%s' % request.path)

@login_required(login_url='/accounts/login/')
def season_detail(request, slug, season_slug):
    series = get_object_or_404(Serie, slug__iexact=slug)
    seasons = Season.objects.filter(series__in=[series])
    season = Season.objects.get(slug=season_slug)
    episode = Episode.objects.filter(season__in=[season])
    if series.cover_image:
        img = Image.open(series.cover_image)
        bg_color = average_color(img)
    template_name = 'serie_detail.html'
    return render(request, 'season_detail.html', {'series':series,'season':season,'seasons':seasons, 'episode':episode, 'bg_color':bg_color, 'serie_price':serie_price})