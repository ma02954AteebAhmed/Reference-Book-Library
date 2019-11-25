from django import forms
import datetime

class student(forms.Form):
	name = forms.CharField(max_length=150)
	major = forms.CharField(max_length=150)
	book_issued = forms.CharField(max_length=150)
	class_of = forms.CharField( max_length=150)
	student_id = forms.CharField(max_length=10) 


class CsvImportForm(forms.Form):
    csv_file = forms.FileField()
	

class criteria_one(forms.Form):
	From = forms.DateField(initial=datetime.datetime.now().date(), required=False)
	To = forms.DateField(initial=datetime.datetime.now().date(), required=False)

class criteria_two(forms.Form):
	From = forms.DateField(initial=datetime.datetime.now().date(), required=False)
	To = forms.DateField(initial=datetime.datetime.now().date(), required=False)
	

	
