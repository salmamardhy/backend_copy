from gettext import translation
import random
import string
from django.shortcuts import get_object_or_404, render, redirect  
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth import logout
from django.contrib import messages
from django.urls import reverse
from webapp import settings
from account.forms import MemberForm, MemberDetailForm, RegisForm
from account.models import Member,  Memberdetail, Users
from django.http import Http404
from django.utils.translation import gettext_lazy as _
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from .decorators import member_ownership_required
from django.contrib.auth.views import LoginView
from booking.models import Event

def generate_token(length=8):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def regis(request):
    if request.method == 'POST':
        form = RegisForm(request.POST)
        
        print(form)
        if form.is_valid():
            # print('1valid')
            # Extract form data
            account_name = form.cleaned_data['accountname']
            email = form.cleaned_data['emailmain']
            token = generate_token()  # Generate a random token
            
            # Store necessary data in the session
            request.session['registration_data'] = {
                'accountname': account_name,
                'emailmain': email,
                'password': form.cleaned_data['password'],  # Store the password temporarily
                'ktpname': form.cleaned_data['ktpname'],  # Store KTP name
                'firstname': form.cleaned_data['firstname'],  # Store first name
                'middlename': form.cleaned_data['middlename'],  # Store middle name
                'lastname': form.cleaned_data['lastname'],  # Store last name
            }
            request.session['token'] = token  # Store the token temporarily
            
            # Send the token via email
            send_mail(
                'Account Verification Token',
                f'Your verification token is: {token}',
                'Alpha Seven Force <salmamardhy14@gmail.com>',
                [email],
                fail_silently=False,
            )

            messages.success(request, _('Verification token sent! Please check your email.'))
            return redirect('logintoken')  # Redirect to token input page
    else:
        form = MemberForm()
        print("masalah", form.errors)  
    
    return render(request, 'registration.html', {'form': form})

# class CustomLoginView(LoginView):
# 	template_name = 'login-acc2.html'
# 	redirect_authenticated_user = True

def loginacc(request):
    if request.method == 'POST':
        accountname = request.POST.get('accountname')
        user_type = request.POST.get('user_type')

        if not accountname:  # Check if accountname is empty
            messages.warning(request, _('Account name cannot be empty!'))
            return render(request, 'login-acc.html')  # Render the same page with a message
        
        if user_type == "operator":
            print('USER', user_type)
            try:
                userdata = Users.objects.get(username=accountname)
                print(userdata)
            
                # Generate a new token for the user
                token = generate_token()  # Replace with your token generation function
                
                # Store the account name and token in session
                request.session['accountname'] = userdata.username  # Store the correct account name
                request.session['token'] = token
                request.session['user_type'] = user_type
                
                # Send the token via email
                send_mail(
                    'Account Login Token',
                    f'Your login token is: {token}',
                    'Alpha Seven Force <salmamardhy14@gmail.com>',
                    [userdata.usermail],  # Use the email from the retrieved account
                    fail_silently=False,
                )
                return redirect('logintoken')
        
            except Users.DoesNotExist:
                messages.warning(request, _('Operator does not exist. Please try again!'))

        else:
            try:     
                # Check if the account exists
                accdata = Member.objects.get(accountname=accountname)
                
                # Generate a new token for the user
                token = generate_token()  # Replace with your token generation function
                
                # Store the account name and token in session
                request.session['accountname'] = accdata.accountname  # Store the correct account name
                request.session['token'] = token
                request.session['user_type'] = user_type
                
                # Send the token via email
                send_mail(
                    'Account Login Token',
                    f'Your login token is: {token}',
                    'Alpha Seven Force <salmamardhy14@gmail.com>',
                    [accdata.emailmain],  # Use the email from the retrieved account
                    fail_silently=False,
                )

                messages.success(request, _('Verification token sent! Please check your email.'))
                return redirect('logintoken')  # Redirect to token input page

            except Member.DoesNotExist:
                messages.warning(request, 'Member does not exist. Please try again!')

    return render(request, 'login-acc.html')

def logintoken(request):
    # Get accountname from session
    registration_data = request.session.get('registration_data')
    print("\n\n request.session", request.session.items())

    if registration_data:  # Registration phase
        print('\nregistration_data', registration_data)
        accountname = registration_data.get('accountname') 

        if accountname is None:
            messages.warning(request, _('Account name not found in session!'))
            return redirect('loginacc')
        
        account = Member.objects.filter(accountname=accountname).first()  # Check if account exists
        print(account)

        if request.method == 'POST':
            logintoken = request.POST.get('token')
            session_token = request.session.get('token')
            print('\nlogintoken', logintoken)
            print('session_token',session_token)
            print("")
            
            if account is None:
                if session_token == logintoken:
                    # Create the new Member instance
                    new_member = Member.objects.create(
                        accountname=accountname,
                        emailmain=registration_data.get('emailmain'),
                        password=registration_data.get('password'),  # Save the password
                        ktpname=registration_data.get('ktpname'),  # Save the KTP name
                        firstname=registration_data.get('firstname'),  # Save first name
                        middlename=registration_data.get('middlename'),  # Save middle name
                        lastname=registration_data.get('lastname'),  # Save last name
                    )
                    # Clear session data
                    del request.session['registration_data']
                    del request.session['token']
                    
                    messages.success(request, _('Account created successfully!'))
                    return redirect('editmember', memberid=new_member.memberid)  # Redirect to edit page
                else:
                    print('1account.token', account.token)
                    print('1logintoken', logintoken)
                    messages.warning(request, _('Invalid token! Please enter the correct one.'))
            else:
                print('account', account)
                # If account exists, check the token against the stored value
                print('account.token', session_token)
                print('logintoken', logintoken)
                if session_token == logintoken:
                    account.token = None  # Clear the token after successful verification
                    account.save()
                    messages.success(request, _('Token verified successfully!'))
                    return redirect('editmember', memberid=account.memberid)
                else:
                    messages.warning(request, _('Invalid token! Please enter the correct one.'))
        
    elif request.session.get('user_type') == "operator":
        accountname = request.session.get('accountname') 

        if request.method == 'POST':
            logintoken = request.POST.get('token')
            account = Users.objects.filter(username=accountname).first()  # Safe account retrieval
            print('\nlogintoken', logintoken)
            print('account', account)
            print('request.session.get.token', request.session.get('token'))

            if account and request.session.get('token') == logintoken:
                request.session['accountname'] = account.username
                del request.session['token']
                del request.session['user_type']
                return redirect('showmember')
            else:
                messages.warning(request, _('Invalid token! Please enter the correct one.'))

    else:  # Login phase
        print('\nlogin phase', request)
        accountname = request.session.get('accountname') 

        if request.method == 'POST':
            logintoken = request.POST.get('token')
            account = Member.objects.filter(accountname=accountname).first()  # Safe account retrieval
            print('\nlogintoken', logintoken)
            print('account', account)
            print('request.session.get.token', request.session.get('token'))

            if account and request.session.get('token') == logintoken:
                del request.session['token']
                del request.session['accountname']
                return redirect('editmember', memberid=account.memberid)
            else:
                messages.warning(request, _('Invalid token! Please enter the correct one.'))

    return render(request, 'login-token.html')

def resend_token(request):
    registration_data = request.session.get('registration_data')
    print('\nresend - request.session.items()', request.session.items())

    if registration_data:
        accountname = registration_data.get('accountname')
        emailmain = registration_data.get('emailmain')
        # Generate new token
        new_token = generate_token()  # Implement this function to create a new token
        request.session['token'] = new_token  # Store the new token in session

        # Send the token via email
        send_mail(
                'Account Login Token',
                f'Your login token is: {new_token}',
                'Alpha Seven Force <salmamardhy14@gmail.com>',
                [emailmain],  # Use the email from the retrieved account
                fail_silently=False,
            )  # Implement your email sending logic

        messages.success(request, _('A new token has been sent to your email!'))

    elif request.session.get('user_type') == "member":
        accountname = request.session.get('accountname')
        accdata = Member.objects.get(accountname=accountname)

        # Generate new token
        new_token = generate_token()  # Implement this function to create a new token
        request.session['token'] = new_token  # Store the new token in session

        # Send the token via email
        send_mail(
                'Account Login Token',
                f'Your login token is: {new_token}',
                'Alpha Seven Force <salmamardhy14@gmail.com>',
                [accdata.emailmain],  # Use the email from the retrieved account
                fail_silently=False,
            )  # Implement your email sending logic

        messages.success(request, _('A new token has been sent to your email!'))
        # messages.warning(request, 'Cannot resend token. No registration data found.')

    elif request.session.get('user_type') == "operator":
        accountname = request.session.get('accountname')
        accdata = Users.objects.get(username=accountname)

        # Generate new token
        new_token = generate_token()  # Implement this function to create a new token
        request.session['token'] = new_token  # Store the new token in session

        # Send the token via email
        send_mail(
                'Account Login Token',
                f'Your login token is: {new_token}',
                'Alpha Seven Force <salmamardhy14@gmail.com>',
                [accdata.usermail],  # Use the email from the retrieved account
                fail_silently=False,
            )  # Implement your email sending logic

        messages.success(request, _('A new token has been sent to your email!'))
        # messages.warning(request, 'Cannot resend token. No registration data found.')

    return redirect('logintoken')

def forgot_acc(request):
    if request.method == 'POST':
        mail = request.POST.get('emailmain')
        print('\nmail input', mail)
        
        if not mail:  # Check if accountname is empty
            messages.warning(request, _('Please Enter Your Main Email!'))
            return render(request, 'forgot-acc.html')  # Render the same page with a message
        
        try: 
            # Check if the account exists
            mailmain = Member.objects.get(emailmain=mail) # get memberid
            print('\nmailmain', mailmain)
            print('mailmain.accountname', mailmain.accountname)
            print('')
            
            # Send the token via email
            send_mail(
                'Account Name for Alpha Seven Force Members',
                f'Your account name is: {mailmain.accountname}',
                'Alpha Seven Force <salmamardhy14@gmail.com>',
                [mail],  # Use the email from the retrieved account
                fail_silently=False,
            )

            messages.success(request, _('Account name has been sent! Please check your email.'))
            return redirect('forgot_acc')  # Redirect to token input page

        except Member.DoesNotExist:
            messages.warning(request, _('Account does not exist. Please try again or sign up!'))

    return render(request, 'forgot-acc.html')

def editmember(request, memberid):  # Change employee_id to memberid
    print("editmember request", request.user)
    try:
        employee = Member.objects.get(memberid=memberid)  
    except Member.DoesNotExist:
        raise Http404("Employee not found")
    
    if request.method == 'POST':
        form = MemberForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            return redirect('login/')  # Redirect to the index page after updating
    else:
        form = MemberForm(instance=employee)

    return render(request, 'editmember.html', {'form': form, 'employee': employee})

def logout_view(request):
    print("before logout", request.user)
    logout(request)
    print("after logout", request.user)
    return redirect(reverse('loginacc'))

def memberdetail(request, memberid):
    try:
        employee = Memberdetail.objects.get(memberid=memberid)  
    except Memberdetail.DoesNotExist:
        raise Http404("Employee not found")
    
    if request.method == 'POST':
        form = MemberDetailForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            return redirect('memberdetail', memberid=employee.memberid)
    else:
        form = MemberDetailForm(instance=employee)

    return render(request, 'memberdetail.html', {'form': form, 'employee': employee})

def update(request, memberid):  
    try:
        employee = Member.objects.get(memberid=memberid)  
    except Member.DoesNotExist:
        raise Http404("Member not found")

    if request.method == 'POST':
        form = RegisForm(request.POST, instance=employee)  
        if form.is_valid():  
            form.save()  
            employee = Member.objects.get(memberid=memberid) 
            return redirect('editmember', memberid=employee.memberid)  # Redirect to the index page after updating
        else:
            messages.warning(request, _('Failed to update. Please check your input.'))
    else:
        form = RegisForm(instance=employee)
        
    return render(request, 'editmember.html', {'form': form, 'employee': employee})

# def update(request, memberid):  
#     try:
#         employee = Member.objects.get(memberid=memberid)  
#     except Member.DoesNotExist:
#         raise Http404("Member not found")

#     if request.method == 'POST':
#         print("INIH")
#         form = MemberForm(request.POST, instance=employee)  
#         print(form)
#         if form.is_valid():  
#             print("VALID KOKS")
#             form.save()  
#             # Check the source of the request
#             source = request.POST.get('source', '')
#             print("1source", source)
#             if source == 'operator':
#                 return redirect('editoperator', memberid=employee.memberid)  # Redirect to the operator edit page
#             else:
#                 return redirect('editmember', memberid=employee.memberid)  # Redirect to the member edit page
#         else:
#             messages.warning(request, 'Failed to update. Please check your input.')
#     else:
#         form = MemberForm(instance=employee)
    
#     # Render the appropriate template based on the source
#     source = request.GET.get('source', '')
#     print("2source", source)
#     if source == 'operator':
#         template_name = 'editoperator.html'
#     else:
#         template_name = 'editmember.html'
        
#     return render(request, template_name, {'form': form, 'employee': employee})

def update_member_detail(request, memberid):
    # print(f"Updating member with ID: {memberid}")  # Debugging output
    try:
        employee = Memberdetail.objects.get(memberid__memberid=memberid)
    except Memberdetail.DoesNotExist:
        raise Http404("Member not found")
    
    # print("Join Date:", employee.join_date)

    if request.method == 'POST':
        form = MemberDetailForm(request.POST, instance=employee)
        print("Form Data:", request.POST)
        if form.is_valid():
            form.save()
            # Akses memberid_id secara langsung
            return redirect('memberdetail', memberid=employee.memberid)
        else:
            print("Form Errors:", form.errors)
    else:
        form = MemberDetailForm(instance=employee)

    return render(request, 'memberdetail.html', {'form': form, 'employee': employee})

def showmember(request):
    members = Member.objects.all()
    accountname = request.session.get('accountname')
    users = Users.objects.get(username=accountname)
    print('accountname', accountname)
    return render(request, "operator/showmember.html", {'members': members, 'users': users})

def destroy(request, memberid):
    members = Member.objects.all()  
    member = Member.objects.get(memberid=memberid)
    member.delete()
    return render(request, "operator/showmember.html", {'members': members}) 

def editoperator(request, memberid):
    members = get_object_or_404(Member, pk=memberid)
    try:
        membersdetail = Memberdetail.objects.get(memberid=members)
    except Memberdetail.DoesNotExist:
        membersdetail = None  # Set to None if no detail exists

    context = {
        'members': members,
        'membersdetail': membersdetail,
        # 'form': YourForm(),  # Replace with actual form if needed
    }
    return render(request, 'operator/editoperator.html', context)

def updateoperatorv1(request, memberid):  
    try:
        members = Member.objects.get(memberid=memberid)  
    except Member.DoesNotExist:
        raise Http404("Member not found")

    if request.method == 'POST':
        form = MemberForm(request.POST, instance=members)  
        print(form)
        if form.is_valid():  
            form.save()  
            members = Member.objects.get(memberid=memberid) 
            return redirect('editoperator', memberid=members.memberid)  # Redirect to the index page after updating
        else:
            messages.warning(request, _('Failed to update. Please check your input.'))
    else:
        print(form.errors)
        form = MemberForm(instance=members)
        
    return render(request, 'operator/editoperator.html', {'form': form, 'members': members})


def updateoperatorv2(request, memberid):  
    # print(f"Updating member with ID: {memberid}")  # Debugging output
    try:
        members = Memberdetail.objects.get(memberid__memberid=memberid)
    except Memberdetail.DoesNotExist:
        raise Http404("Member not found")
    
    # print("Join Date:", employee.join_date)

    if request.method == 'POST':
        form = MemberDetailForm(request.POST, instance=members)
        if form.is_valid():
            form.save()
            # Akses memberid_id secara langsung
            return redirect('editoperator', memberid=members.memberid)
        else:
            print("Form Errors:", form.errors)
    else:
        form = MemberDetailForm(instance=members)

    return render(request, 'operator/editoperator.html', {'form': form, 'members': members})

def regisoperator(request):
    if request.method == "POST":
        form = MemberForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('showmember')
        else:
            print("Error in form:", form.errors)  # Print errors for debugging
            return render(request, 'operator/regisoperator.html', {'form': form, 'error': 'Invalid data. Please try again.'})
    else:
        form = MemberForm()
    # messages.success(request, 'Registration successful. You can now log in.')
    return render(request, 'operator/regisoperator.html', {'form': form})

def home(request):
    events = Event.objects.all()
    return render(request, 'home.html', {'events': events})

def loginadmin(request):
    if request.method == 'POST':
        accountname = request.POST.get('accountname')

        if not accountname:  # Check if accountname is empty
            messages.warning(request, _('Account name cannot be empty!'))
            return render(request, 'login-acc.html')  # Render the same page with a message
        
        try:
            userdata = Users.objects.get(username=accountname)
            print(userdata)
        
            # Generate a new token for the user
            token = generate_token()  # Replace with your token generation function
            
            # Store the account name and token in session
            request.session['accountname'] = userdata.username  # Store the correct account name
            request.session['token'] = token
            request.session['user_type'] = 'operator'
            
            # Send the token via email
            send_mail(
                'Account Login Token',
                f'Your login token is: {token}',
                'Alpha Seven Force <salmamardhy14@gmail.com>',
                [userdata.usermail],  # Use the email from the retrieved account
                fail_silently=False,
            )
            return redirect('logintoken')
    
        except Users.DoesNotExist:
            messages.warning(request, _('Operator does not exist. Please try again!'))

    return render(request, 'operator/login-admin.html')

