from django.urls import path
from .views import AdminRegistration, MainPage, LoginUser, Admin, Group, logout_user, ExportExcel


urlpatterns = [
    path('', MainPage.as_view(), name='main'),
    path('group/', Group.as_view(), name='group'),
    path('admin_panel/group/<int:group>', Admin.as_view(), name='admin'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('admin_panel/registration', AdminRegistration.as_view(), name='admin_registration'),
    # path('admin_panel/export', export_excel, name='export_excel'),
    path('admin_panel/export', ExportExcel.as_view(), name='export_excel'),
]