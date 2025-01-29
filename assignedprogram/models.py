from django.db import models
from organization.models import OrganizationModel
from account.models import AccountModel
from program.models import Program
# Create your models here.
class AssignedProgramModel(models.Model):
    ASSIGN_TYPE_CHOICES = [
        ('user', 'User'),
        ('team', 'Team'),
    ]
    STATUS_CHOICES = [
        (0, 'Inactive'),
        (1, 'Active'),
    ]
    assign_to = models.TextField()
    assign_type = models.CharField(max_length=5, choices=ASSIGN_TYPE_CHOICES)
    account_id = models.IntegerField(null=True,blank=True)
    company_id = models.IntegerField(null=True,blank=True)
    program_id = models.IntegerField(null=True,blank=True)
    start_date = models.DateField()
    end_date = models.DateField(null=True,blank=True)
    status = models.IntegerField(choices=STATUS_CHOICES, default=0)
    is_completed = models.IntegerField(choices=[(0, 'No'), (1, 'Yes')], default=0)
    updated_on = models.DateTimeField(auto_now=True)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Assignment {self.id} to {self.assign_to}'
