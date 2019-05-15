from django.db import models
from django.db.models.signals import pre_save, post_save
from .utils import unique_slug_generator
from django.db.models import Q
from taggit.managers import TaggableManager
from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL

SEASON_CHOICES = (
    ('S01','Season 1'),
    ('S02','Season 2'),
    ('S03','Season 3'),
    ('S04','Season 4'),
    ('S05','Season 5'),
    ('S06','Season 6'),
)

EPISODE_CHOICES = (
    ('E01','Episode 1'),
    ('E02','Episode 2'),
    ('E03','Episode 3'),
    ('E04','Episode 4'),
    ('E05','Episode 5'),
    ('E06','Episode 6'),
    ('E07','Episode 7'),
    ('E08','Episode 8'),
    ('E09','Episode 9'),
    ('E10','Episode 10'),
    ('E11','Episode 11'),
    ('E12','Episode 12'),
    ('E13','Episode 13'),
    ('E14','Episode 14'),
    ('E15','Episode 15'),
)



class Site(models.Model):
    name = models.CharField(max_length=122,null=True, blank=True)
    font = models.TextField(null=True, blank=True)
    text_color = models.CharField(max_length=122,null=True, blank=True)
    back_ground_image1 = models.ImageField(upload_to='./media/bg_image',null=True, blank=True)
    back_ground_image2 = models.ImageField(upload_to='./media/bg_image',null=True, blank=True)

    app = models.FileField(upload_to="./media/app",null=True, blank=True)
    movie_cost = models.IntegerField(null=True, blank=True)
    episode_cost = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.name

class Genre(models.Model):
    name = models.CharField(max_length=122)

    def __str__(self):
        return self.name

class Movie(models.Model):
    name = models.CharField(max_length=122)
    cover_image = models.ImageField(upload_to='./media')
    tags = TaggableManager()
    genre = models.ManyToManyField(Genre, related_name='moviegenre', blank=True)
    timestamp = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)
    slug = models.SlugField(null=True, blank=True)
    translated = models.BooleanField(default=False)
    file = models.FileField(upload_to='Movies', blank=True, null=True)
    story_line = models.CharField(max_length=600, blank=True, null=True)

    def __str__(self):
        if self.name:
            titled = self.name
            x=titled.title()
            no_space=x.replace(' ','' )
            return '#'+no_space

    def get_download_url(self):
        qs = self.file.url()
        return qs

    @property
    def title(self):
        return self.name

def movie_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(movie_pre_save_receiver, sender=Movie)


class Serie(models.Model):
    name = models.CharField(max_length=122, null=True, blank=True)
    cover_image = models.FileField()
    timestamp = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)
    tags = TaggableManager()
    genre = models.ManyToManyField(Genre, related_name='seriegenre', blank=True)
    slug = models.SlugField(null=True, blank=True)
    translated = models.BooleanField(default=False)
    story_line = models.CharField(max_length=222, null=True, blank=True)

    def __str__(self):
        if self.name:
            titled = self.name
            x=titled.title()
            no_space=x.replace(' ','' )
            return '#'+no_space

    @property
    def title(self):
        return self.name

def rl_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(rl_pre_save_receiver, sender=Serie)


class Season(models.Model):
    seasoname = models.CharField(max_length=122, choices=SEASON_CHOICES, null=True, blank=True)
    slug = models.SlugField(null=True, blank=True)
    series = models.ForeignKey(Serie, on_delete=models.CASCADE, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return str(self.series) + '-' + self.seasoname 

    @property
    def title(self):
        return str(self.series)+'-'+self.seasoname

def rl_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = random_string_generator()

pre_save.connect(rl_pre_save_receiver, sender=Season)


class Episode(models.Model):
    episodenumber = models.CharField(max_length=112, choices=EPISODE_CHOICES, null=True, blank=True)
    video_file = models.FileField(upload_to='Series', null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)
    season = models.ForeignKey(Season, on_delete=models.CASCADE)
    story  = models.CharField(max_length=122, null=True, blank=True)

    class Meta:
        ordering = ['season','episodenumber']
        verbose_name_plural = "Episodes"

    def __str__(self):
        return str(self.season) +self.episodenumber


class Downloaded(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    movie = models.ManyToManyField(Movie, related_name='my_movies', blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username

def post_save_user_receiver(sender, instance, created, *args, **kwargs):
    if created:
        downloaded, is_created = Downloaded.objects.get_or_create(user=instance)

post_save.connect(post_save_user_receiver, sender=User)