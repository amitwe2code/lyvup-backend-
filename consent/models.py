from django.db import models
from userapp.models import UserModel
# Create your models here.
class ConsentModel(models.Model):
    CONSENT_TYPE_CHOICES = [
        ('data sharing', 'Data Sharing'),
        ('third-party access', 'Third-party Access'),
    ]

    CONSENT_STATUS_CHOICES = [
        ('given', 'Given'),
        ('revoked', 'Revoked'),
    ]

    user_id = models.ForeignKey(UserModel,on_delete=models.CASCADE,null=True)  
    consent_type = models.CharField(max_length=20,null=False, choices=CONSENT_TYPE_CHOICES)
    consent_status = models.CharField(max_length=10, choices=CONSENT_STATUS_CHOICES, default='given')
    consent_date = models.DateField(auto_now_add=True)
    is_deleted = models.IntegerField(default=0)
    is_active = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)    

    class Meta:
        db_table = 'consent_table'  

    def __str__(self):
        return f"Consent for User {self.user_id}"