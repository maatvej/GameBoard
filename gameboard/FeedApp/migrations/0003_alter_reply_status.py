# Generated by Django 4.2.7 on 2023-11-15 13:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FeedApp', '0002_reply_postingdate_alter_reply_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reply',
            name='status',
            field=models.BooleanField(default=False),
        ),
    ]
