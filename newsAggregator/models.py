from datetime import datetime

from django.db import models


class Story(models.Model):
    CATEGORY_CHOICES = (
        ('pol', 'politics'),
        ('art', 'Art'),
        ('tech', 'technology'),
        ('trivial', 'trivial news')
    )

    REGION_CHOICES = (
        ('uk', 'United Kingdom news'),
        ('eu', 'European news'),
        ('w', 'World news')
    )

    key = models.AutoField(primary_key=True)
    headline = models.CharField(max_length=64)
    story_cat = models.CharField(max_length=10, choices=CATEGORY_CHOICES)
    story_region = models.CharField(max_length=10, choices=REGION_CHOICES)
    author = models.CharField(max_length=50)
    story_date = models.DateField()
    story_details = models.CharField(max_length=128)

    def __str__(self):
        return self.headline


class Agency(models.Model):
    agency_name = models.CharField(max_length=255)
    url = models.URLField()
    agency_code = models.CharField(max_length=255)

    def __str__(self):
        return self.agency_name
