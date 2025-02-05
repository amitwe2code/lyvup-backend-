# notifications/models.py
from django.db import models

class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ('project_assigned', 'Project Assigned'),
        ('message', 'Message'),
        # Add other types as needed
    ]
    
    id = models.AutoField(primary_key=True)  
    type = models.CharField(max_length=50, choices=NOTIFICATION_TYPES)
    from_id = models.PositiveIntegerField()  
    from_type = models.CharField(max_length=50)  
    to_id = models.PositiveIntegerField() 
    to_type = models.CharField(max_length=50)  
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True) 

    def __str__(self):
        return f"Notification for {self.to_id} - {self.message}"
    class Meta:
        db_table = 'notification_table'    