from django import forms
from .models import Class, CourseMaterial, Vanue, LookUp
from course.models import LookUp, Certifiedassistant, Certifiedinstructor  # Pastikan LookUp sudah didefinisikan di models.py
from account.models import Users, Member
from django.utils.translation import gettext_lazy as _

class ClassForm(forms.ModelForm):
    class Meta:
        model = Class
        fields = ['classid', 'classname', 'courseid', 'presenter', 'assistant1', 'assistant2', 'assistant3', 'classtype', 
                  'classcity', 'deliverymode', 'startdate', 'enddate', 'vanue', 'classstatus', 'classdesc', 'publishrate', 
                  'bottomrate', 'suggestrate', 'currency', 'studentmax', 'studentjoin', 'classpic', 'registurl', 
                  'certificateurl', 'competenceurl', 'pretask', 'zoomlink', 'classphoto', 'classstatus', 'vanue']

    # You can customize form widgets here to use Flowbite components like text input, select, etc.
    classid = forms.CharField(widget=forms.TextInput(attrs={'class': 'input input-bordered w-full'}))
    classname = forms.CharField(widget=forms.TextInput(attrs={'class': 'input input-bordered w-full'}))
    courseid = forms.ModelChoiceField(queryset=CourseMaterial.objects.all(), widget=forms.Select(attrs={'class': 'select select-bordered w-full'}), required=False)
    presenter = forms.ModelChoiceField(queryset=Certifiedinstructor.objects.all(), widget=forms.Select(attrs={'class': 'select select-bordered w-full'}), required=False)
    assistant1 = forms.ModelChoiceField(queryset=Certifiedassistant.objects.all(), widget=forms.Select(attrs={'class': 'select select-bordered w-full'}), required=False)
    assistant2 = forms.ModelChoiceField(queryset=Certifiedassistant.objects.all(), widget=forms.Select(attrs={'class': 'select select-bordered w-full'}), required=False)
    assistant3 = forms.ModelChoiceField(queryset=Certifiedassistant.objects.all(), widget=forms.Select(attrs={'class': 'select select-bordered w-full'}), required=False)
    classtype = forms.ModelChoiceField(queryset=LookUp.objects.filter(lookkey='BB'), widget=forms.Select(attrs={'class': 'select select-bordered w-full'}), required=False)
    # classtype = forms.ModelChoiceField(queryset=LookUp.objects.filter(lookkey='BB'), to_field_name='lookname', widget=forms.Select(attrs={'class': 'select select-bordered w-full'}), required=False)
    vanue = forms.ModelChoiceField(queryset=Vanue.objects.all(), widget=forms.Select(attrs={'class': 'select select-bordered w-full'}), required=False)
    classcity = forms.CharField(widget=forms.TextInput(attrs={'class': 'input input-bordered w-full'}), required=False)
    deliverymode = forms.ModelChoiceField(
        queryset=LookUp.objects.filter(lookkey='BC'),
        widget=forms.Select(attrs={'class': 'select select-bordered w-full'}),
        required=False
    )
    startdate = forms.DateField(widget=forms.DateInput(attrs={'class': 'input input-bordered w-full', 'type': 'date'}))
    enddate = forms.DateField(widget=forms.DateInput(attrs={'class': 'input input-bordered w-full', 'type': 'date'}))
    classdesc = forms.CharField(widget=forms.Textarea(attrs={'class': 'textarea textarea-bordered w-full'}), required=False)
    publishrate = forms.DecimalField(widget=forms.NumberInput(attrs={'class': 'input input-bordered w-full'}), required=False)
    bottomrate = forms.DecimalField(widget=forms.NumberInput(attrs={'class': 'input input-bordered w-full'}), required=False)
    suggestrate = forms.DecimalField(widget=forms.NumberInput(attrs={'class': 'input input-bordered w-full'}), required=False)
    currency = forms.ModelChoiceField(queryset=LookUp.objects.filter(lookkey='CA'), widget=forms.Select(attrs={'class': 'select select-bordered w-full'}), required=False)
    studentmax = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'input input-bordered w-full'}), required=False)
    studentjoin = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'input input-bordered w-full'}), required=False)
    classstatus = forms.ModelChoiceField(queryset=LookUp.objects.filter(lookkey='BD'), widget=forms.Select(attrs={'class': 'select select-bordered w-full'}), required=False)
    classpic = forms.ModelChoiceField(queryset=Users.objects.all(), widget=forms.Select(attrs={'class': 'select select-bordered w-full'}), required=False)
    registurl = forms.URLField(widget=forms.URLInput(attrs={'class': 'input input-bordered w-full'}), required=False)
    certificateurl = forms.URLField(widget=forms.URLInput(attrs={'class': 'input input-bordered w-full'}), required=False)
    competenceurl = forms.URLField(widget=forms.URLInput(attrs={'class': 'input input-bordered w-full'}), required=False)
    pretask = forms.CharField(widget=forms.TextInput(attrs={'class': 'input input-bordered w-full'}), required=False)
    zoomlink = forms.URLField(widget=forms.URLInput(attrs={'class': 'input input-bordered w-full'}), required=False)
    classphoto = forms.URLField(widget=forms.URLInput(attrs={'class': 'input input-bordered w-full'}), required=False)

    def clean_classcity(self):
        classcity = self.cleaned_data.get('classcity')
        if classcity:
            return classcity.lower()
        return classcity

    def clean_classdesc(self):
        classdesc = self.cleaned_data.get('classdesc')
        if classdesc:
            return classdesc.lower()
        return classdesc

    def clean_classphoto(self):
        classphoto = self.cleaned_data.get('classphoto')
        if classphoto and "drive.google.com" in classphoto:
            classphoto = classphoto.replace("/view?usp=sharing", "")
            classphoto = classphoto.replace("https://drive.google.com/file/d/", "https://drive.google.com/thumbnail?id=")
        return classphoto
    
    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
        return user

class VanueForm(forms.ModelForm):
    class Meta:
        model = Vanue
        fields = ['vanuename', 'location', 'vanueurl', 'vanuegmap', 'phone', 'photo']
        widgets = {
            'vanuename': forms.TextInput(attrs={'class': 'form-control', 'value': ''}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'value': ''}),
            'vanueurl': forms.URLInput(attrs={'class': 'form-control', 'value': ''}),
            'vanuegmap': forms.URLInput(attrs={'class': 'form-control', 'value': ''}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'value': ''}),
            'photo': forms.URLInput(attrs={'class': 'form-control', 'value': ''})
        }

    def clean_photo(self):
        photo = self.cleaned_data.get('photo')
        if photo and "drive.google.com" in photo:
            photo = photo.replace("/view?usp=sharing", "")
            photo = photo.replace("https://drive.google.com/file/d/", "https://drive.google.com/thumbnail?id=")
        return photo
