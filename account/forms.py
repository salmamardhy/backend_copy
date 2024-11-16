from django import forms  
from account.models import Member, Memberdetail  # Ensure you import the correct model
from django.forms import ModelForm

class MemberForm(forms.ModelForm): 
    MEMBER_STATUS_CHOICES = [
        (True, 'Active'),
        (False, 'Inactive'),
    ]

    # Use a ChoiceField for memberstatus
    memberstatus = forms.ChoiceField(
        choices=MEMBER_STATUS_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'}),  # Adding the class for styling
        label="Current Member Status"
    )

    class Meta:  
        model = Member 
        fields = ['ktpname', 'emailmain', 'accountname', 'password', 'firstname', 'middlename', 'lastname', 'memberstatus'] 
        widgets = { 
            'ktpname': forms.TextInput(attrs={'class': 'form-control'}),
            'emailmain': forms.EmailInput(attrs={'class': 'form-control'}),
            'accountname': forms.TextInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
            'firstname': forms.TextInput(attrs={'class': 'form-control'}),
            'middlename': forms.TextInput(attrs={'class': 'form-control'}),
            'lastname': forms.TextInput(attrs={'class': 'form-control'}),
            # 'memberstatus' widget is already defined above, so no need to include it here
        }

    # def clean_memberstatus(self):
    #     memberstatus = self.cleaned_data.get('memberstatus')
    #     if memberstatus == 'Yes':
    #         return 1  # Convert 'Yes' to 1
    #     elif memberstatus == 'No':
    #         return 0  # Convert 'No' to 0
    #     raise forms.ValidationError('This field is required.')

    def clean_ktpname(self):
        ktpname = self.cleaned_data.get('ktpname', '').strip()  # Strip whitespace
        if not all(char.isalpha() or char.isspace() for char in ktpname):
            raise forms.ValidationError('KTP name can only contain letters and spaces.')
        return ktpname

    def clean_firstname(self):
        firstname = self.cleaned_data.get('firstname')
        if not firstname.isalpha():
            raise forms.ValidationError('First name can only contain letters.')
        return firstname

    def clean_middlename(self):
        middlename = self.cleaned_data.get('middlename')
        if middlename:
            if not all(char.isalpha() or char.isspace() for char in middlename):
                raise forms.ValidationError('Middle name can only contain letters.')
        else:
            return ''
        return middlename

    def clean_lastname(self):
        lastname = self.cleaned_data.get('lastname')
        if not lastname.isalpha():
            raise forms.ValidationError('Last name can only contain letters.')
        return lastname
    
    def clean_accountname(self):
        accountname = self.cleaned_data.get('accountname')
        if accountname and not accountname.islower():
            raise forms.ValidationError("Account Name must be in lowercase")
        return accountname

class RegisForm(forms.ModelForm): 
    class Meta:  
        model = Member 
        fields = ['ktpname', 'emailmain', 'accountname', 'password', 'firstname', 'middlename', 'lastname', 'memberstatus'] 
        widgets = { 
            'ktpname': forms.TextInput(attrs={'class': 'form-control'}),
            'emailmain': forms.EmailInput(attrs={'class': 'form-control'}),
            'accountname': forms.TextInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
            'firstname': forms.TextInput(attrs={'class': 'form-control'}),
            'middlename': forms.TextInput(attrs={'class': 'form-control'}),
            'lastname': forms.TextInput(attrs={'class': 'form-control'}),
            # 'memberstatus' widget is already defined above, so no need to include it here
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.memberstatus = False  # Set memberstatus to False by default
        if commit:
            user.save()
        return user

    def clean_ktpname(self):
        ktpname = self.cleaned_data.get('ktpname', '').strip()  # Strip whitespace
        if not all(char.isalpha() or char.isspace() for char in ktpname):
            raise forms.ValidationError('KTP name can only contain letters and spaces.')
        return ktpname

    def clean_firstname(self):
        firstname = self.cleaned_data.get('firstname')
        if not firstname.isalpha():
            raise forms.ValidationError('First name can only contain letters.')
        return firstname

    def clean_middlename(self):
        middlename = self.cleaned_data.get('middlename')
        if middlename:
            if not all(char.isalpha() or char.isspace() for char in middlename):
                raise forms.ValidationError('Middle name can only contain letters.')
        else:
            return ''
        return middlename

    def clean_lastname(self):
        lastname = self.cleaned_data.get('lastname')
        if not lastname.isalpha():
            raise forms.ValidationError('Last name can only contain letters.')
        return lastname
    
    def clean_accountname(self):
        accountname = self.cleaned_data.get('accountname')
        if accountname and not accountname.islower():
            raise forms.ValidationError("Account name must be in lowercase")
        return accountname

class MemberDetailForm(forms.ModelForm):
            
    class Meta:
        model = Memberdetail
        fields = ['memberid', 'callsign', 'participant', 'instructor', 'author', 'referral', 'dob', 'ktpnumber',
            'taxid', 'join_date', 'emailmain', 'emailalt', 'whatsapp', 'phone', 'telegram',
            'referralid', 'paidclass', 'freeclass', 'pointtotal', 'pointredeem']
        widgets = { 
            'memberid': forms.TextInput(attrs={'class': 'form-control'}),
            'callsign': forms.TextInput(attrs={'class': 'form-control'}),
            'participant': forms.TextInput(attrs={'class': 'form-control'}),
            'instructor': forms.TextInput(attrs={'class': 'form-control'}),
            'referral': forms.TextInput(attrs={'class': 'form-control'}),
            'dob': forms.DateInput(attrs={'class': 'form-control'}),
            'ktpnumber': forms.TextInput(attrs={'class': 'form-control'}),
            'taxid': forms.TextInput(attrs={'class': 'form-control'}),
            'join_date': forms.DateInput(attrs={'class': 'form-control'}),
            'emailmain': forms.EmailInput(attrs={'class': 'form-control'}),
            'emailalt': forms.EmailInput(attrs={'class': 'form-control'}),
            'whatsapp': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'telegram': forms.TextInput(attrs={'class': 'form-control'}),
            'referralid': forms.TextInput(attrs={'class': 'form-control'}),
            'paidclass': forms.TextInput(attrs={'class': 'form-control'}),
            'freeclass': forms.TextInput(attrs={'class': 'form-control'}),
            'pointtotal': forms.TextInput(attrs={'class': 'form-control'}),
            'pointredeem': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean_emailalt(self):
        emailmain = self.cleaned_data.get('emailmain')
        emailalt = self.cleaned_data.get('emailalt')

        if emailmain and emailalt and emailmain == emailalt:
            raise forms.ValidationError("Email Alternative must be different from Email Main.")
        return emailalt
        
    # def clean(self):
    #     cleaned_data = super().clean()  # Call the parent class's clean method
    #     fields_to_clean = ['callsign', 'emailalt', 'taxid', 'whatsapp']

    #     for field in fields_to_clean:
    #         value = cleaned_data.get(field)  # Access cleaned_data for the field
    #         # Set field value to an empty string if it's None
    #         if value is None or value == '':
    #             self.add_error(field, 'Please fill out this field!')  # Use add_error to set the error message

    #     return cleaned_data  # Return the cleaned_data instead of a single value