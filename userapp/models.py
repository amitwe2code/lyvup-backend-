from django.db import models
from django.core.validators import MinLengthValidator, RegexValidator
from account.models import AccountModel

class UserModel(models.Model):
    USER_TYPE_CHOICES = [
        ('SUPERADMIN', 'Superadmin'),
        ('PATIENT', 'Patient'),
        ('HEALTHCARE_PROVIDER', 'Healthcare Provider'),
        ('TEAMLEAD', 'Teamlead'),
        ('FRIEND', 'Friend'),
    ]

    STATUS_CHOICES = [
        ('ACTIVE', 'Active'),
        ('INACTIVE', 'Inactive'),
        ('SUSPENDED', 'Suspended'),
    ]

    name = models.CharField(
        max_length=100,
        validators=[
            RegexValidator(
                regex=r'^[a-zA-Z\s]{2,}$',
                message='Name must contain only letters and spaces, minimum 2 characters'
            )
        ]
    )
    email = models.EmailField(
        unique=True,
        error_messages={
            'unique': 'An account with this email already exists',
            'invalid': 'Please enter a valid email address'
        }
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
        default='PATIENT',
        error_messages={
            'invalid_choice': 'Please select a valid user type'
        }
    )
    profile_picture = models.ImageField(
        upload_to= 'media/',
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
        default='en', 
        blank=True, 
        null=True
    )
    status = models.CharField(
        max_length=50, 
        choices=STATUS_CHOICES, 
        default='ACTIVE',
        error_messages={
            'invalid_choice': 'Please select a valid status'
        }
    )
    is_team_leader = models.BooleanField(default=False)
    wly_token = models.BooleanField(default=False)
    is_used_token = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    password = models.CharField(
        max_length=128,
        null=False,
        blank=False,
        editable=True,
        error_messages={
            'required': 'Password is required',
            'blank': 'Password cannot be blank'
        },
        validators=[
            MinLengthValidator(8, 'Password must be at least 8 characters long'),
            RegexValidator(
                regex=r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&#])[A-Za-z\d@$!%*?&#]{8,}$',
                message='Password must contain at least one uppercase letter, one lowercase letter, one number and one special character (@$!%*?&#)'
            ),
        ],
    )

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'user'