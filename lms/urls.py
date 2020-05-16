from django.urls import path
from .views import (
	BookListView, 
	BookDetailView, 
	AddBookView,
	UpdateBookView,
	DeleteBookView,
    StudentListView,
    StudentDetailView,
    AddStudentView,
    UpdateStudentView,
    DeleteStudentView,
    CurrentlyIssuedView,
)
from . import views

urlpatterns = [

    #everything about books
    path('', views.home, name='lms-home'),
    #path('library/', views.library, name='lms-library'),
    path('library/', BookListView.as_view(), name='lms-library'),
    path('book/<int:pk>/', BookDetailView.as_view(), name='book-detail'),
    path('book/new/', AddBookView.as_view(), name='add-book'),
    path('book/<int:pk>/update/', UpdateBookView.as_view(), name='book-update'),
    path('book/<int:pk>/delete/', DeleteBookView.as_view(), name='book-delete'),
    path('searchbooks', views.searchBooks, name='search-books'),

    #everything about students
    path('student/', StudentListView.as_view(), name='student-list'),
    path('student/<int:pk>/', StudentDetailView.as_view(), name='student-detail'),
    path('student/new/', AddStudentView.as_view(), name='add-student'),
    path('student/<int:pk>/update/', UpdateStudentView.as_view(), name='student-update'),
    path('student/<int:pk>/delete/', DeleteStudentView.as_view(), name='student-delete'),
    path('searchstudents', views.searchStudents, name='search-students'),

    #evrything about basic functionalites
    path('student/<int:pk>/issuebook/', views.IssueBook, name='issue-books'),
    #path('issuedbooks/', views.currentlyIssued, name='currently-issued'),
    path('issuedbooks/', CurrentlyIssuedView.as_view(), name='currently-issued'),
    path('issuedbooks/<int:pk>/returnbook/', views.returnBook, name='return-book'),
    path('returnedbook/', views.TransactionandReturnBook, name='returned-book'),

]