import json
from django.db import models
# from django.utils import timezone


class Snippet(models.Model):
    LORENZO, BENNI, MARTINA, LINDA = 1, 2, 3, 4

    PROFILE_CHOICES = (
        (LORENZO, 'lorenzo.writing'),
        (BENNI, 'benni.wolf09'),
        (MARTINA, 'martina.dresdner'),
        (LINDA, 'linda-welle'),
    )

    PROCESSING, QUEUED, ERROR, ACCEPTED, CANCELLED = 0, 1, 2, 3, 99

    STATUS_CHOICES = (
        (PROCESSING, 'processing'),
        (QUEUED, 'queued'),
        (ERROR, 'error'),
        (ACCEPTED, 'accepted'),
        (CANCELLED, 'cancelled')
    )

    profile = models.IntegerField(
        choices=PROFILE_CHOICES, null=True, blank=True)
    title = models.TextField(max_length=500, null=True, blank=True)
    description = models.TextField(max_length=1000, null=True, blank=True)
    keywords = models.TextField(max_length=1000, null=True, blank=True)
    username = models.TextField(max_length=1000, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(default=PROCESSING, choices=STATUS_CHOICES)

    class Meta:
        ordering = ['date', 'status']

    # This is for basic and custom serialisation to return it to client as JSON.
    @property
    def to_dict(self):
        data = {
            'data': json.loads(self.data),
            'date': self.date,
            'status': self.status
        }
        return data

    def __str__(self):
        return '{} - {} - {}'.format(
            str(self.profile), self.title, self.description
        )
