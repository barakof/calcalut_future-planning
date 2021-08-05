from django.conf.urls import url
from FuturePlanning import views

# SET THE NAMESPACE!
app_name = 'FuturePlanning'

urlpatterns = [
    url(r'^$',views.v_f_index,name='index'),
    url(r'^c_records/$',views.v_f_new_c_record,name='new_record'),
    url(r'^del_c_records/$',views.v_f_del_c_record,name='del_record'),
    url(r'^edit_c_records/$',views.v_f_edit_c_record,name='edit_record'),
    url(r'^edit_c_records/$',views.v_f_edit_c_record_data,name='edit_record_data'),


]
