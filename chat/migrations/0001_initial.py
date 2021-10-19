# Generated by Django 3.2.8 on 2021-10-19 15:48

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Chat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField()),
                ('is_seen', models.BooleanField(default=False)),
                ('seen_at', models.DateTimeField(blank=True, null=True)),
                ('sent_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
            ],
            options={
                'verbose_name': 'User Chat',
                'verbose_name_plural': 'User Chats',
                'ordering': ['id'],
            },
        ),
    ]
