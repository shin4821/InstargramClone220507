# Generated by Django 4.0.3 on 2022-05-02 12:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0003_bookmark_like_reply'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='feed',
            name='like_count',
        ),
    ]
