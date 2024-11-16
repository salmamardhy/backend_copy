from datetime import timezone
from django.shortcuts import render, get_object_or_404, redirect
from .models import DraftBooking, Event
from account.models import Member
from django.http import Http404, HttpResponse
from .forms import DraftBookingForm
from django.contrib import messages

def booking_with_referral(request, event_id, referral_id):
    try:
        event = Event.objects.get(event_id=event_id)
        try:
            referral = Member.objects.get(memberid=referral_id)
        except Member.DoesNotExist:
            referral = None
    except Event.DoesNotExist:
        raise Http404("Event doesn't exist")
        
    if request.method == "POST":
        form = DraftBookingForm(request.POST)
        if form.is_valid():
            draft_booking = form.save(commit=False)
            try:
                member = Member.objects.get(emailmain=form.cleaned_data['email'])
                draft_booking.memberstatus = member
            except Member.DoesNotExist:
                draft_booking.memberstatus = None
            draft_booking.save()
            messages.success(request, 'Booking created successfully! Please check your email for payment instructions.')
            return redirect('/')
    else:
        initial_data = {
            'event': event,
            'referralid': referral,
        }
        form = DraftBookingForm(initial=initial_data)

    context = {
        'form': form,
        'event': event,
        'referral': referral,
    }
    return render(request, 'booking.html', context)

def booking_without_referral(request, event_id):
    try:
        event = Event.objects.get(event_id=event_id)
    except Event.DoesNotExist:
        raise Http404("Event doesn't exist")
        
    if request.method == "POST":
        form = DraftBookingForm(request.POST)
        if form.is_valid():
            draft_booking = form.save(commit=False)
            try:
                member = Member.objects.get(emailmain=form.cleaned_data['email'])
                draft_booking.memberstatus = member
            except Member.DoesNotExist:
                draft_booking.memberstatus = None
            draft_booking.save()
            messages.success(request, 'Booking created successfully! Please check your email for payment instructions.')
            return redirect('booking_event', event_id=event_id)
    else:
        initial_data = {
            'event': event,
            'referralid': None,
        }
        form = DraftBookingForm(initial=initial_data)

    context = {
        'form': form,
        'event': event,
        'referral': None,
    }
    return render(request, 'booking.html', context)

def event(request, event_id):
    event = Event.objects.get(event_id=event_id)
    print("event", event)
    print("event_photo", event.event_photo)
    context = {
        'event': event,
    }
    return render(request, 'event.html', context)
