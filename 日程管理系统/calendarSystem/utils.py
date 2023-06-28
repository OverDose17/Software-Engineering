from calendar import HTMLCalendar, monthrange
from .models import Event, User
import array as arr

class Calendar(HTMLCalendar):
	def __init__(self, year=None, month=None):
		self.year = year
		self.month = month
		super(Calendar, self).__init__()

	# formats a day as a td
	# filter events by day
	def formatday(self, day, events, supers):
		events_per_day = events.filter(start_time__day=day)
		d = ''
		for event in events_per_day:
			if event.owner_id in supers:
				str2 = f'<li> <strong>{event.get_html_url} (assigned by {event.owner})</strong> </li>' 
				d += str2
			else :
				str2 = f'<li> {event.get_html_url} </li>'
				d += str2
		if day != 0:
			return f"<td><span class='date'>{day}</span><ul> {d} </ul></td>"
		return '<td></td>'

	# formats a week as a tr
	def formatweek(self, theweek, events, supers):
		week = ''
		for d, weekday in theweek:
			week += self.formatday(d, events, supers)
		return f'<tr> {week} </tr>'

	# formats a month as a table
	# filter events by year and month
	def formatmonth2(self, withyear=True, owner = None, supers=None): # in here supers still not used, so will be error
		events = Event.objects.filter(start_time__year=self.year, start_time__month=self.month, owner_id = owner )
	
		cal = f'<table border="0" cellpadding="0" cellspacing="0" class="calendar">\n'
		cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
		cal += f'{self.formatweekheader()}\n'
		for week in self.monthdays2calendar(self.year, self.month):
			cal += f'{self.formatweek(week, events, supers)}\n'
		return cal
	
	def formatmonth(self, withyear=True, owner = None):
		events = Event.objects.filter(start_time__year=self.year, start_time__month=self.month).order_by('start_time')
		supers = listSuperUser() # superuser
		for e in events:
			if not (e.owner_id == owner.id or e.owner_id in supers):
				events = events.exclude(event_id = e.event_id)

		cal = f'<table border="0" cellpadding="0" cellspacing="0" class="calendar">\n'
		cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
		cal += f'{self.formatweekheader()}\n'
		for week in self.monthdays2calendar(self.year, self.month):
			cal += f'{self.formatweek(week, events, supers)}\n'
		return cal
	
def statisticutilsadmin(y, m, owner):
	counter = 0
	events = Event.objects.filter(start_time__year=y, owner_id = owner )
	events = events.filter( start_time__month=m, owner_id = owner ).order_by('start_time') # filter once more
	typea = [] # lifestyle
	typeb = []
	typec = []
	totalday= monthrange(int(y), int(m))[1]
	total_arr = arr.array('i')	
	total_arr = [0] * (totalday + 1)

	total_type = [0] * 3

	for obj in events :
		total_arr[obj.start_time.day] += 1
		counter += 1
		if obj.event_type == 1 :
			total_type[0] += 1
			typea.append(obj)
		elif obj.event_type == 2:
			total_type[1] += 1
			typeb.append(obj)
		else :
			total_type[2] += 1
			typec.append(obj)	
	total_arr.remove(0)
	x = list(range(1, totalday + 1))
	return x, total_arr, total_type, typea, typeb, typec

def statisticutils(y, m, owner):
	counter = 0
	events = Event.objects.filter(start_time__year=y)
	events = events.filter( start_time__month=m).order_by('start_time') # filter once more
	supers = listSuperUser()
	typea = [] # lifestyle
	typeb = []
	typec = []
	for e in events:
		if e.owner != owner and not e.owner_id in supers:
			events = events.exclude(event_id = e.event_id)
		else:
			if e.event_type == 1:
				typea.append(e)
			elif e.event_type == 2:
				typeb.append(e)
			elif e.event_type == 3:
				typec.append(e)
	totalday= monthrange(int(y), int(m))[1]
	total_arr = arr.array('i')	# set to integer array
	total_arr = [0] * (totalday + 1)

	total_type = [0] * 3

	for obj in events :
		total_arr[obj.start_time.day] += 1
		counter += 1
		if obj.event_type == 1 :
			total_type[0] += 1
		elif obj.event_type == 2:
			total_type[1] += 1
		else :
			total_type[2] += 1
	total_arr.remove(0)

	x = list(range(1, totalday + 1))
	return x, total_arr, total_type, typea, typeb, typec

def listSuperUser():
    supUsers = User.objects.filter(is_superuser = True)
    supers = []
    for su in supUsers: # getsuper all user
        supers.append(su.id)
    return supers