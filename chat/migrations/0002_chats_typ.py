# Generated by Django 3.1.3 on 2020-11-23 16:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='chats',
            name='typ',
            field=models.CharField(choices=[('txt', 'text'), ('img', 'image'), ('file', 'file')], default='txt', max_length=25),
        ),
    ]
