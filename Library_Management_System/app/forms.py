from django import forms
from .models import UserInfo,Book
import pandas as pd

class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserInfo
        fields = ['profile_picture']
class UserForm(forms.ModelForm):
    class Meta:
        model = UserInfo
        fields = ['Username', 'email', 'firstname', 'lastname', 'phone', 'profile_picture']
class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'description', 'is_available', 'quantity']

class BookBulkUploadForm(forms.Form):
    file = forms.FileField()

    def clean_file(self):
        uploaded_file = self.cleaned_data['file']
        if not uploaded_file.name.endswith(('.csv', '.xlsx')):
            raise forms.ValidationError("Only CSV or Excel files are allowed.")
        return uploaded_file

    def process_file(self):
        file = self.cleaned_data['file']
        df = None

        if file.name.endswith('.csv'):
            df = pd.read_csv(file)
        elif file.name.endswith('.xlsx'):
            df = pd.read_excel(file)

        books = []
        for _, row in df.iterrows():
            book = Book(
                title=row['title'],
                author=row['author'],
                description=row.get('description', ''),
                is_available=row.get('is_available', True),
                quantity=row.get('quantity', 1)
            )
            books.append(book)

        Book.objects.bulk_create(books)