from django.db import models
from userapp.models import UserModel

class GDPRRequestModel(models.Model):
    REQUEST_TYPE_CHOICES = [
        ('access', 'Access'),
        ('deletion', 'Deletion'),
        ('rectification', 'Rectification'),
    ]

    REQUEST_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('denied', 'Denied'),
    ]

    user_id = models.ForeignKey(UserModel,on_delete=models.CASCADE,null=True)  
    request_type = models.CharField(max_length=20,null=False, choices=REQUEST_TYPE_CHOICES)
    request_status = models.CharField(max_length=10, choices=REQUEST_STATUS_CHOICES, default='pending')
    requested_at = models.DateTimeField(auto_now_add=True) 
    processed_at = models.DateTimeField(auto_now=True) 
    is_deleted = models.IntegerField(default=0)
    is_active = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'gdprrequest'
    def __str__(self):
        return f"GDPR for User {self.user_id}"