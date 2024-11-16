from django.urls import path
from account import views  
from django.contrib.auth.decorators import login_required

urlpatterns = (
    path('', views.home, name='home'), 
    path('login/', views.loginacc, name='loginacc'), 
    path('login/admin', views.loginadmin, name='loginadmin'), 
    # path('login/', views.CustomLoginView.as_view(), name='login'),
    path('forgotacc/', views.forgot_acc, name='forgot_acc'), 
    path('token/', views.logintoken, name='logintoken'), 
    path('resend_token/', views.resend_token, name='resend_token'), 
    path('regis/', views.regis, name='regis'),   
    path('edit/<str:memberid>/', views.editmember, name='editmember'),
    path('logout/', views.logout_view, name='logout'),
    # path('edit/<str:memberid>/', views.editmember, name='editmember'),
    path('update/<str:memberid>/', views.update, name='update'),
    path('memberdetail/<str:memberid>/', views.memberdetail, name='memberdetail'),
    path('updatememberdetail/<str:memberid>/', views.update_member_detail, name='updatememberdetail'),
    path('edit-operator/<str:memberid>/', views.editoperator, name='editoperator'),
    path('delete/<str:memberid>/', views.destroy, name='destroy'),
    path('updatoperatorv1/<str:memberid>/', views.updateoperatorv1, name='updateoperatorv1'),
    path('updatoperatorv2/<str:memberid>/', views.updateoperatorv2, name='updateoperatorv2'),
    path('regisoperator/', views.regisoperator, name='regisoperator'),
    path('showmember/', views.showmember, name='showmember'),
)