from django.shortcuts import render
# from django.http import HttpResponse
from firebase import firebase
import pandas as pd
import json
import matplotlib.pyplot as plt


# Create your views here.
'''
posts = [
    {
        'author': 'Yuanyuan',
        'title': 'test',
        'content': 'first time test',
        'date_posted': 'July 3, 2020'
    },
{
        'author': 'Yuanyuan2',
        'title': 'test2',
        'content': 'first time test2',
        'date_posted': 'July 3, 2020'
    }

]
'''

fbobject = firebase.FirebaseApplication("https://canbewell-uottawa.firebaseio.com/", None)
fbdata_temp = fbobject.get("", "")
# get keys of fbdata_temp: fbdata_temp.keys()


# data_list should be created by user input later.
date_list = ['20200709', '20200710']


fbdata = pd.DataFrame()
for i in range(0, len(date_list)):
    temp = pd.DataFrame.from_dict(fbdata_temp[date_list[i]], orient='index')
    fbdata = fbdata.append(temp)


def home(request):
    context = {
        'page_title': 'Blog Home',
        'fbdata': fbdata,
        'fbdata_temp': fbdata_temp
    }
    return render(request, 'blog/home.html', context)


def about(request):
    context = {
        'page_title': 'About Page'
    }
    return render(request, 'blog/about.html', context)
