from django.db import models


class OrganizationModel(models.Model):
    organization_name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    created_by = models.TextField(max_length=100)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.organization_name
    
    class Meta:
        db_table = 'organization'