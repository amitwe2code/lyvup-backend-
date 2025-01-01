from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.core.validators import RegexValidator
from account.models import AccountModel

class UserManager(BaseUserManager):
    def create_user(self, email, password,user_type, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        if not password:
            raise ValueError('Password is required')
        if not user_type:
            raise ValueError('User type is required')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        if not password:
            raise ValueError('Password is required')
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('user_type', 'SUPERADMIN')
        return self.create_user(email, password, **extra_fields)

class UserModel(AbstractBaseUser, PermissionsMixin):
    USER_TYPE_CHOICES = [
        ('patient', 'patient'), 
        ('admin', 'admin'),
        ('superadmin', 'superadmin'),
    ]

    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'), 
        ('suspended', 'Suspended'),
    ]

    email = models.EmailField(unique=True)
    name = models.CharField(
        max_length=100,
        validators=[
            RegexValidator(
                regex=r'^[a-zA-Z\s]{2,}$',
                message='Name must contain only letters and spaces, minimum 2 characters'
            )
        ]
    )
    account_id = models.ForeignKey(
        AccountModel,
        on_delete=models.CASCADE,
        related_name='account',
        null=True,
        blank=True
    )
    team_leader_id = models.CharField(
        max_length=100,
        default=None,
        null=True, 
        blank=True
    )
    phone = models.CharField(
        max_length=10,
        validators=[
            RegexValidator(
                regex=r'^\d{10}$',
                message='Phone number must be exactly 10 digits'
            )
        ]
    )
    user_type = models.CharField(
        max_length=50,
        choices=USER_TYPE_CHOICES,
        default='patient',
        error_messages={
            'invalid_choice': 'Please select a valid user type'
        }
    )
    profile_picture = models.CharField(
        # upload_to='media/',
        null=True,
        blank=True,
        max_length=255,
        error_messages={
            'invalid': 'Please upload a valid image file',
            'invalid_image': 'The uploaded file is not a valid image'
        },
    )
    language_preference = models.CharField(
        max_length=10,
        default='english',
        blank=True,
        null=True
    )
    status = models.CharField(
        max_length=50,
        choices=STATUS_CHOICES,
        default='active',
        error_messages={
            'invalid_choice': 'Please select a valid status'
        }
    )
    is_team_leader = models.BooleanField(default=False)
    wly_token = models.BooleanField(default=False)
    is_used_token = models.BooleanField(default=False)
    is_deleted = models.IntegerField(default=0)
    is_active = models.IntegerField(default=1)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def save(self, *args, **kwargs):
       
        if self.is_deleted:
            self.is_active = 0  
        else:
            self.is_active = 1  

        super(UserModel, self).save(*args, **kwargs)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'phone']

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'user'