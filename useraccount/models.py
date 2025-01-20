from django.db import models
from userapp.models import UserModel
from account.models import AccountModel
# Create your models here.
class UserAccountModel(models.Model):
    id=models.AutoField(primary_key=True)
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    account = models.ForeignKey(AccountModel, on_delete=models.CASCADE)
    is_active = models.IntegerField(default=1)
    is_deleted = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
       
        if self.is_deleted:
            self.is_active = 0  
        else:
            self.is_active = 1  

        super(UserAccountModel, self).save(*args, **kwargs)


    def __str__(self):
        return f'{self.user.name} - {self.account.account_name}'
    
    class Meta:
        db_table = 'user_account'
        unique_together = ('user', 'account')
    
   