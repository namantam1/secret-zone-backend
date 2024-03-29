# Generated by Django 3.1.3 on 2020-11-23 17:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('chat', '0003_auto_20201123_2227'),
    ]

    operations = [
        migrations.CreateModel(
            name='Friends',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('blocked', models.ManyToManyField(blank=True, related_name='user_blocked', to=settings.AUTH_USER_MODEL)),
                ('friends', models.ManyToManyField(blank=True, related_name='user_friends', to=settings.AUTH_USER_MODEL)),
                ('requested', models.ManyToManyField(blank=True, related_name='user_requested', to=settings.AUTH_USER_MODEL)),
                ('requests', models.ManyToManyField(blank=True, related_name='user_requests', to=settings.AUTH_USER_MODEL)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
