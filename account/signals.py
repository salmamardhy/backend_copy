from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from account.models import Member, Memberdetail

@receiver(post_save, sender=Member)
def create_or_update_memberdetail(sender, instance, created, **kwargs):
    if created:  # Only create if it's a new Member instance
        if instance.memberstatus == 1:
            Memberdetail.objects.create(
                memberid=instance,  # Store the Member instance, the primary key will be saved automatically
                emailmain=instance.emailmain,
                dob='2000-01-01',  # Example placeholder for date of birth
                ktpnumber='',  # Placeholder KTP number
                join_date=timezone.now().date(),  # Use Django's timezone.now()
                participant=0,  # Default value
                instructor=0,  # Default value
                author=0,  # Default value
                referral=0  # Default value
            )
    else:  # This block handles updates to the Member instance
        try:
            member_detail = Memberdetail.objects.get(memberid=instance)
            # If memberstatus changes to 0, delete the Memberdetail instance
            if instance.memberstatus == 0:
                member_detail.delete()  # Delete the Memberdetail if memberstatus is 0
            else:
                # Update the Memberdetail if necessary
                member_detail.emailmain = instance.emailmain
                member_detail.save()  # Save the changes
        except Memberdetail.DoesNotExist:
            # If the Memberdetail does not exist and memberstatus is 1, create it
            if instance.memberstatus == 1:
                Memberdetail.objects.create(
                    memberid=instance,
                    emailmain=instance.emailmain,
                    dob='2000-01-01',  # Example placeholder
                    ktpnumber='',  # Placeholder
                    join_date=timezone.now().date(),
                    participant=0,
                    instructor=0,
                    author=0,
                    referral=0
                )
