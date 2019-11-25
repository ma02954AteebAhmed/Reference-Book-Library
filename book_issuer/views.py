from django.http import HttpResponseRedirect , HttpResponse
from django.shortcuts import render, reverse , redirect
from .forms import forms
from .hu_lib_book_fetcher import *
from .models import *
from datetime import datetime , timedelta
import datetime as dt
import collections
import os

def report_criteria_one(request):
	'''1. Count of all books issued during a particular period / date(s). Date selection slider(s) should be available with From  and To'''
	if request.method == 'POST':
		b = books_issued.objects.all()
		to_str = request.POST['To']
		from_str = request.POST['From']
		To_str = request.POST['To'].split('/')
		From_str = request.POST['From'].split('/')
		
		To = dt.date(int(To_str[2]) , int(To_str[0]), int(To_str[1]))
		From = dt.date(int(From_str[2]) , int(From_str[0]), int(From_str[1]))
		
		books = []

		if To == From:
			on_day = To
			for i in b:
				if i.time_due.date() == on_day:
					books.append(i.bookname)
		else:
			for i in b:
				if i.time_due.date() >= From and i.time_due.date() <= To:
					books.append(i.bookname)

		counter=collections.Counter(books)
		payload = list(zip(counter.keys() , counter.values()))
		return render (request, 'criteria_one_results.html' , {'payload': payload , 'To':to_str , 'From': from_str})

	return render(request , 'criteria_one.html')

def report_criteria_one_download(request):

	b = books_issued.objects.all()
	to_str = request.POST['To']
	from_str = request.POST['From']
	To_str = request.POST['To'].split('/')
	From_str = request.POST['From'].split('/')
	
	To = dt.date(int(To_str[2]) , int(To_str[0]), int(To_str[1]))
	From = dt.date(int(From_str[2]) , int(From_str[0]), int(From_str[1]))
	
	books = []

	if To == From:
		on_day = To
		for i in b:
			if i.time_due.date() == on_day:
				books.append(i.bookname)
	else:
		for i in b:
			if i.time_due.date() >= From and i.time_due.date() <= To:
				books.append(i.bookname)

	counter=collections.Counter(books)
	payload = list(zip(counter.keys() , counter.values()))
	#f_name = to_str + ' - ' +from_str+'.csv'
	f_name = f_name = 'criteria_one ' + From_str[0] +'-'+From_str[1]+'-'+From_str[2] + '  ' + To_str[0] +'-'+To_str[1]+'-'+To_str[2] +'.csv'
	f = open(f_name , 'w')
	f.write('Title,Times Issued \n')
	for title , freq in payload:
		Title = ''
		for i in title:
			if i == ',':
				i = ' '
			Title += i

		f.write(Title+','+str(freq)+'\n')
	f.close()
	f = open(f_name , 'r')
	F = f.read()
	f.close()
	os.remove(f_name)

	response = HttpResponse(F, content_type = 'application/csv')
	response['Content-Disposition'] = 'attachment; filename="' + f_name + '"'
	return response

def report_criteria_two(request):
	'''2. Count of all books issued department/school wise during a particular period/date(s)'''
	if request.method == 'POST':
		to_str = request.POST['To']
		from_str = request.POST['From']

		To_str = request.POST['To'].split('/')
		From_str = request.POST['From'].split('/')
		To = dt.date(int(To_str[2]) , int(To_str[0]), int(To_str[1]))
		From = dt.date(int(From_str[2]) , int(From_str[0]), int(From_str[1]))
		School = request.POST['School']
		b = books_issued.objects.all()
		books = []

		if To == From:
			on_day = To
			for i in b:
				if i.time_due.date() == on_day:
					books.append(i.bookname)
		else:
			for i in b:
				try:
					if i.time_due.date() >= From and i.time_due.date() <= To and student.objects.get(student_id = i.student_id).major == School:
						books.append(i.bookname)
				except:
					pass

		counter=collections.Counter(books)
		payload = list(zip(counter.keys() , counter.values()))
		return render(request , 'criteria_two_results.html', {'payload': payload , 'To':to_str , 'From':from_str, 'School': School})
	else:
		return render(request, 'criteria_two.html')

def report_criteria_two_download(request):

	To_str = request.POST['To'].split('/')
	From_str = request.POST['From'].split('/')
	print(To_str , From_str)
	To = dt.date(int(To_str[2]) , int(To_str[0]), int(To_str[1]))
	From = dt.date(int(From_str[2]) , int(From_str[0]), int(From_str[1]))
	School = request.POST['School']
	b = books_issued.objects.all()
	books = []

	if To == From:
		on_day = To
		for i in b:
			if i.time_due.date() == on_day:
				books.append(i.bookname)
	else:
		for i in b:
			try:
				if i.time_due.date() >= From and i.time_due.date() <= To and student.objects.get(student_id = i.student_id).major == School:
					books.append(i.bookname)
			except:
				pass

	counter=collections.Counter(books)
	payload = list(zip(counter.keys() , counter.values()))
	f_name = f_name = 'criteria_two ' + From_str[0] +'-'+From_str[1]+'-'+From_str[2] + '  ' + To_str[0] +'-'+To_str[1]+'-'+To_str[2] +'.csv'
	f = open(f_name , 'w')
	f.write('Title,Times Issued \n')
	for title , freq in payload:
		Title = ''
		for i in title:
			if i == ',':
				i = ' '
			Title += i

		f.write(Title+','+str(freq)+'\n')
	f.close()
	f = open(f_name , 'r')
	F = f.read()
	f.close()
	os.remove(f_name)

	response = HttpResponse(F, content_type = 'application/csv')
	response['Content-Disposition'] = 'attachment; filename="' + f_name + '"'
	return response

def student_info_view(request):
	if request.method == 'POST':
		form = forms.student(request.POST)
		if form.is_valid():
			return HttpResponseRedirect(reverse('admin'))
	else:
		form = forms.student()
	return render(request , 'student_info.html' ,{'form':form} )


def books_importer(request):
	import pandas as pd
	df = pd.read_csv('C://users//ateeb//desktop//books.csv')
	
	for i in df.iterrows():
		book_name = i[1]['Title']
		barcode = i[1][' Barcode']

		# loading model in python
		model = book(
					 barcode = barcode,
					 name = book_name,
					 status = 'Available'
					)
		model.save()
	return 


def search(request):
	
	books = book.objects.all()
	return render(request, 'search_page.html' , {'book_list': books , 'has_results': True, 'place_holder': 'Search'})


def issue(request):
	if request.method == 'POST':
		print(request.POST)
		barcode = request.POST['barcode']
		student_id = request.POST['student_id']
		obj = book.objects.get(barcode = barcode)
		obj.status = 'Not Available'

		to_beIssued = currently_issued(
									bookname = obj.name,
									barcode = barcode,
									student_id = student_id,
									student_name = student.objects.get(student_id = student_id).firstname,
									time_issued = datetime.now(),
									time_due = datetime.now() + timedelta(hours = 2),
									)
		print(to_beIssued.time_issued, 'dgfjasidghaudsfhasdijsudc')

		#setting time field of book object
		
		obj.time_issued = to_beIssued.time_issued.time().strftime('%I:%M %p')
		obj.time_due = to_beIssued.time_due.time().strftime('%I:%M %p')
		
		#saving model instances
		to_beIssued.save()
		obj.save()

	# loading the books again!
	return redirect('/book_issuer/search/')
	

def return_book(request):
	if request.method == 'POST':
		barcode = request.POST['barcode']

		# changing the status of that specific book in the book table
		obj = book.objects.get(barcode = barcode)
		obj.status = 'Available'
		
		#resetting the time_issued and time_due fields
		obj.time_issued = ""
		obj.time_due = ""

		#saving the book object after making changes
		obj.save()

		# deleting the entry of that from currently_issued, and posting it in books_issued
		obj = currently_issued.objects.get(barcode = barcode)
		
		#creating the books_issued object
		issued_book = books_issued(
									bookname = obj.bookname,
									barcode = obj.barcode,
									student_id = obj.student_id,
									student_name = obj.student_name, 
									time_issued = obj.time_issued,
									time_due = obj.time_due,
									)

		#saving the entry in books_issued table
		issued_book.save()
		obj.delete()

		return redirect('/book_issuer/search')














