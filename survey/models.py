from django.db import models

class Intervention(models.Model):
    INTERVENTION_TYPES = [
        ('Survey', 'Survey'),
        ('Challenge', 'Challenge'),
        ('Interview', 'Interview'),
        ('Video', 'Video'),
        ('Podcast', 'Podcast'),
        ('Workshop', 'Workshop'),
        ('Assignment', 'Assignment'),
        ('Exercise', 'Exercise'),
        ('Other', 'Other'),
    ]
    LANGUAGES = [
        ('English', 'English'),
        ('French', 'French'),
        ('Other', 'Other'),
    ]

    intervention_type = models.CharField(max_length=50, choices=INTERVENTION_TYPES)
    language = models.CharField(max_length=50, choices=LANGUAGES)
    activity = models.CharField(max_length=255)
    brand = models.CharField(max_length=255, null=True, blank=True)
    who = models.CharField(max_length=255, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    costs = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    send_reminder = models.BooleanField(default=False)
    add_comment_option = models.BooleanField(default=False)
    show_completed = models.BooleanField(default=False)
    location = models.CharField(max_length=255, null=True, blank=True)
    user_duration = models.IntegerField(null=True, blank=True)
    duration_teamlead = models.IntegerField(null=True, blank=True)
    duration_coach = models.IntegerField(null=True, blank=True)
    coach_type = models.CharField(max_length=50, null=True, blank=True)
    travel_time = models.IntegerField(null=True, blank=True)
    url = models.URLField(null=True, blank=True)
    amount = models.IntegerField(null=True, blank=True)
    file = models.FileField(upload_to='uploads/', null=True, blank=True)
    upload_possible = models.BooleanField(default=False)
    intervention_description = models.TextField(null=True, blank=True)
    intervention_name = models.CharField(max_length=255, null=True, blank=True)
    show_in_tasks = models.BooleanField(default=False)
    indicate_when_completed = models.BooleanField(default=False)

    def __str__(self):
        return self.activity
