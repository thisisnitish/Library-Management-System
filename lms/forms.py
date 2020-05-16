from django import forms
from .models import Issue, ReturnBook

class IssueForm(forms.ModelForm):
    class Meta:
        model = Issue
        fields = [
            'student_name', 
            'book'
        ]


class ReturnBookForm(forms.ModelForm):
    class Meta:
        model = ReturnBook
        fields = [
            'actual_return_date',
            'book',
            'student_name',
        ]