from datetime import datetime, timedelta, date
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.utils.safestring import mark_safe
import calendar
from .models import *
from .utils import Calendar, statisticutils, listSuperUser, statisticutilsadmin
from functools import reduce
from django.contrib import messages

def index(request):
    if request.user.is_authenticated:
        return render(request, "index.html")
    else:
        return render(request, "indexout.html")
    
def calendar_view(request):
    if request.user.is_authenticated:
        d = get_date(request.GET.get('month', None))
        print("this is d in view", d)
        cal = Calendar(d.year, d.month)
        html_cal = cal.formatmonth(withyear=True, owner = request.user)
        obj = Event.objects.filter(owner_id=request.user)
        x = str(d).split("-")
        # print("todate = ", todate.)
        # dateval = str(todate.year) + "-" + str(todate.month) +"-01T08:30"
        dateval = "month=" + str(d.year) + "-" + str(d.month)
        print("date val is", dateval)
        thedate = ""
        thedate += x[0]
        thedate += "-"
        thedate += x[1]
        context = {
            'calendar': mark_safe(html_cal),
            'prev_month': prev_month(d),
            'next_month': next_month(d),
            'date': d,
            'thedate':thedate,
            'object_list': obj,
            'dateval': dateval,
        }
        
        return render(request, 'calendar.html', context)
    else:
        return redirect("/login") 
    
    
def get_date(req_month):
    if req_month:
        year, month = (int(x) for x in req_month.split('-'))
        return date(year, month, day=1)
    return datetime.today()

def prev_month(d):
    first = d.replace(day = 1)
    prev_month = first - timedelta(days = 1)
    month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
    return month

def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days = 1)
    month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
    return month

def event(request, mydate):
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        start_time = request.POST.get("start_time")
        event_type = request.POST.get("event_type")
        event = Event(title = title, description = description, start_time = start_time, event_type = event_type, owner = request.user)
        event.save()
        event = Event.objects.get(event_id = event.event_id)
        # return HttpResponseRedirect(reverse('calendarSystem:calendar'))
        date = "month="
        date += str(event.start_time.year)
        date += "-"
        date += str(event.start_time.month)
        
        return HttpResponseRedirect(reverse('calendarSystem:calendar') + "?" + date)
    # caldate =  mydate + "-01T08:30"
    print("caldate is ",mydate)
    return render(request, 'event.html', {'caldate':mydate})

def editevent(request, event_id=None): # create new event
    if request.user.is_authenticated and not request.user.is_superuser:
        event = Event.objects.get(event_id = event_id)
        flagtype = event.event_type
        type = revnumtype(event.event_type)
        supersList = listSuperUser()
        flagadmin = False
        if event.owner_id in supersList :
            flagadmin = True
        date = "month="
        date += str(event.start_time.year)
        date += "-"
        date += str(event.start_time.month)
        return render(request, 'eventedit.html',{'event':event, 'type':type, 'flagtype':flagtype, 'flagadmin':flagadmin, 'date':date})
    
    elif request.user.is_authenticated and request.user.is_superuser:
        event = Event.objects.get(event_id = event_id)
        flagtype = event.event_type
        type = revnumtype(event.event_type)
        supersList = listSuperUser()
        flagadmin = False
        if event.owner_id in supersList and event.owner_id != request.user.id:
            flagadmin = True
        date = "month="
        date += str(event.start_time.year)
        date += "-"
        date += str(event.start_time.month)
        return render(request, 'eventedit.html',{'event':event, 'type':type, 'flagtype':flagtype, 'flagadmin':flagadmin, 'date':date})
    else:
        return redirect("/login")
                    
def revnumtype(num): #reverse numeric type
    if num == 1:
        return "Lifestyle"
    elif num == 2:
        return "Academic"
    else :
        return "Not Specified"
    
def updateevent(request, event_id=None): # edit new event
    if request.user.is_authenticated:
        # print("request post is ",request.POST)
        event = Event.objects.get(event_id = event_id)
        date = "month="
        date += str(event.start_time.year)
        date += "-"
        date += str(event.start_time.month)
        if 'update' in request.POST:
            # print("request post is update")
            title = request.POST.get("title")
            description = request.POST.get("description")
            type = request.POST.get("event_type")
            Event.objects.filter(event_id = event_id).update(title = title, description = description, event_type = type)
            messages.success(request, 'Update Succeed')
            return HttpResponseRedirect(reverse('calendarSystem:event_edit', args=(event_id,)))
        elif 'delete' in request.POST:
            # print("request post is delete")
            return redirect("/cal/event/delete/" + event_id) 
        else:
            return HttpResponseRedirect(reverse('calendarSystem:calendar')+"?"+date)
    else:
        return redirect("/login") 

def delete(request, event_id):
    if request.user.is_authenticated:
        event = Event.objects.get(event_id = event_id)
        # return HttpResponseRedirect(reverse('calendarSystem:calendar'))
        date = "month="
        date += str(event.start_time.year)
        date += "-"
        date += str(event.start_time.month)
        event.delete()
        return HttpResponseRedirect(reverse('calendarSystem:calendar')+"?"+date)
    
    else:
        return redirect("/login") 

def user_info(request): # check data transfer
    text = f"""
        Selected HttpRequest.user attributes:

        username:     {request.user.username}
        is_anonymous: {request.user.is_anonymous}
        is_staff:     {request.user.is_staff}
        is_superuser: {request.user.is_superuser}
        is_active:    {request.user.is_active}
    """
    return HttpResponse(text, content_type="text/plain")

def statistic(request, mydate): # need convert from str to date 
    if request.user.is_authenticated:
        if mydate:
            x = str(mydate).split("-")
            # cal = Calendar(x[0], x[1])
            y = x[0]
            m = x[1]
        else :
            d = get_date(request.GET.get('month', None))
            # cal = Calendar(d.year, d.month)
            y = d.year
            m = d.month
        if request.user.is_superuser:
            xaxis, yaxis, types, typea, typeb, typec = statisticutilsadmin(y, m, request.user)
        else:
            xaxis, yaxis, types, typea, typeb, typec = statisticutils(y, m, request.user)
        countinga = countingdown(typea)
        countingb = countingdown(typeb)
        countingc = countingdown(typec)
        month = calendar.month_name[int(m)]
        date = "month="
        date += str(y)
        date += "-"
        date += str(m)
        context = {
            'y':y,
            'm':month,
            'label': xaxis,
            'data': yaxis,
            'types': types,
            'typea': typea,
            'typeb': typeb,
            'typec': typec,
            'countinga': countinga,
            'countingb': countingb,
            'countingc': countingc,
            'date': date,
        }
        return render(request, 'statistic.html', context)

    else:
        return redirect("/login") 

def countingdown(typex): # givea list of event
    today = date.today()
    counts = []
    for e in typex:
        date2 = date(e.start_time.year, e.start_time.month, e.start_time.day)
        num = numOfDays(date2, today)
        if date2 < today:
            counts.append("expired")
        else:
            counts.append(abs(num))    
    return counts

def numOfDays(date1, date2):
    return reduce(lambda x, y: (y-x).days, [date1, date2])