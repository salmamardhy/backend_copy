from datetime import timezone
from django.shortcuts import render, get_object_or_404, redirect
from course.models import Class, LookUp, CourseMaterial
from account.models import Member
from django.http import Http404, HttpResponse
from .forms import ClassForm, CourseMaterialForm, VenueForm, CertifiedAssistantForm, CertifiedInstructorForm
from django.contrib import messages
from django.utils.translation import gettext as _


def addclass(request):
    if request.method == "POST":
        form = ClassForm(request.POST)
        print("1.form", form)
        print("1.1 form.classid", form.cleaned_data['classid'])
        if form.is_valid():
            try:
                classid_input = form.cleaned_data['classid']  # Mengakses classid yang sudah divalidasi

                if len(classid_input) < 4:
                    seq_number = Class.objects.filter(classid__istartswith=classid_input).count()

                    print("classid_input seq_number", seq_number)
                    seq_number = seq_number + 1 if seq_number > 0 else 1
                    classid = classid_input.upper() + form.cleaned_data['startdate'].strftime("%y%m") + f"{seq_number:02d}"

                    if Class.objects.filter(classid=classid).exists():
                        seq_number = seq_number + 1
                        classid = classid_input.upper() + form.cleaned_data['startdate'].strftime("%y%m") + f"{seq_number:02d}"

                    form.instance.classid = classid
                    print("classid", classid)
                    print("form.cleaned_data['classid']", form.cleaned_data['classid'])

                if len(classid_input) > 3:
                    messages.error(request, _('Please Input only three initial for courseid'))
                    return render(request, 'addclass.html', {'form': form})

                if (form.cleaned_data['assistant1'] is not None and form.cleaned_data['assistant1'] == form.cleaned_data['assistant2']) or \
                   (form.cleaned_data['assistant2'] is not None and form.cleaned_data['assistant2'] == form.cleaned_data['assistant3']) or \
                   (form.cleaned_data['assistant1'] is not None and form.cleaned_data['assistant1'] == form.cleaned_data['assistant3']):
                    messages.error(request, _('Assistant 1, 2, 3 must be different person!'))
                    return render(request, 'addclass.html', {'form': form})

                print("2.form", form)
                form.save()
                print("2.1 Saved classid", form.cleaned_data['classid'])
                return redirect('showmember')

            except Exception as error_addclass:
                print("Error saving form:", str(error_addclass))
                return render(request, 'addclass.html', {
                    'form': form, 
                    'error': _('Failed to add class')
                })
        else:
            print("Error in form:", form.errors)  # Print errors for debugging
            return render(request, 'addclass.html', {'form': form, 'error': _('Invalid data. Please try again.')})
    else:
        form = ClassForm()
    return render(request, 'addclass.html', {'form': form})

def addcourse(request):
    if request.method == "POST":
        form = CourseMaterialForm(request.POST)
        print("1. form", form)
        if form.is_valid():
            try:
                # Accessing the form data
                courseid_input = form.cleaned_data['courseid']  # Access the courseid
                print("courseid_input", courseid_input)

                # Validate and handle the languages_id field (similar to category, coursetype)
                languages = form.cleaned_data.get('languages_id')
                if isinstance(languages, str):  # Check if it's a string
                    try:
                        # Try to fetch the LookUp object for the languages_id
                        languages = LookUp.objects.get(lookkey=languages)
                        print(f"Found LookUp record for languages: {languages}")
                    except LookUp.DoesNotExist:
                        raise ValueError(_('Invalid language "%s" provided.') % languages)
                
                # Optional: Validate other string-based fields (category, coursetype)
                category = form.cleaned_data.get('category')  # Example for category
                if isinstance(category, str):
                    try:
                        category = LookUp.objects.get(lookkey=category)
                        print(f"Found LookUp record for category: {category}")
                    except LookUp.DoesNotExist:
                        raise ValueError(_('Invalid category "%s" provided.') % category)
                
                coursetype = form.cleaned_data.get('coursetype')  # Example for coursetype
                if isinstance(coursetype, str):
                    try:
                        coursetype = LookUp.objects.get(lookkey=coursetype)
                        print(f"Found LookUp record for coursetype: {coursetype}")
                    except LookUp.DoesNotExist:
                        raise ValueError(_('Invalid course type "%s" provided.') % coursetype)

                # If the LookUp fields are valid, assign them to the form instance
                form.instance.languages_id = languages
                form.instance.category = category
                form.instance.coursetype = coursetype

                # Handle the courseid generation logic
                if len(courseid_input) < 5:
                    seq_number = CourseMaterial.objects.filter(courseid__istartswith=courseid_input).count()
                    print("courseid_input seq_number", seq_number)
                    seq_number = seq_number + 1 if seq_number > 0 else 1
                    courseid = courseid_input.upper() + f"{seq_number:03d}"

                    if CourseMaterial.objects.filter(courseid=courseid).exists():
                        seq_number += 1
                        courseid = courseid_input.upper() + f"{seq_number:03d}"

                    form.instance.courseid = courseid
                    print("courseid", courseid)

                # Save the CourseMaterial form instance
                form.save()
                print("2.1 Saved courseid", form.cleaned_data['courseid'])

                messages.success(request, _("Course successfully added!"))
                return redirect('showmember')  # Adjust the redirection as needed
            except ValueError as ve:
                # If validation fails, show the error message
                messages.error(request, str(ve))
                return render(request, 'addcourse.html', {'form': form, 'error': str(ve)})
            except Exception as e:
                print("Error saving form:", str(e))
                messages.error(request, _("Failed to add course"))
                return render(request, 'addcoursematerial.html', {'form': form, 'error': _('Failed to add course')})
        else:
            print("Error in form:", form.errors)  # Print errors for debugging
            return render(request, 'addcoursematerial.html', {'form': form, 'error': _('Invalid data. Please try again.')})
    else:
        form = CourseMaterialForm()
    return render(request, 'addcoursematerial.html', {'form': form})

def addvenue(request):
    if request.method == "POST":
        form = VenueForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, _("Venue successfully added!"))
                return redirect('showmember')
            
            except Exception as e:
                print("Error saving form:", str(e))
                messages.error(request, _("Failed to add course"))
                return render(request, 'addvenue.html', {'form': form, 'error': _('Failed to add course')})
        else:
            print("Error in form:", form.errors)  # Print errors for debugging
            return render(request, 'addvenue.html', {'form': form, 'error': _('Invalid data. Please try again.')})
    else:
        form = VenueForm()
    return render(request, 'addvenue.html', {'form': form})

def addcertif_assistant(request):
    title = _('Assistant')
    if request.method == "POST":
        form = CertifiedAssistantForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, _("Certificate Assistant successfully added!"))
                return redirect('showmember')
            
            except Exception as e:
                print("Error saving form:", str(e))
                messages.error(request, _("Failed to add course"))
                return render(request, 'addcertificate.html', {'form': form, 'error': _('Failed to add course')})
        else:
            print("Error in form:", form.errors)  # Print errors for debugging
            return render(request, 'addcertificate.html', {'form': form, 'error': _('Invalid data. Please try again.')})
    else:
        form = CertifiedAssistantForm()
    return render(request, 'addcertificate.html', {'form': form, 'title': title})

def addcertif_instructor(request):
    title = _("Instructor")
    if request.method == "POST":
        form = CertifiedInstructorForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, _("Certificate instructor successfully added!"))
                return redirect('showmember')
            
            except Exception as e:
                print("Error saving form:", str(e))
                messages.error(request, _("Failed to add course"))
                return render(request, 'addcertificate.html', {'form': form, 'error': _('Failed to add course')})
        else:
            print("Error in form:", form.errors)  # Print errors for debugging
            return render(request, 'addcertificate.html', {'form': form, 'error': _('Invalid data. Please try again.')})
    else:
        form = CertifiedInstructorForm()
    return render(request, 'addcertificate.html', {'form': form, 'title': title})

# def addclass(request):
#     if request.method == "POST"
#         form = ClassForm(request.POST)
#         if form.is_valid():
#             try:
#                 # Validate delivery mode exists in LookUp table
#                 # delivery_mode = form.cleaned_data.get('deliverymode')
#                 # if delivery_mode and not LookUp.objects.filter(lookkey=delivery_mode.lookkey).exists():
#                 #     raise ValueError("Invalid delivery mode selected")
#                 # print("delivery_mode", LookUp.objects.filter(lookkey=delivery_mode.lookkey).exists())
                
#                 form.save()
#                 print(form)
#                 return redirect('showmember')
            
#             except Exception as e:
#                 print("Error saving form:", str(e))
#                 print("Form errors:", form)
#                 return render(request, 'addclass.html', {
#                     'form': form, 
#                     'error': 'Failed to save class. Please check that the class status is valid.'
#                 })
#         else:
#             print("Error in form:", form.errors)  # Print errors for debugging
#             return render(request, 'addclass.html', {'form': form, 'error': 'Invalid data. Please try again.'})
#     else:
#         form = ClassForm()
#     return render(request, 'addclass.html', {'form': form})
