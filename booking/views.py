from datetime import timezone
from django.shortcuts import render, get_object_or_404, redirect
from course.models import Class
from account.models import Member
from django.http import Http404, HttpResponse
from .forms import DraftBookingForm
from django.contrib import messages
from django.utils.translation import gettext as _

def booking_with_referral(request, event_id, referral_id):
    print("referral_id", referral_id)
    try:
        event = Class.objects.get(classid=event_id)
        try:
            referral = Member.objects.get(memberid=referral_id)
        except Member.DoesNotExist:
            referral = None
    except Class.DoesNotExist:
        raise Http404(_("Event doesn't exist"))
    
    print("referral", referral)
        
    if request.method == "POST":
        form = DraftBookingForm(request.POST)
        print(form)
        if form.is_valid():
            draft_booking = form.save(commit=False)
            try:
                member = Member.objects.get(emailmain=form.cleaned_data['email'])
                draft_booking.memberstatus = member
            except Member.DoesNotExist:
                draft_booking.memberstatus = None

            draft_booking.eventid = event
            draft_booking.referralid = referral
            draft_booking.save()
            
            messages.success(request, _(f'Thank you for your booking! Please pay the payment before {draft_booking.payment_expires_at.strftime("%d-%m-%y %H:%M")} WIB. Check your email for payment instructions.'))
            return redirect('booking_with_referral', event_id=event_id, referral_id=referral_id)
    else:
        form = DraftBookingForm()
        
    context = {
        'form': form,
        'event': event,
        'referralid': referral,
    }
    print("context", context)
    return render(request, 'booking.html', context)

def booking_without_referral(request, event_id):
    try:
        event = Class.objects.get(classid=event_id)
    except Class.DoesNotExist:
        raise Http404(_("Event doesn't exist"))
        
    if request.method == "POST":
        form = DraftBookingForm(request.POST)
        if form.is_valid():
            draft_booking = form.save(commit=False)
            try:
                member = Member.objects.get(emailmain=form.cleaned_data['email'])
                draft_booking.memberstatus = member
            except Member.DoesNotExist:
                draft_booking.memberstatus = None
            draft_booking.eventid = event
            draft_booking.save()
            
            messages.success(request, _(f'Thank you for your booking! Please pay the payment before {draft_booking.payment_expires_at.strftime("%d-%m-%y %H:%M")} WIB. Check your email for payment instructions.'))
            return redirect('booking_index', event_id=event_id)
    else:
        form = DraftBookingForm()

    context = {
        'form': form,
        'event': event,
        'referral': None,
    }
    return render(request, 'booking.html', context)

def event(request, event_id):
    event = Class.objects.get(classid=event_id)
    print("event", event)
    print("event_photo", event.classphoto)
    context = {
        'event': event,
    }
    return render(request, 'event.html', context)
