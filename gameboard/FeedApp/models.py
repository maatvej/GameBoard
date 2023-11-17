from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Post(models.Model):

    ROLES = [
        ('Tanks', 'Танки'),
        ('Healers', 'Хилы'),
        ('DamageDealers', 'ДД'),
        ('Traders', 'Торговцы'),
        ('GuildMasters', 'Гилдмастеры'),
        ('QuestGivers', 'Квестгиверы'),
        ('Forgers', 'Кузнецы'),
        ('Tanners', 'Кожевники'),
        ('Alchemics', 'Зельевары'),
        ('SpellMasters', 'Мастера заклинаний')
    ]

    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               db_column='author')
    title = models.CharField(max_length=64)
    body = models.TextField()
    category = models.CharField(max_length=64, choices=ROLES)
    postingDate = models.DateTimeField(auto_now_add=True)
    upload = models.FileField(null=True, blank=True, upload_to='uploads/')

    def __str__(self):
        return f'{self.author}: {self.title}'

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])


class Reply(models.Model):
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               db_column='author')
    body = models.TextField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE, default=None)
    status = models.BooleanField(default=False)
    postingDate = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'Reaction by {} on {}'.format(self.author, self.post)

    def get_absolute_url(self):
        return reverse('reply', args=[str(self.id)])


