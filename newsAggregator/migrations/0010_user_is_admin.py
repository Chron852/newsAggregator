# Generated by Django 5.0.3 on 2024-04-19 13:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newsAggregator', '0009_user_alter_story_story_cat'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_admin',
            field=models.BooleanField(default=False),
        ),
    ]
