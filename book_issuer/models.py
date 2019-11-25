from django.db import models

MAJOR_CHOICES = (
				('CS' , 'CS'),
				('SDP' , 'SDP'),
				('CND' , 'CND'),
				('EE' , 'EE'),
				('CLS' , 'CLS'),
)

class book(models.Model):
	barcode = models.CharField(max_length = 20)
	name = models.CharField(max_length=500)
	status = models.CharField(max_length = 12)
	time_issued = models.CharField(max_length=12)
	time_due = models.CharField(max_length=12)

	def __str__(self):
		return self.name

class books_issued(models.Model):
	bookname = models.CharField(max_length=1000)
	barcode = models.CharField(max_length = 12)
	student_id = models.CharField(max_length=10)
	student_name = models.CharField(max_length = 250)
	time_issued = models.DateTimeField(auto_now = True)
	time_due = models.DateTimeField(auto_now = True)

	def __str__(self):
		return (self.student_name + ' issued ' + self.bookname)

	class Meta:
		verbose_name_plural = 'books_issued'

class currently_issued(models.Model):
	bookname = models.CharField(max_length=1000)
	barcode = models.CharField(max_length=12)
	student_id = models.CharField(max_length=10)
	student_name = models.CharField(max_length = 250)
	time_issued = models.DateTimeField(auto_now = True)
	time_due = models.DateTimeField(auto_now = True)
	
	class Meta:
		verbose_name_plural = 'currently_issued'

class student(models.Model):
	student_id = models.CharField(max_length= 10)
	surname = models.CharField(max_length=30)
	firstname = models.CharField(max_length=30)
	email = models.CharField(max_length=30)
	mobile = models.CharField(max_length=11)
	#major = models.CharField(max_length=3)
	major = models.CharField(max_length=4, choices=MAJOR_CHOICES, default='CS')
	year = models.CharField(max_length = 4)


	def __str__(self):
		return (self.firstname + ' ' + self.surname + ' , ' + self.student_id)