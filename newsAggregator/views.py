import json
import time
from django.contrib.auth import authenticate
from django.contrib.auth import login as django_login
from django.contrib.auth import logout as django_logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from .models import *


@csrf_exempt
def login(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')

        # check whether the user has logged in
        if not request.user.is_authenticated:
            # login successfully
            user1 = authenticate(username=username, password=password)
            if user1 is not None:
                django_login(request, user1)
                request.session.set_expiry(604800)
                return HttpResponse('Welcome! You have successfully logged in.', status=200)
            else:
                return HttpResponse('Wrong password or Username', status=401)
        else:
            # user has logged
            return HttpResponse('User is already authenticated.', status=200)
    else:
        # if the method is not 'post'
        return HttpResponse('Method not allowed', status=405)


@csrf_exempt
@login_required
def logout(request):
    if request.method == 'POST':
        # end sessions
        request.session.flush()
        # logout user
        django_logout(request)
        # send response
        return HttpResponse('Goodbye! You have been successfully logged out.', status=200)
    else:
        # if method is not 'post'
        return HttpResponse('Method not allowed.', status=405)


@csrf_exempt
@login_required
def modify_story(request):
    if request.method == 'POST':
        # check whether user logged in
        if not request.user.is_authenticated:
            return HttpResponse('Unauthorized. Please log in to post a story.', status=503)

        # get story information from json
        try:
            data = json.loads(request.body)
            headline = data['headline']
            category = data['category']
            region = data['region']
            details = data['details']
        except (json.JSONDecodeError, KeyError):
            return HttpResponse('Invalid request data. Please provide all required fields in JSON format.', status=400)
        if category not in ['pol', 'art', 'tech', 'trivial']:
            return HttpResponse("Invalid category!", status=503)
        elif region not in ['uk', 'eu', 'w']:
            return HttpResponse("Invalid region!", status=503)
        # add story into Story form
        try:
            # create new story
            new_story = Story.objects.create(
                headline=headline,
                story_cat=category,
                story_region=region,
                story_details=details,
                story_date=datetime.now(),
                author=request.user.username
            )
            new_story.save()
        except Exception as e:
            return HttpResponse(f'Error creating story: {str(e)}', status=503)

        # response success message if created
        return HttpResponse('Story created successfully.', status=201)
    elif request.method == 'GET':
        if not request.user.is_authenticated:
            return HttpResponse('Unauthorized. Please log in to get stories.', status=503)

        # get information from json
        try:
            data = json.loads(request.body)
            category = data['category']
            region = data['region']
            date = data['date']
        except (json.JSONDecodeError, KeyError):
            return HttpResponse('Invalid request data. Please provide all required fields in JSON format.', status=400)

        if category == '*':
            category_filter = Q()  # 创建一个空的查询对象
        else:
            category_filter = Q(story_cat=category)  # 创建一个筛选category的查询对象

        if region == '*':
            region_filter = Q()  # 创建一个空的查询对象
        else:
            region_filter = Q(story_region=region)  # 创建一个筛选region的查询对象

        if date == '*':
            date_filter = Q()  # 创建一个空的查询对象
        else:
            try:
                time.strptime(date, "%Y-%m-%d")
                date_filter = Q(story_date=date)
            except Exception as e:
                return HttpResponse(f"Error : {str(e)}", status=503)

        # search stories from Story
        stories = Story.objects.filter(
            category_filter & region_filter & date_filter
        )

        # check whether the story exists
        if stories.exists():
            # get all story
            story_list = []
            for story in stories:
                story_data = {
                    'key': story.key,
                    'headline': story.headline,
                    'story_cat': story.story_cat,
                    'story_region': story.story_region,
                    'author': story.author,
                    'story_date': str(story.story_date),
                    'story_details': story.story_details
                }
                story_list.append(story_data)

            # return stories
            response_data = {'stories': story_list}
            return HttpResponse(json.dumps(response_data), content_type='application/json', status=200)
        else:
            # if not found, return error message
            return HttpResponse('No stories found.', status=404)
    else:
        return HttpResponse('Method not allowed', status=405)


@csrf_exempt
@login_required
def delete_story(request, story_key):
    if request.method == 'DELETE':
        # check whether the user has logged in
        if not request.user.is_authenticated:
            return HttpResponse('Unauthorized. Please log in to delete a story.', status=503)

        try:
            # search story needed to be deleted in Story
            story = Story.objects.get(key=story_key)

            # check if the username equal to the author
            if story.author != request.user.username and not request.user.is_superuser:
                return HttpResponse('Forbidden. You are not authorized to delete this story.', status=503)

            # delete the story
            story.delete()

            return HttpResponse('Story deleted successfully.', status=200)
        except Story.DoesNotExist:
            return HttpResponse('Story not found.', status=503)


@csrf_exempt
@login_required
def directory(request):
    if request.method == 'POST':
        try:
            agency_name = request.POST.get('agency_name')
            url = request.POST.get('url')
            agency_code = request.POST.get('agency_code')

            # Save the registration details to the agency
            # Assuming you have an Agency model:
            agency_entry = Agency(agency_name=agency_name, url=url, agency_code=agency_code)
            agency_entry.save()

            return HttpResponse(status=201)
        except Exception as e:
            return HttpResponse(status=503, content='Service Unavailable: ' + str(e))
    elif request.method == 'GET':
        try:
            agencies = Agency.objects.all()

            agency_list = []
            for agency in agencies:
                agency_data = {
                    'agency_name': agency.agency_name,
                    'url': agency.url,
                    'agency_code': agency.agency_code
                }
                agency_list.append(agency_data)

            return HttpResponse(status=200, content_type='application/json', content=json.dumps({
                'agency_list': agency_list
            }))
        except Exception as e:
            return HttpResponse(status=500, content='Internal Server Error: ' + str(e))
    else:
        return HttpResponse(status=405, content='Method Not Allowed')
