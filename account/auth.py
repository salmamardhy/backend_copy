from django.contrib.auth.backends import ModelBackend
from .models import Member  # Make sure to import your Member model

class EmailNameBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # Attempt to retrieve the member by email
            member = Member.objects.get(emailmain=username)
            
            # Check the password
            if member.check_password(password):  # Assuming the password is hashed
                return member  # Authentication successful
        except Member.DoesNotExist:
            # Optionally log the failed attempt here for debugging
            return None  # Return None if no matching member is found or password is incorrect
