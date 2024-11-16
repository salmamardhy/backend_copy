from datetime import datetime, timedelta
from django.db import models
from django.core.validators import RegexValidator
import string
import random

# Admin
class Users(models.Model):
    userid = models.CharField(primary_key=True, max_length=5)
    username = models.CharField(max_length=50)
    usermail = models.EmailField(unique=True, max_length=255, null=False, blank=False, default='example@gmail.com')
    usergroup = models.CharField(max_length=1)
    usergrade = models.IntegerField(blank=True, default='')
    userdesc = models.CharField(max_length=150, blank=True, null=True)

    def __str__(self):
        return str(self.userid)

    class Meta:
        managed = True
        db_table = 'users'
        verbose_name_plural = "Users"

# Member
def generate_member_id(ktpname):
    while True:
        prefix = ktpname[:3].upper()
        rand_num = ''.join(random.choices(string.digits, k=9))
        parity = ''.join(random.choices(string.ascii_uppercase, k=3))
        member_id = f"{prefix}{rand_num[:3]}{parity[0]}{rand_num[3:6]}{parity[1]}{rand_num[6:]}{parity[2]}" 
        if not Member.objects.filter(memberid=member_id).exists():  # Check if the ID is unique
            return member_id

class Member(models.Model):
    letter_validator = RegexValidator(regex=r'^[a-zA-Z\s]+$', message='Only letters and spaces are allowed')
    letterv2_validator = RegexValidator(regex=r'^[a-zA-Z]+$', message='Only letters are allowed, without space')

    memberid = models.CharField(primary_key=True, max_length=15)
    emailmain = models.EmailField(unique=True, max_length=255, null=False, blank=False, default='example@gmail.com')
    accountname = models.CharField(unique=True, max_length=255, default='default_value', validators=[letterv2_validator])
    password = models.CharField(max_length=30)

    ktpname = models.CharField(max_length=100, validators=[letter_validator])
    firstname = models.CharField(max_length=50, validators=[letter_validator])
    middlename = models.CharField(max_length=20, blank=True, null=True, validators=[letter_validator])
    lastname = models.CharField(max_length=50, validators=[letter_validator])
    memberstatus = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        self.accountname = self.accountname.lower()
        self.ktpname = self.ktpname.lower()
        self.firstname = self.firstname.lower()
        self.middlename = self.middlename.lower() if self.middlename else self.middlename
        self.lastname = self.lastname.lower()

        if not self.memberid:
            self.memberid = generate_member_id(self.ktpname)

        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.memberid

    class Meta:
        db_table = 'member'
        verbose_name_plural = "Members"
        managed = True

# Member Detail
class Memberdetail(models.Model):
    letter_validator = RegexValidator(regex=r'^[a-zA-Z\s]+$', message='Only letters and spaces are allowed')
    number_validator = RegexValidator(regex=r'^\d+$', message='Only numbers are allowed')

    memberid = models.OneToOneField(Member, on_delete=models.CASCADE, db_column='memberid', null=True)  # Remove primary_key=True
    callsign = models.CharField(max_length=25, blank=True, default='', validators=[letter_validator])
    participant = models.IntegerField()
    instructor = models.IntegerField()
    author = models.IntegerField()
    referral = models.IntegerField()
    dob = models.DateField()
    ktpnumber = models.CharField(max_length=30, blank=True, default='', validators=[number_validator])
    taxid = models.CharField(max_length=30, blank=True, default='', validators=[number_validator])
    join_date = models.DateField()
    emailmain = models.EmailField(max_length=50)
    emailalt = models.EmailField(max_length=50, blank=True, default='')
    whatsapp = models.CharField(max_length=20, blank=True, default='', validators=[number_validator])
    phone = models.CharField(max_length=20, blank=True, default='', validators=[number_validator])
    telegram = models.CharField(max_length=20, blank=True, default='')
    referralid = models.CharField(max_length=15, blank=True, default='')
    paidclass = models.PositiveIntegerField(default=0, null=True)
    freeclass = models.PositiveIntegerField(default=0, null=True)
    pointtotal = models.PositiveIntegerField(db_column='pointTotal', default=0, null=True)  # Field name made lowercase.
    pointredeem = models.PositiveIntegerField(db_column='pointRedeem', default=0, null=True)  # Field name made lowercase.

    def save(self, *args, **kwargs):
        if self.callsign:
            self.callsign = self.callsign.lower()
        if self.referral:  # If referral is set, assign the memberid's value
            self.referralid = self.memberid.memberid  # Use the actual memberid string
        super().save(*args, **kwargs)

    def __str__(self):
        return str(self.memberid)  # Return the memberid from the related Member instance

    class Meta:
        db_table = 'memberdetail'
        verbose_name_plural = "Member Detail"
        unique_together = (('ktpnumber', 'emailmain'),)
        managed = True


# class OtpToken(models.Model):
#     member = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
#     otp = models.CharField(max_length=8, default=secrets.token_hex(4))
#     created_at = models.DateTimeField(auto_now_add=True)
#     expires_at = models.DateTimeField(blank=True, null=True)

#     def __str__(self):
#         return self.member.memberid