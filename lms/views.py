from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from .models import Book, Student, Issue, ReturnBook
from .forms import IssueForm, ReturnBookForm
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import datetime, date
from django.urls import reverse
from django.views.generic import (
	ListView, 
	DetailView, 
	CreateView,
	UpdateView,
	DeleteView
)

# everything about books start from here
def home(request):
	return render(request, 'lms/home.html', {'title': 'Home'})



def library(request):
	context = {
		'books': Book.objects.all()
	}
	return render(request, 'lms/library.html', context)


def bookTipMsg(request):
	return messages.info(request, 'Click the Book name to know the details about the book')


class BookListView(LoginRequiredMixin, ListView):
	model = Book
	template_name = 'lms/library.html'  #<app>/<model>_<viewtype>.html
	context_object_name = 'books'
	ordering = ['-id']
	paginate_by = 7

#	def get_success_message(self):
#		return 'Tip: Click on the book name in order to get details about the book!!!'


class BookDetailView(LoginRequiredMixin, DetailView):
	model = Book



class AddBookView(LoginRequiredMixin, SuccessMessageMixin, CreateView):     #LoginRequiredMixin
	model = Book
	fields = '__all__'

	def form_valid(self, form):
		return super().form_valid(form)

	def get_success_message(self, cleaned_data):
		return 'Tip: Book is added to the library go and check it out!!!'


class UpdateBookView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):            #LoginRequiredMixin
	model = Book
	fields = '__all__'

	def form_valid(self, form):
		return super().form_valid(form)

	def get_success_message(self, cleaned_data):
		return 'Tip: Book details are updated!!!'


class DeleteBookView(LoginRequiredMixin, DeleteView):            #LoginRequiredMixin
	model = Book
	success_url = '/library/'


@login_required
def searchBooks(request):
	query = request.GET['query']

	#books = Book.objects.all()
	if len(query) > 150 or len(query) == 0:
		books = Book.objects.none()
	else:
		booksbook_name = Book.objects.filter(book_name__icontains = query)
		booksauthor_name = Book.objects.filter(author_name__icontains = query)
		booksgenre = Book.objects.filter(genre__icontains = query)
		books = booksbook_name.union(booksauthor_name, booksgenre)

	if books.count() == 0:
		messages.warning(request, f'No Search Results found please redefine your query by using suggestions!!!')

	params = {
		'books': books,
		'title': 'Search Books',
		'query': query
	}

	return render(request, 'lms/search_books.html', params)

#everything about books end here


#everything about students start from here

class StudentListView(LoginRequiredMixin, ListView):
	model = Student
	template_name = 'lms/students.html'  #<app>/<model>_<viewtype>.html
	context_object_name = 'students'
	ordering = ['-id']
	paginate_by = 8


class StudentDetailView(LoginRequiredMixin, DetailView):
	model = Student


class AddStudentView(LoginRequiredMixin, SuccessMessageMixin, CreateView):     #LoginRequiredMixin
	model = Student
	fields = '__all__'

	def form_valid(self, form):
		return super().form_valid(form)

	def get_success_message(self, cleaned_data):
		return 'Tip: Student data is added to the library!!!'


class UpdateStudentView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):            #LoginRequiredMixin
	model = Student
	fields = '__all__'

	def form_valid(self, form):
		return super().form_valid(form)

	def get_success_message(self, cleaned_data):
		return 'Tip: Student details are updated!!!'


class DeleteStudentView(LoginRequiredMixin, DeleteView):            #LoginRequiredMixin
	model = Student
	success_url = '/student/'


@login_required
def searchStudents(request):
	query = request.GET['query']

	if len(query) > 150 or len(query) == 0:
		students = Student.objects.none()
	else:
		student_fname = Student.objects.filter(first_name__icontains = query)
		student_lname = Student.objects.filter(last_name__icontains = query)
		student_rollno = Student.objects.filter(roll_no__icontains = query)
		student_year = Student.objects.filter(year__icontains = query)
		student_contact = Student.objects.filter(contact_no__icontains = query)
		students = student_fname.union(student_lname, student_rollno, student_year, student_contact)

	if students.count() == 0:
		messages.warning(request, f'No Search Results found please redefine your query by using suggestions!!!')

	params = {
		'students': students,
		'title': 'Search Students',
		'query': query
	}

	return render(request, 'lms/search_students.html', params)

#everything about student ends here


#everything about basic functionality start here

@login_required
def IssueBook(request, pk):

	if request.method == 'POST':
		obj = Student.objects.get(id=pk)
		#print(obj)
		#print(obj.id)
		form = IssueForm(request.POST)
	
		if form.is_valid():
			book = form.cleaned_data['book']
			student = Student.objects.get(id=obj.id)

			bookObj = Book.objects.get(book_name=book)
			
			if student.no_of_issued_books > 10:
				messages.warning(request, 'We cannot issue book to you because you have already more than 10 books issued. So, return anyone of them and get your new book')
				form = IssueForm()
			else:
				#print(student)
				if bookObj.available_copies == 0:
					messages.info(request, 'Sorry!! Not books are available as of now, because there is no available copies here!!!')
					form = IssueForm()
				else:
					form.save()
					books = Book.objects.get(book_name=book)
					#print(books)
					student.no_of_issued_books = student.no_of_issued_books + 1
					#print(books.available_copies)
					books.available_copies = books.available_copies - 1
					student.save()
					books.save()
					#print(books.available_copies)
					messages.success(request, books.book_name + ' is issued to ' + student.first_name)
					return redirect('currently-issued')
	else:
		form = IssueForm()

	context = {
		'form': form,
		'title': 'Issue book',
		'fname': Student.objects.get(id=pk).first_name,
		'lname': Student.objects.get(id=pk).last_name
	}

	return render(request, 'lms/issue_form.html', context)


@login_required
def currentlyIssued(request):

	context = {
		'issued': Issue.objects.all().order_by('-id'),
		'title': 'Issued Books'
	}

	return render(request, 'lms/currently_issued.html', context)


class CurrentlyIssuedView(LoginRequiredMixin, ListView):
	model = Issue
	template_name = 'lms/currently_issued.html'  #<app>/<model>_<viewtype>.html
	context_object_name = 'issued'
	ordering = ['-id']
	paginate_by = 8



def calculate_penalty(issue):
	return (date.today() - issue.expected_return_date).days * 2


@login_required
def returnBook(request, pk):

	issue = Issue.objects.get(id=pk)

	penalty = calculate_penalty(issue)

	book = issue.book
	book.available_copies = book.available_copies + 1
	book.save()

	student = Student.objects.get(first_name=issue.student_name.first_name)
	student.no_of_issued_books = student.no_of_issued_books - 1
	student.save()

	messages(request, 'You have returned the book')
	return redirect('lms-library')


#@login_required
#def returnBook(request, pk):
#	
#	issue = Issue.objects.get(id=pk)
#
#	if request.method == "POST":
# 
#		# note: `instance`  not `initial`
#		form = ReturnBookForm(request.POST, instance=issue)
#		penalty = calculate_penalty(issue)
# 
#		if form.is_valid():
#			form.fine_amount = penalty
#			form.save()
# 
#		#if penalty:
#		#    # this is a different transaction logically
#		#    issue.refresh_from_db()
#		#    issue.fine_amount = penalty
#		#    issue.save()
#
#
#		book = issue.book
#		book.available_copies = book.available_copies + 1
#		book.save()
#
#		student = Student.objects.get(first_name=issue.student_name.first_name)
#
#		student.no_of_issued_books = student.no_of_issued_books - 1
#		student.save()
#
#		#issue.delete()
#		return redirect('returned-book')
#		#return HttpResponseRedirect("returned-book") # or wherever
#	else:
#		# we are here if request.method == "GET"
#		form = ReturnBookForm(instance=issue)
# 
#	context = {
#		'form': form,
#		'obj' : issue,
#		'title': 'Return Book'
#	}
#	return render(request, 'lms/returnbook_form.html', context)


@login_required
def TransactionandReturnBook(request):
	
	context = {
		'returns':  ReturnBook.objects.all().order_by('-id'),
		'title': 'Returned Books and Transaction History'
	}

	return render(request, 'lms/return_and_transaction.html', context)
