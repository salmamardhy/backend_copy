from datetime import timedelta, datetime
from django.db import models
from account.models import Users

class LookUp(models.Model):
    lookkey = models.CharField(max_length=3) 
    lookcode = models.CharField(max_length=30)
    lookname = models.CharField(max_length=100)
    lookdesc = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.lookname

    class Meta:
        db_table = 'lookup'
        managed = True
        constraints = [
            models.UniqueConstraint(fields=['lookkey', 'lookcode'], name='combouniq_lookup')
        ]

class Vanue(models.Model):
    vanuename = models.CharField(max_length=100)
    location = models.CharField(max_length=250)
    vanueurl = models.URLField(null=True, blank=True)
    vanuegmap = models.URLField(null=True, blank=True)
    phone = models.CharField(max_length=20)
    photo = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.vanuename
    
    def save(self, *args, **kwargs):
        if self.photo and "drive.google.com" in self.photo:
            self.photo = self.photo.replace("/view?usp=sharing", "")
            self.photo = self.photo.replace("https://drive.google.com/file/d/", "https://drive.google.com/thumbnail?id=")
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'vanue'

class CourseMaterial(models.Model):
    courseid = models.CharField(primary_key=True, max_length=7)
    coursename = models.CharField(max_length=100,  db_index=True)
    coursedesc = models.CharField(max_length=200, null=True, blank=True)
    creator = models.ForeignKey(to='account.Member', on_delete=models.SET_NULL, null=True, blank=True, related_name='creators')
    languages = models.ForeignKey(LookUp, on_delete=models.SET_NULL, null=True, blank=True, related_name='languages', limit_choices_to={'lookkey': 'AA'})
    category = models.ForeignKey(LookUp, on_delete=models.SET_NULL, null=True, blank=True, related_name='category', limit_choices_to={'lookkey': 'BE'})
    submission = models.DateTimeField(auto_now_add=True)
    paidrun = models.PositiveIntegerField(blank=True, null=True, default=0)
    freerun = models.PositiveIntegerField(blank=True, null=True, default=0)
    folder = models.CharField(max_length=250, blank=True, null=True)
    thumbnailurl = models.URLField(blank=True, null=True)
    coursetype = models.ForeignKey(LookUp, on_delete=models.SET_NULL, null=True, blank=True, related_name='coursetype', limit_choices_to={'lookkey': 'BA'})
    courselab = models.BooleanField()
    labdesc = models.CharField(max_length=250, blank=True, null=True)
    landingpage = models.CharField(max_length=250, blank=True, null=True)
    marketingtoolkit = models.CharField(max_length=250, blank=True, null=True)

    def __str__(self):
        return self.courseid
    
    def save(self, *args, **kwargs):
        # Ensure that category is always set to a valid lookkey value
        # if isinstance(self.category, str):
        #     try:
        #         self.category = LookUp.objects.get(lookkey=self.category)
        #     except LookUp.DoesNotExist:
        #         raise ValueError(f"Invalid category '{self.category}' provided.")
        
        # if isinstance(self.languages, str):
        #     try:
        #         self.languages = LookUp.objects.get(lookkey=self.languages)
        #     except LookUp.DoesNotExist:
        #         raise ValueError(f"Invalid language '{self.languages}' provided.")
        
        # if isinstance(self.coursetype, str):
        #     try:
        #         self.coursetype = LookUp.objects.get(lookkey=self.coursetype)
        #     except LookUp.DoesNotExist:
        #         raise ValueError(f"Invalid course type '{self.coursetype}' provided.")

        if self.coursename:
            self.coursename = self.coursename.lower()

        if self.thumbnailurl and "drive.google.com" in self.thumbnailurl:
            self.thumbnailurl = self.thumbnailurl.replace("/view?usp=sharing", "")
            self.thumbnailurl = self.thumbnailurl.replace("https://drive.google.com/file/d/", "https://drive.google.com/thumbnail?id=")
        super().save(*args, **kwargs)
    
    class Meta:
        db_table = 'coursematerial'

# Certified Instructor
class Certifiedinstructor(models.Model):
    courseid = models.ForeignKey(CourseMaterial, on_delete=models.SET_NULL, null=True, blank=True, related_name='courseid_instructor')
    instructor = models.CharField(primary_key=True, max_length=15)
    description = models.CharField(max_length=250, blank=True, null=True)

    def __str__(self):
        return self.instructor

    class Meta:
        managed = True
        db_table = 'certifiedinstructor'
        constraints = [
            models.UniqueConstraint(fields=['courseid', 'instructor'], name='combouniq_courseid_instructor')
        ]

# Certified Assistant
class Certifiedassistant(models.Model):
    courseid = models.ForeignKey(CourseMaterial, on_delete=models.SET_NULL, null=True, blank=True, related_name='courseid_assistant')
    assistant = models.CharField(primary_key=True, max_length=15)
    description = models.CharField(max_length=250, blank=True, null=True)

    def __str__(self):
        return self.assistant

    class Meta:
        managed = True
        db_table = 'certifiedassistant'
        constraints = [
            models.UniqueConstraint(fields=['courseid', 'assistant'], name='combouniq_courseid_assistant')
        ]

class Class(models.Model):
    classid = models.CharField(primary_key=True, max_length=9)
    classname = models.CharField(max_length=100, null=True, blank=True)
    courseid = models.ForeignKey(CourseMaterial, on_delete=models.SET_NULL, null=True, blank=True)
    presenter = models.ForeignKey(Certifiedinstructor, on_delete=models.SET_NULL, null=True, blank=True, related_name='presenter')
    assistant1 = models.ForeignKey(Certifiedassistant, on_delete=models.SET_NULL, null=True, blank=True, related_name='assistant1')
    assistant2 = models.ForeignKey(Certifiedassistant, on_delete=models.SET_NULL, null=True, blank=True, related_name='assistant2')
    assistant3 = models.ForeignKey(Certifiedassistant, on_delete=models.SET_NULL, null=True, blank=True, related_name='assistant3')
    #         migrations.AlterField(
    #         model_name='class',
    #         name='assistant1',
    #         field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='assistant1', to='course.certifiedinstructor'),
    #     ),
    #     migrations.AlterField(
    #         model_name='class',
    #         name='assistant2',
    #         field=models.ForeignKey(blank=true, null=true, on_delete=django.db.models.deletion.SET_NULL, related_name='assistant2', to='course.certifiedinstructor'),
    #     ),
    #     migrations.AlterField(
    #         model_name='class',
    #         name='assistant3',
    #         field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='assistant3', to='course.certifiedinstructor'),
    #     ),
    #     migrations.AlterField(
    #         model_name='class',
    #         name='presenter',
    #         field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='presenter', to='course.certifiedinstructor'),
    #     ),
    # presenter = models.CharField(max_length=100, null=True, blank=True)
    # assistant1 = models.CharField(max_length=100, null=True, blank=True)
    # assistant2 = models.CharField(max_length=100, null=True, blank=True)
    # assistant3 = models.CharField(max_length=100, null=True, blank=True)
    classtype = models.ForeignKey(LookUp, on_delete=models.SET_NULL, null=True, blank=True, related_name='class_type')
    # classtype = models.ForeignKey(LookUp, on_delete=models.SET_NULL, null=True, blank=True, related_name='class_type', limit_choices_to={'lookkey': 'BB'})
    classcity = models.CharField(max_length=30, null=True, blank=True)
    deliverymode = models.ForeignKey(LookUp, on_delete=models.SET_NULL, null=True, blank=True, related_name='delivery_mode')
    startdate = models.DateField()
    enddate = models.DateField()
    vanue = models.ForeignKey(Vanue, on_delete=models.CASCADE, null=True, blank=True)
    classstatus = models.ForeignKey(LookUp, on_delete=models.SET_NULL, null=True, blank=True, related_name='class_status')
    # classstatus = models.ForeignKey(LookUp, on_delete=models.SET_NULL, null=True, blank=True, related_name='class_status', limit_choices_to={'lookkey': 'BD'})
    classdesc = models.TextField(null=True, blank=True)
    publishrate = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    bottomrate = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    suggestrate = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    currency = models.ForeignKey(LookUp, on_delete=models.SET_NULL, null=True, blank=True, related_name='currency')
    # currency = models.ForeignKey(LookUp, on_delete=models.SET_NULL, null=True, blank=True, related_name='currency', limit_choices_to={'lookkey': 'CA'})
    studentmax = models.PositiveIntegerField(null=True, blank=True, default=0)
    studentjoin = models.PositiveIntegerField(null=True, blank=True, default=0)
    classpic = models.ForeignKey(Users, on_delete=models.SET_NULL, null=True, blank=True, related_name='userid_classpic')
    registurl = models.URLField(null=True, blank=True)
    certificateurl = models.URLField(null=True, blank=True)
    competenceurl = models.URLField(null=True, blank=True)
    pretask = models.URLField(null=True, blank=True)
    zoomlink = models.URLField(null=True, blank=True)
    classphoto = models.URLField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.classcity:
            self.classcity = self.classcity.lower()
        if self.classdesc:
            self.classdesc = self.classdesc.lower()
        
        if self.classphoto and "drive.google.com" in self.classphoto:
            self.classphoto = self.classphoto.replace("/view?usp=sharing", "")
            self.classphoto = self.classphoto.replace("https://drive.google.com/file/d/", "https://drive.google.com/thumbnail?id=")
        super().save(*args, **kwargs)

    def __str__(self):
        return self.classid
    
    class Meta:
        db_table = 'class'
        managed = True
