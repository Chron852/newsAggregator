# Generated by Django 5.0.3 on 2024-04-13 06:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('newsAggregator', '0006_alter_story_author_alter_story_headline_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='User',
        ),
    ]