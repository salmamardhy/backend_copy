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

class CourseMaterialForm(forms.ModelForm):
    class Meta:
        model = CourseMaterial
        fields = ['courseid', 'coursename', 'coursedesc', 'creator', 'languages', 'category', 'paidrun', 'freerun', 'folder', 'thumbnailurl', 'coursetype', 'courselab', 'labdesc', 'landingpage', 'marketingtoolkit']

    # Anda dapat mengustomisasi widget form di sini untuk menggunakan komponen Flowbite seperti input teks, select, dll.
    courseid = forms.CharField(widget=forms.TextInput(attrs={'class': 'input input-bordered w-full'}))
    coursename = forms.CharField(widget=forms.TextInput(attrs={'class': 'input input-bordered w-full'}))
    coursedesc = forms.CharField(widget=forms.Textarea(attrs={'class': 'textarea textarea-bordered w-full'}), required=False)
    creator = forms.ModelChoiceField(queryset=Member.objects.all(), widget=forms.Select(attrs={'class': 'select select-bordered w-full'}), required=False)
    languages = forms.ModelChoiceField(queryset=LookUp.objects.filter(lookkey='AA'), widget=forms.Select(attrs={'class': 'select select-bordered w-full'}), required=False)
    # languages = forms.ModelChoiceField(queryset=LookUp.objects.filter(lookkey='AA'), to_field_name='lookname', widget=forms.Select(attrs={'class': 'select select-bordered w-full'}), required=False)
    # to_field_name membuat formnya jd ----- gk muncul value yg udh dipilih sebelumnya
    category = forms.ModelChoiceField(queryset=LookUp.objects.filter(lookkey='BE'), widget=forms.Select(attrs={'class': 'select select-bordered w-full'}), required=False)
    paidrun = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'input input-bordered w-full'}), required=False, initial=0)
    freerun = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'input input-bordered w-full'}), required=False, initial=0)
    folder = forms.URLField(widget=forms.URLInput(attrs={'class': 'input input-bordered w-full'}), required=False)
    coursetype = forms.ModelChoiceField(queryset=LookUp.objects.filter(lookkey='BA'), widget=forms.Select(attrs={'class': 'select select-bordered w-full'}), required=False)
    courselab = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': 'checkbox checkbox-primary'}), required=False)
    thumbnailurl = forms.URLField(widget=forms.URLInput(attrs={'class': 'input input-bordered w-full'}), required=False)
    labdesc = forms.CharField(widget=forms.Textarea(attrs={'class': 'textarea textarea-bordered w-full'}), required=False)
    landingpage = forms.URLField(widget=forms.URLInput(attrs={'class': 'input input-bordered w-full'}), required=False)
    marketingtoolkit = forms.URLField(widget=forms.URLInput(attrs={'class': 'input input-bordered w-full'}), required=False)

# class CourseMaterialForm(forms.ModelForm):
#     class Meta:
#         model = CourseMaterial
#         fields = [
#             'courseid', 'coursename', 'coursedesc', 'creator', 'languages', 'category',
#             'paidrun', 'freerun', 'folder', 'thumbnailurl', 'coursetype', 
#             'courselab', 'labdesc', 'landingpage', 'marketingtoolkit'
#         ]
#         widgets = {
#             'coursename': forms.TextInput(attrs={'placeholder': 'Masukkan nama kursus'}),
#             'coursedesc': forms.Textarea(attrs={'placeholder': 'Masukkan deskripsi kursus', 'rows': 3}),
#             'folder': forms.TextInput(attrs={'placeholder': 'Masukkan jalur folder kursus'}),
#             'thumbnailurl': forms.URLInput(attrs={'placeholder': 'Masukkan URL thumbnail'}),
#             'labdesc': forms.Textarea(attrs={'placeholder': 'Masukkan deskripsi lab', 'rows': 3}),
#             'landingpage': forms.URLInput(attrs={'placeholder': 'Masukkan URL halaman landing'}),
#             'marketingtoolkit': forms.TextInput(attrs={'placeholder': 'Masukkan URL toolkit pemasaran'}),
#         }

#     # Menampilkan pilihan 'languages' dengan filter 'lookkey'='AA'
#     languages = forms.ModelChoiceField(
#         queryset=LookUp.objects.filter(lookkey='AA'),
#         empty_label="Pilih Bahasa",
#         required=False,
#         widget=forms.Select(attrs={'class': 'form-control'})
#     )

#     # Menampilkan pilihan 'category' dengan filter 'lookkey'='BE'
#     category = forms.ModelChoiceField(
#         queryset=LookUp.objects.filter(lookkey='BE'),
#         empty_label="Pilih Kategori",
#         required=False,
#         widget=forms.Select(attrs={'class': 'form-control'})
#     )

#     # Menampilkan pilihan 'coursetype' dengan filter 'lookkey'='BA'
#     coursetype = forms.ModelChoiceField(
#         queryset=LookUp.objects.filter(lookkey='BA'),
#         empty_label="Pilih Tipe Kursus",
#         required=False,
#         widget=forms.Select(attrs={'class': 'form-control'})
#     )

    # Validasi untuk kursus dengan nama kecil
    def clean_coursename(self):
        name = self.cleaned_data['coursename']
        return name.lower()

    # Validasi untuk field 'languages', memastikan hanya pilihan dengan 'lookkey'='AA'
    def clean_languages(self):
        languages = self.cleaned_data.get('languages')
        if isinstance(languages, str):
            try:
                languages = LookUp.objects.get(lookvalue=languages)
            except LookUp.DoesNotExist:
                raise forms.ValidationError("Invalid language selected.")
        return languages

    # Validasi untuk field 'category', memastikan hanya pilihan dengan 'lookkey'='BE'
    def clean_category(self):
        category = self.cleaned_data.get('category')
        if isinstance(category, str):
            try:
                category = LookUp.objects.get(lookvalue=category)
            except LookUp.DoesNotExist:
                raise forms.ValidationError("Invalid category selected.")
        return category

    # Validasi untuk field 'coursetype', memastikan hanya pilihan dengan 'lookkey'='BA'
    def clean_coursetype(self):
        coursetype = self.cleaned_data.get('coursetype')
        if isinstance(coursetype, str):
            try:
                coursetype = LookUp.objects.get(lookvalue=coursetype)
            except LookUp.DoesNotExist:
                raise forms.ValidationError("Invalid course type selected.")
        return coursetype

    # Menyimpan instance jika form valid
    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
        return instance

class VenueForm(forms.ModelForm):
    class Meta:
        model = Vanue
        fields = ['vanuename', 'location', 'vanueurl', 'vanuegmap', 'phone', 'photo']

    vanuename = forms.CharField(widget=forms.TextInput(attrs={'class': 'input input-bordered w-full'}))
    location = forms.CharField(widget=forms.TextInput(attrs={'class': 'input input-bordered w-full'}))
    vanueurl = forms.URLField(widget=forms.URLInput(attrs={'class': 'input input-bordered w-full'}), required=False)
    vanuegmap = forms.URLField(widget=forms.URLInput(attrs={'class': 'input input-bordered w-full'}), required=False)
    phone = forms.CharField(widget=forms.TextInput(attrs={'class': 'input input-bordered w-full'}), required=False)
    photo = forms.URLField(widget=forms.URLInput(attrs={'class': 'input input-bordered w-full'}), required=False)

    def clean_photo(self):
        photo = self.cleaned_data.get('photo')
        if photo and "drive.google.com" in photo:
            photo = photo.replace("/view?usp=sharing", "")
            photo = photo.replace("https://drive.google.com/file/d/", "https://drive.google.com/thumbnail?id=")
        return photo

class CertifiedInstructorForm(forms.ModelForm):
    class Meta:
        model = Certifiedinstructor
        fields = ['courseid', 'instructor', 'description']

    courseid = forms.ModelChoiceField(queryset=CourseMaterial.objects.all(), widget=forms.Select(attrs={'class': 'select select-bordered w-full'}), required=True)
    instructor = forms.CharField(widget=forms.TextInput(attrs={'class': 'input input-bordered w-full'}), required=True)
    description = forms.CharField(widget=forms.TextInput(attrs={'class': 'input input-bordered w-full'}), required=False)

    def clean_description(self):
        description = self.cleaned_data['description']
        return description.lower()

class CertifiedAssistantForm(forms.ModelForm):
    class Meta:
        model = Certifiedassistant
        fields = ['courseid', 'assistant', 'description']

    courseid = forms.ModelChoiceField(queryset=CourseMaterial.objects.all(), widget=forms.Select(attrs={'class': 'select select-bordered w-full'}), required=True)
    assistant = forms.CharField(widget=forms.TextInput(attrs={'class': 'input input-bordered w-full'}), required=True)
    description = forms.CharField(widget=forms.TextInput(attrs={'class': 'input input-bordered w-full'}), required=False)

    def clean_description(self):
        description = self.cleaned_data['description']
        return description.lower()

# from django import forms
# from .models import Class, CourseMaterial, Vanue
# from course.models import LookUp, Certifiedassistant, Certifiedinstructor  # Pastikan LookUp sudah didefinisikan di models.py
# from account.models import Users, Member
# from django.utils.translation import gettext_lazy as _

# class ClassForm(forms.ModelForm):
#     class Meta:
#         model = Class
#         fields = ['classid', 'classname', 'courseid', 'presenter', 'assistant1', 'assistant2', 'assistant3', 'classtype', 
#                   'classcity', 'deliverymode', 'startdate', 'enddate', 'vanue', 'classstatus', 'classdesc', 'publishrate', 
#                   'bottomrate', 'suggestrate', 'currency', 'studentmax', 'studentjoin', 'classpic', 'registurl', 
#                   'certificateurl', 'competenceurl', 'pretask', 'zoomlink', 'classphoto', 'classstatus', 'vanue']

#     # You can customize form widgets here to use Flowbite components like text input, select, etc.
#     classid = forms.CharField(widget=forms.TextInput(attrs={'class': 'input input-bordered w-full'}))
#     classname = forms.CharField(widget=forms.TextInput(attrs={'class': 'input input-bordered w-full'}))
#     courseid = forms.ModelChoiceField(queryset=CourseMaterial.objects.all(), widget=forms.Select(attrs={'class': 'select select-bordered w-full'}), required=False)
#     presenter = forms.ModelChoiceField(queryset=Certifiedinstructor.objects.all(), widget=forms.Select(attrs={'class': 'select select-bordered w-full'}), required=False)
#     assistant1 = forms.ModelChoiceField(queryset=Certifiedassistant.objects.all(), widget=forms.Select(attrs={'class': 'select select-bordered w-full'}), required=False)
#     assistant2 = forms.ModelChoiceField(queryset=Certifiedassistant.objects.all(), widget=forms.Select(attrs={'class': 'select select-bordered w-full'}), required=False)
#     assistant3 = forms.ModelChoiceField(queryset=Certifiedassistant.objects.all(), widget=forms.Select(attrs={'class': 'select select-bordered w-full'}), required=False)
#     classtype = forms.ModelChoiceField(queryset=LookUp.objects.filter(lookkey='BB'), widget=forms.Select(attrs={'class': 'select select-bordered w-full'}), required=False)
#     # classtype = forms.ModelChoiceField(queryset=LookUp.objects.filter(lookkey='BB'), to_field_name='lookname', widget=forms.Select(attrs={'class': 'select select-bordered w-full'}), required=False)
#     vanue = forms.ModelChoiceField(queryset=Vanue.objects.all(), widget=forms.Select(attrs={'class': 'select select-bordered w-full'}), required=False)
#     classcity = forms.CharField(widget=forms.TextInput(attrs={'class': 'input input-bordered w-full'}), required=False)
#     deliverymode = forms.ModelChoiceField(
#         queryset=LookUp.objects.filter(lookkey='BC'),
#         widget=forms.Select(attrs={'class': 'select select-bordered w-full'}),
#         required=False
#     )
#     startdate = forms.DateField(widget=forms.DateInput(attrs={'class': 'input input-bordered w-full', 'type': 'date'}))
#     enddate = forms.DateField(widget=forms.DateInput(attrs={'class': 'input input-bordered w-full', 'type': 'date'}))
#     classdesc = forms.CharField(widget=forms.Textarea(attrs={'class': 'textarea textarea-bordered w-full'}), required=False)
#     publishrate = forms.DecimalField(widget=forms.NumberInput(attrs={'class': 'input input-bordered w-full'}), required=False)
#     bottomrate = forms.DecimalField(widget=forms.NumberInput(attrs={'class': 'input input-bordered w-full'}), required=False)
#     suggestrate = forms.DecimalField(widget=forms.NumberInput(attrs={'class': 'input input-bordered w-full'}), required=False)
#     currency = forms.ModelChoiceField(queryset=LookUp.objects.filter(lookkey='CA'), widget=forms.Select(attrs={'class': 'select select-bordered w-full'}), required=False)
#     studentmax = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'input input-bordered w-full'}), required=False)
#     studentjoin = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'input input-bordered w-full'}), required=False)
#     classstatus = forms.ModelChoiceField(queryset=LookUp.objects.filter(lookkey='BD'), widget=forms.Select(attrs={'class': 'select select-bordered w-full'}), required=False)
#     classpic = forms.ModelChoiceField(queryset=Users.objects.all(), widget=forms.Select(attrs={'class': 'select select-bordered w-full'}), required=False)
#     registurl = forms.URLField(widget=forms.URLInput(attrs={'class': 'input input-bordered w-full'}), required=False)
#     certificateurl = forms.URLField(widget=forms.URLInput(attrs={'class': 'input input-bordered w-full'}), required=False)
#     competenceurl = forms.URLField(widget=forms.URLInput(attrs={'class': 'input input-bordered w-full'}), required=False)
#     pretask = forms.CharField(widget=forms.TextInput(attrs={'class': 'input input-bordered w-full'}), required=False)
#     zoomlink = forms.URLField(widget=forms.URLInput(attrs={'class': 'input input-bordered w-full'}), required=False)
#     classphoto = forms.URLField(widget=forms.URLInput(attrs={'class': 'input input-bordered w-full'}), required=False)

#     def clean_classcity(self):
#         classcity = self.cleaned_data.get('classcity')
#         if classcity:
#             return classcity.lower()
#         return classcity

#     def clean_classdesc(self):
#         classdesc = self.cleaned_data.get('classdesc')
#         if classdesc:
#             return classdesc.lower()
#         return classdesc

#     def clean_classphoto(self):
#         classphoto = self.cleaned_data.get('classphoto')
#         if classphoto and "drive.google.com" in classphoto:
#             classphoto = classphoto.replace("/view?usp=sharing", "")
#             classphoto = classphoto.replace("https://drive.google.com/file/d/", "https://drive.google.com/thumbnail?id=")
#         return classphoto
    
#     def save(self, commit=True):
#         user = super().save(commit=False)
#         if commit:
#             user.save()
#         return user

# class CourseMaterialForm(forms.ModelForm):
#     class Meta:
#         model = CourseMaterial
#         fields = ['courseid', 'coursename', 'coursedesc', 'creator', 'languages', 'category', 'paidrun', 'freerun', 'folder', 'thumbnailurl', 'coursetype', 'courselab', 'labdesc', 'landingpage', 'marketingtoolkit']

#     # Anda dapat mengustomisasi widget form di sini untuk menggunakan komponen Flowbite seperti input teks, select, dll.
#     courseid = forms.CharField(widget=forms.TextInput(attrs={'class': 'input input-bordered w-full'}))
#     coursename = forms.CharField(widget=forms.TextInput(attrs={'class': 'input input-bordered w-full'}))
#     coursedesc = forms.CharField(widget=forms.Textarea(attrs={'class': 'textarea textarea-bordered w-full'}), required=False)
#     creator = forms.ModelChoiceField(queryset=Member.objects.all(), widget=forms.Select(attrs={'class': 'select select-bordered w-full'}), required=False)
#     languages = forms.ModelChoiceField(queryset=LookUp.objects.filter(lookkey='AA'), to_field_name='lookname', widget=forms.Select(attrs={'class': 'select select-bordered w-full'}), required=False)
#     category = forms.ModelChoiceField(queryset=LookUp.objects.filter(lookkey='BE'), to_field_name='lookname', widget=forms.Select(attrs={'class': 'select select-bordered w-full'}), required=False)
#     paidrun = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'input input-bordered w-full'}), required=False)
#     freerun = forms.IntegerField(widget=forms.NumberInput(attrs={'class': 'input input-bordered w-full'}), required=False)
#     folder = forms.CharField(widget=forms.TextInput(attrs={'class': 'input input-bordered w-full'}), required=False)
#     thumbnailurl = forms.URLField(widget=forms.URLInput(attrs={'class': 'input input-bordered w-full'}), required=False)
#     coursetype = forms.ModelChoiceField(queryset=LookUp.objects.filter(lookkey='BA'), to_field_name='lookname', widget=forms.Select(attrs={'class': 'select select-bordered w-full'}), required=False)
#     courselab = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class': 'checkbox checkbox-primary'}), required=False)
#     labdesc = forms.CharField(widget=forms.Textarea(attrs={'class': 'textarea textarea-bordered w-full'}), required=False)
#     landingpage = forms.CharField(widget=forms.TextInput(attrs={'class': 'input input-bordered w-full'}), required=False)
#     marketingtoolkit = forms.CharField(widget=forms.TextInput(attrs={'class': 'input input-bordered w-full'}), required=False)

#     def clean_coursename(self):
#         coursename = self.cleaned_data.get('coursename')
#         if coursename:
#             return coursename.lower()
#         return coursename

#     def save(self, commit=True):
#         user = super().save(commit=False)
#         if commit:
#             user.save()
#         return user

# class VanueForm(forms.ModelForm):
#     class Meta:
#         model = Vanue
#         fields = ['vanuename', 'location', 'vanueurl', 'vanuegmap', 'phone', 'photo']
#         widgets = {
#             'vanuename': forms.TextInput(attrs={'class': 'form-control', 'value': ''}),
#             'location': forms.TextInput(attrs={'class': 'form-control', 'value': ''}),
#             'vanueurl': forms.URLInput(attrs={'class': 'form-control', 'value': ''}),
#             'vanuegmap': forms.URLInput(attrs={'class': 'form-control', 'value': ''}),
#             'phone': forms.TextInput(attrs={'class': 'form-control', 'value': ''}),
#             'photo': forms.URLInput(attrs={'class': 'form-control', 'value': ''})
#         }

#     def clean_photo(self):
#         photo = self.cleaned_data.get('photo')
#         if photo and "drive.google.com" in photo:
#             photo = photo.replace("/view?usp=sharing", "")
#             photo = photo.replace("https://drive.google.com/file/d/", "https://drive.google.com/thumbnail?id=")
#         return photo

