from django.shortcuts import render
from django.http import HttpResponse
from firebase import firebase
import pandas as pd
from .myform import dateRangeForm
import datetime


# Create your views here.


def firebase_date_range(startDate, endDate):
    diff = endDate - startDate
    date_list = list()
    for i in range(diff.days + 1):
        date_temp = startDate + datetime.timedelta(i)
        date_temp = date_temp.strftime("%Y%m%d")
        date_list.append(date_temp)
    return date_list


def firebase_live_connection(date_list):
    fbdata = pd.DataFrame()
    fbobject = firebase.FirebaseApplication("https://canbewell-uottawa.firebaseio.com/", None)
    fbdata_temp = fbobject.get("", "")
    for i in range(0, len(date_list)):
        try:
            temp = pd.DataFrame.from_dict(fbdata_temp[date_list[i]], orient='index')
            fbdata = fbdata.append(temp)
        except:
            print('date exception caught -- ', str(date_list[i]))
    return fbdata


def data_cleaning(fbdata):
    avg_view_time = fbdata['pageviewtime'].mean()
    fbdata['pageviewtime'].fillna(avg_view_time, inplace=True)
    agerange = [''] * len(fbdata)
    for i in range(0, len(fbdata)):
        if fbdata.age[i] == 'all ages':
            agerange[i] = 'all ages'
        elif '{:0>3}'.format(fbdata.age[i]) <= '049':
            agerange[i] = 'Young'
        elif '{:0>3}'.format(fbdata.age[i]) <= '064':
            agerange[i] = 'Middle'
        else:
            agerange[i] = 'Senior'
    fbdata.insert(0, 'firebase_json_index', fbdata.index)
    fbdata.insert(1, 'agerange', agerange)
    fbdata.reset_index(drop=True, inplace=True)
    fbdata.index = fbdata.index + 1
    return fbdata


def Download_csv(self):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=canbewell_data_export.csv'
    #fbdata.to_csv(path_or_buf=response, sep=';', float_format='%.2f', index=False, decimal=",")
    fbdata.to_csv(path_or_buf=response, index=True)
    return response


def home(request):
    if request.method == 'POST':
        form = dateRangeForm(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data['startDate']
            end_date = form.cleaned_data['endDate']
            date_list = firebase_date_range(start_date, end_date)
            if date_list:
                global fbdata
                fbdata = firebase_live_connection(date_list)
                fbdata = data_cleaning(fbdata)
                context = {
                    'page_title': 'Analysis Home',
                    'fbdata': fbdata,
                    'form': dateRangeForm(),
                    'start_date': start_date,
                    'end_date': end_date
                }
            else:
                context = {
                    'page_title': 'Analysis Home',
                    'form': dateRangeForm()
                }
    else:
        context = {
            'page_title': 'Analysis Home',
            'form': dateRangeForm()
        }
    return render(request, 'analysis/home.html', context)


def about(request):
    context = {
        'page_title': 'About Page'
    }
    return render(request, 'analysis/about.html', context)
