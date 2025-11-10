from django.urls import path
from .views import updatedata, getData_Method_1, getData_Method_2, update_note, delete_date

urlpatterns = [
    path('updatedata/', updatedata, name='updatedata'),
    path('getData_Method_1/', getData_Method_1, name='getData_Method_1'),
    path('getData_Method_2/', getData_Method_2, name='getData_MethgetData_Method_2od_1'),
    path('update_note/', update_note, name='update_note'),
    path('delete_date/', delete_date, name='delete_date')
]