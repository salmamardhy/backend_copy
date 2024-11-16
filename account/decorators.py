from django.http import HttpResponseForbidden
from account.models import Member

def member_ownership_required(view_func):
    def _wrapped_view(request, memberid, *args, **kwargs):
        try:
            # Ambil akun member yang sedang login
            current_user_member = Member.objects.get(accountname=request.user.username)
        except Member.DoesNotExist:
            return HttpResponseForbidden("You need to login")

        # Cek apakah memberid yang diakses adalah milik user yang sedang login
        if str(current_user_member.memberid) != str(memberid):
            print('current_user_member.memberid', current_user_member.memberid)
            return HttpResponseForbidden("You do not have permission to access this page.")
        
        # Jika valid, lanjutkan ke view
        return view_func(request, memberid, *args, **kwargs)

    return _wrapped_view
