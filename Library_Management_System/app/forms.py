from django import forms
from .models import UserInfo,Book,BookCopy,AdminActions
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
    
    def process_file(self,admin_user):
        file = self.cleaned_data['file']
        df = None

        if file.name.endswith('.csv'):
            df = pd.read_csv(file)
        elif file.name.endswith('.xlsx'):
            df = pd.read_excel(file)

        books = []
        book_copies = []
        admin_actions = []

        for _, row in df.iterrows():
            book, created = Book.objects.get_or_create(
                title=row['title'],
                author=row['author'],
                defaults={
                    'description': row.get('description', ''),
                    'is_available': row.get('is_available', True),
                    'quantity': row.get('quantity', 1)
                }
            )

            # If the book already existed, update its quantity and add only the new copies
            if not created:
                existing_copies = book.quantity
                new_copies = row.get('quantity', 1) - existing_copies
                book.quantity += max(new_copies, 0)  # Ensure it doesn't decrease quantity
                book.save()
                admin_actions.append(AdminActions(
                    admin_id=admin_user,
                    action_type="Bulk Update Book",
                    description=f"Updated book: {book.title}, new quantity: {book.quantity}"
                ))

                for copy_number in range(existing_copies + 1, book.quantity + 1):
                    book_copies.append(BookCopy(book=book, copy_number=copy_number))

            else:
                for copy_number in range(1, row.get('quantity', 1) + 1):
                    book_copies.append(BookCopy(book=book, copy_number=copy_number))
                admin_actions.append(AdminActions(
                    admin_id=admin_user,
                    action_type="Bulk Add Book",
                    description=f"Added new book: {book.title}"
                ))    

        BookCopy.objects.bulk_create(book_copies)  # Bulk insert book copies
        AdminActions.objects.bulk_create(admin_actions)  



    # def process_file(self):
    #     file = self.cleaned_data['file']
    #     df = None

    #     if file.name.endswith('.csv'):
    #         df = pd.read_csv(file)
    #     elif file.name.endswith('.xlsx'):
    #         df = pd.read_excel(file)

    #     books = []
    #     for _, row in df.iterrows():
    #         book = Book(
    #             title=row['title'],
    #             author=row['author'],
    #             description=row.get('description', ''),
    #             is_available=row.get('is_available', True),
    #             quantity=row.get('quantity', 1)
    #         )
    #         books.append(book)

    #     Book.objects.bulk_create(books)

    # def process_file(self, admin_user):
    #     file = self.cleaned_data['file']
    #     df = None

    #     if file.name.endswith('.csv'):
    #         df = pd.read_csv(file)
    #     elif file.name.endswith('.xlsx'):
    #         df = pd.read_excel(file)

    #     books = []
    #     book_copies = []
    #     admin_actions = []  # Store admin actions in bulk

    #     for _, row in df.iterrows():
    #         book, created = Book.objects.get_or_create(
    #             title=row['title'],
    #             author=row['author'],
    #             defaults={
    #                 'description': row.get('description', ''),
    #                 'is_available': row.get('is_available', True),
    #                 'quantity': row.get('quantity', 1)
    #             }
    #         )
    #         books.append(book)

    #         if not created:
    #             existing_copies = book.quantity
    #             new_copies = row.get('quantity', 1) - existing_copies
    #             book.quantity += max(new_copies, 0)
    #             book.save()
                
    #             admin_actions.append(AdminActions(
    #                 admin_id=admin_user,
    #                 action_type="Bulk Update Book",
    #                 description=f"Updated book: {book.title}, new quantity: {book.quantity}"
    #             ))

    #             for copy_number in range(existing_copies + 1, book.quantity + 1):
    #                 book_copies.append(BookCopy(book=book, copy_number=copy_number))

    #         else:
    #             admin_actions.append(AdminActions(
    #                 admin_id=admin_user,
    #                 action_type="Bulk Add Book",
    #                 description=f"Added new book: {book.title}"
    #             ))

    #             for copy_number in range(1, row.get('quantity', 1) + 1):
    #                 book_copies.append(BookCopy(book=book, copy_number=copy_number))

    #     BookCopy.objects.bulk_create(book_copies)  
    #     AdminActions.objects.bulk_create(admin_actions)  
