# Generated by Django 3.2.8 on 2021-10-19 15:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='status',
            field=models.CharField(choices=[('available', 'Available'), ('busy', 'Busy')], default='available', max_length=30),
        ),
    ]
