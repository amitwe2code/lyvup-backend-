from django.db import models


class Activity(models.Model):
    ACTIVITY_TYPES = [
        ('survey', 'survey'),
        ('challenge', 'challenge'),
        ('interview', 'interview'),
        ('video', 'video'),
        ('podcast', 'podcast'),
        ('workshop', 'workshop'),
        ('assignment', 'assignment'),
        ('excercise', 'excercise'),
        ('other', 'other'),
    ]
    LANGUAGES = [
        ('en', 'english'),
        ('fr', 'french'),
        ('nl', 'dutch'),
        ('hn',"hindi"),
    ]
    id = models.AutoField(primary_key=True)
    activity_type = models.CharField(max_length=50, choices=ACTIVITY_TYPES, null=True, blank=True)
    language = models.CharField(max_length=50, choices=LANGUAGES,null=True, blank=True)
    activity = models.CharField(max_length=255,null=True, blank=True)
    brand = models.CharField(max_length=255, null=True, blank=True)
    who = models.TextField(max_length=255, null=True, blank=True)
    completion_check = models.CharField(null=True, blank=True)
    show_completed = models.BooleanField(default=False, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    user_duration = models.IntegerField(null=True,default=0, blank=True)
    teamlead_duration = models.IntegerField(null=True,default=0, blank=True)
    coach_duration = models.IntegerField(null=True, default=0,blank=True)
    coach_type = models.CharField(max_length=50,default='', null=True, blank=True) 
    travel_time = models.IntegerField(null=True, blank=True)
    url = models.URLField(null=True, blank=True)
    amount = models.IntegerField(null=True, blank=True)
    file = models.TextField( null=True, blank=True)   
    upload_possible = models.CharField(default='no',blank=True,null=True)
    activity_description = models.TextField(null=True, blank=True)
    activity_name = models.TextField(max_length=255, null=True, blank=True)
    send_reminder = models.CharField(default='no', blank=True )
    show_in_task = models.CharField(default='no',blank=True)
    add_comment_option = models.CharField(default='no',blank=True)
    indicate_when_completed = models.CharField(default='no',blank=True ,null=True)

    is_active = models.IntegerField(default=1)  
    is_deleted = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
   
    class Meta:
        db_table = 'activity_table'
   
    def save(self, *args, **kwargs):
        if self.activity == "":
            self.activity = None
        if self.brand == "":
            self.brand = None
        if self.who == "":
            self.who = None
        if self.activity_type == "":
            self.activity_type = None
        if self.completion_check == "":
            self.completion_check = None
        if self.location == "":
            self.location = None
        if self.coach_type == "":
            self.coach_type = None
        if self.url == "":
            self.url = None
        if self.user_duration:
            self.user_duration=0
        if self.coach_duration:
            self.coach_duration=0
        if self.teamlead_duration:
            self.teamlead_duration=0
        if self.file == "":
            self.file = None
        if self.activity_description == "":
            self.activity_description = None
        if self.activity_name == "":
            self.activity_name = None
        # If the activity is marked as deleted, set is_active to False and is_deleted to True
        if self.is_deleted:
            self.is_active = 0  # Set is_active to 0 if deleted
        else:
            self.is_active = 1  # Set is_active to 1 if not deleted

        super(Activity, self).save(*args, **kwargs)

    def __str__(self):
        return self.activity_name 
   