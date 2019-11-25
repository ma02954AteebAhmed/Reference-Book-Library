from django.urls import path
from . import views

urlpatterns = [
	path('', views.student_info_view, name='student_info_view'),
	path('search/', views.search , name = 'search_page'),
	path('issue/', views.issue , name ='issue_book'),
	path('return_book/', views.return_book , name = 'return_book'),
	path('r1/' , views.report_criteria_one , name= 'criteria_one'),
	path('r2/' , views.report_criteria_two , name= 'criteria_two'),
	path('r1_download/', views.report_criteria_one_download , name = 'criteria_one_download'),
	path('r2_download/', views.report_criteria_two_download , name = 'criteria_two_download'),

]