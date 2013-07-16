from django.http import HttpResponse
from django.shortcuts import render
from datetime import date, timedelta, datetime, time
from bl_booking.models import contact
from ical.utils import icalParse, tdColour, getWeek
from django.views.decorators.cache import cache_page
    


 
# returns the schedule table
def buildTableBody(week):
   
    bmEvents = icalParse("/webroot/bmit/static/calendar.ics")
    table = '<tbody>'
    
    for weekday in week:
        contacts = contact.objects.filter(day__exact=weekday).values()
        table += '<tr>'
        table += '<td rowspan="3">' + weekday.strftime("%a %b %d/%y") +'</td><td>00:00-08:00</td><td '
        table +=  tdColour(bmEvents, weekday, 0)+ ' >'
        for event in bmEvents:
            if (event['start'] <= datetime.combine(weekday,time(0)) and event['end'] >= datetime.combine(weekday,time(8))):
                table += event['subject']
        table += '</td><td>'
        #ID 0 - 8 goes here
        table += '</td><td rowspan="3">'
        for cont in contacts:
            if weekday == cont['day']:
                table += cont['name']
        table += '</td>'
        table += '</tr>'
        table += '<tr>'
	table += '<td>08:00-16:00</td><td '
        table += tdColour(bmEvents, weekday, 8) + ' >'
        for event in bmEvents:
            if (event['start'] <= datetime.combine(weekday,time(8)) and event['end'] >= datetime.combine(weekday, time(16))):
                table += event['subject']
        table += '</td><td>'
        #ID 8 - 16 goes here
        table += '</td>'
        table += '</tr>'
        table += '<tr>'
        table += '<td>16:00-24:00</td><td '
        table +=  tdColour(bmEvents, weekday, 16) + ' >'
        for event in bmEvents:
            if (event['start'] <= datetime.combine(weekday,time(16)) and event['end'] >= datetime.combine(weekday + timedelta(days = 1), time(0))):
                table += event['subject']
        table += '</td><td>'
        #ID 16 - 24 goes here
        table += '</td></tr>'
      
    table += '</tbody>'
    return table

#@cache_page(60 * 15)   
def index(request):
    currentDate = getWeek(date.today())
    previousWeek = currentDate[0] - timedelta(days=7)
    nextWeek = currentDate[0] + timedelta(days=7)
    context = {'tableBody': buildTableBody(currentDate),
               'previousWeek': previousWeek,
               'nextWeek': nextWeek,
               'week': currentDate}
    return 'bl_booking/base.html', context
#@cache_page(60 * 15)
def week(request, year, month, day):
    currentDate = getWeek(date(int(year), int(month), int(day)))
    previousWeek = currentDate[0] - timedelta(days=7)
    nextWeek = currentDate[0] + timedelta(days=7)
    context = {'tableBody': buildTableBody(currentDate),
               'previousWeek': previousWeek,
               'nextWeek': nextWeek,
               'week': currentDate}
    return 'bl_booking/base.html', context
    
