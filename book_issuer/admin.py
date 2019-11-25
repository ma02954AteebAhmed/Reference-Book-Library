from django.contrib import admin
from .models import book, books_issued, currently_issued , student 
from django import forms
import csv
from django.urls import path , include
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect 

# Register your models here.
from io import TextIOWrapper



class currently_issuedAdmin(admin.ModelAdmin):
	list_display = ('barcode' , 'bookname' , 'student_id' , 'student_name' , 'time_issued' , 'time_due')
	readonly_fields = ('time_issued','time_due' )

class books_issuedAdmin(admin.ModelAdmin):
	list_display = ('barcode' , 'bookname' , 'student_id' , 'student_name' , 'time_issued' , 'time_due')
	readonly_fields = ('time_issued','time_due' )

class bookAdmin(admin.ModelAdmin):
	list_display = ('barcode' , 'name' , 'status')

admin.site.register(currently_issued , currently_issuedAdmin )
admin.site.register(books_issued , books_issuedAdmin )
admin.site.register(book, bookAdmin)



class ExportCsvMixin:
    def export_as_csv(self, request, queryset):

        meta = self.model._meta
        field_names = [field.name for field in meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)

        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names])

        return response

    export_as_csv.short_description = "Export Selected"


class CsvImportForm(forms.Form):
    csv_file = forms.FileField()



@admin.register(student)
class studentAdmin(admin.ModelAdmin, ExportCsvMixin):
	list_display = ('student_id' , 'firstname' , 'surname' , 'major' , 'year' , 'email' , 'mobile'  )
	change_list_template = "student_changelist.html"

	def get_urls(self):
		urls = super().get_urls()
		my_urls = [path('import-csv/', self.import_csv)]
		return my_urls + urls

	def import_csv(self, request):
		if request.method == "POST":
			
			csv_file = TextIOWrapper(request.FILES['csv_file'].file, encoding='utf-8')

			reader = csv.reader(csv_file , delimiter=',')
			for row in reader:
				
				st = student()
				st.surname = row[1]
				st.firstname = row[0]
				st.email = 'fudshfuasd'
				st.mobile = '03212209923'
				st.major = 'CS'
				st.year = '2020'
				st.save()

			self.message_user(request, "Your csv file has been imported")
			return redirect("..")

		form = CsvImportForm()
		payload = {"form": form}
		return render(
		request, "admin/csv_form.html", payload
		)
