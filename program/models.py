from django.db import models

class Program(models.Model):
    id = models.AutoField(primary_key=True)

    name=models.CharField(max_length=100,null=False,blank=False)
    description=models.CharField(max_length=100,null=False,blank=False)
    written_by=models.CharField(max_length=100,null=False,blank=False)
    version=models.CharField(max_length=100,null=False,blank=False)
    price=models.CharField(max_length=100,null=False,blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.IntegerField(default=1)
    is_deleted = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
       
        if self.is_deleted:
            self.is_active = 0  
        else:
            self.is_active = 1  

        super(Program, self).save(*args, **kwargs)


    def __str__(self):
        return self.name

