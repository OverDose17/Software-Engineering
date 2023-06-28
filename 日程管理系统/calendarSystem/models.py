from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.

class Event(models.Model):
    event_id = models.AutoField(primary_key = True)
    title = models.CharField(max_length = 200)
    description = models.TextField()
    start_time = models.DateTimeField()
    # end_time = models.DateTimeField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    event_type = models.IntegerField(default=3)

    class Meta:
        db_table = "Event"

    @property
    def get_html_url(self):
        url = reverse('calendarSystem:event_edit', args=(self.event_id,))
        return f'<a href="{url}"> {self.title} </a>'