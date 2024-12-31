from django.db import models

class ActivityActionType(models.Model):
    activity_type = models.CharField(max_length=255,null=True, blank=True)
    activity = models.CharField(max_length=255,null=True, blank=True)
    amount = models.IntegerField(null=True, blank=True)
    unit = models.IntegerField(null=True, blank=True)
    key_activity = models.CharField(max_length=255,null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True,null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True,null=True, blank=True)
    is_active = models.BooleanField(default=True,null=True, blank=True)
    # is_active = models.BooleanField(default=True,null=True, blank=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.activity_type

    # class Meta:
    #     db_table = 'activity_action_type'
