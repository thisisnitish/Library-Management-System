from django.db import models
from django.urls import reverse
from datetime import datetime, timedelta
from django.utils import timezone

# Create your models here.
#Book model
class Book(models.Model):
	book_name = models.CharField(max_length=100, default='')
	author_name = models.CharField(max_length=100, default='')
	book_edition = models.CharField(max_length=100, default='')
	book_publisher = models.CharField(max_length=100, default='')
	isbn_no = models.CharField(max_length=50, default='')
	price = models.DecimalField(max_digits=7, decimal_places=2)
	total_copies = models.PositiveIntegerField(default=0)
	available_copies = models.PositiveIntegerField(default=0)

	genre_choice = (
		('Adventure', 'Adventure'),
		('Autobiography', 'Autobiography'),
		('Art', 'Art'),
		('Business', 'Business'),
		('Biography', 'Biography'),
		('Comic-Book', 'Comic-Book'),
		('Cookbook', 'Cookbook'),
		('Computer-Science', 'Computer-Science'),
		('Encyclopedia', 'Encyclopedia'),
		('Fantasy', 'Fantasy'),
		('Fairytale', 'Fairytale'),
		('History', 'History'),
		('Horror', 'Horror'),
		('Health', 'Health'),
		('Mystery', 'Mystery'),
		('Motivational', 'Motivational'),
		('Mathematics', 'Mathematics'),
		('Poetry', 'Poetry'),
		('Religion', 'Religion'),
		('Romance', 'Romance'),
		('Satire', 'Satire'),
		('Science-Fiction', 'Science-Fiction'),
		('Self-help', 'Self-help'),
		('Science', 'Science'),
		('Thriller', 'Thriller')
		)

	genre = models.CharField(max_length=50, choices=genre_choice)

	stack_choice = (
		('1', '1'),
		('2', '2'),
		('3', '3'),
		('4', '4'),
		('5', '5')
		)

	stack_no = models.CharField(max_length=5, choices=stack_choice)

	shelves_choice = (
		('1', '1'),
		('2', '2'),
		('3', '3'),
		('4', '4'),
		('5', '5'),
		('6', '6'),
		('7', '7'),
		('8', '8')
		)

	shelf_no = models.CharField(max_length=5, choices=shelves_choice)

	row_choice = (
		('1', '1'),
		('2', '2'),
		('3', '3'),
		('4', '4'),
		('5', '5'),
		('6', '6'),
		('7', '7'),
		('8', '8'),
		('9', '9'),
		('10', '10')
		)

	row_no = models.CharField(max_length=5, choices=row_choice)

	
	def __str__(self):
		return self.book_name

	def get_absolute_url(self):
		return reverse('book-detail', kwargs={'pk': self.pk})




#Student model
class Student(models.Model):
	first_name = models.CharField(max_length=50, default='')
	last_name = models.CharField(max_length=50, default='')
	roll_no = models.CharField(max_length=25, default='')

	year_choice = (
		('I', 'I'),
		('II', 'II'),
		('III', 'III'),
		('IV', 'IV'),
		('V', 'V')
		)

	year = models.CharField(max_length=25, default='', choices=year_choice)

	department_choice = (
		('CSE', 'CSE'),
		('ECE', 'ECE'),
		('Electrical Engg', 'Electrical Engg'),
		('Mech Engg', 'Mech Engg'),
		('Civil Engg', 'Civil Engg'),
		('Prod Engg', 'Prod Engg'),
		('Chemical Engg', 'Chemical Engg'),
		('BBA', 'BBA'),
		('MBA', 'MBA'),
		('PHD', 'PHD')
	)

	department = models.CharField(max_length=50, default='', choices=department_choice)
	contact_no = models.CharField(max_length=15, default='')
	email_id = models.EmailField(max_length=50, default='')
	no_of_issued_books = models.PositiveIntegerField(default=0)


	def __str__(self):
		return self.first_name + ' ' + self.last_name

	def get_absolute_url(self):
		return reverse('student-detail', kwargs={'pk': self.pk})



#Issue model
def get_expected_return_date():
	return datetime.today() + timedelta(days=30)

class Issue(models.Model):
	student_name = models.ForeignKey(Student, on_delete=models.CASCADE)
	book = models.ForeignKey(Book, on_delete=models.CASCADE)
	issue_date = models.DateField(default=datetime.today)
	expected_return_date = models.DateField(default=get_expected_return_date)

	def __str__(self):
		return self.book.book_name + ' issued for ' + self.student_name.first_name + ' ' + self.student_name.last_name



#Return book and transaction history model
class ReturnBook(models.Model):
	actual_return_date = models.DateField(default=datetime.today)
	book = models.ForeignKey(Book, on_delete=models.CASCADE)
	student_name = models.ForeignKey(Student, on_delete=models.CASCADE)
	fine_amount = models.PositiveIntegerField(default=0)

	def __str__(self):
		return self.book.book_name + ' is returned by ' + self.student_name.first_name + ' ' + self.student_name.last_name


#actual_return_date
#book_name
#student_name
#fine

