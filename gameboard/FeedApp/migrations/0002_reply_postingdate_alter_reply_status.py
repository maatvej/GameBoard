# Generated by Django 4.2.7 on 2023-11-15 12:30

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('FeedApp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='reply',
            name='postingDate',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='reply',
            name='status',
            field=models.BooleanField(default=None),
        ),
    ]
