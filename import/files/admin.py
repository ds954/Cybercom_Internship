from django.contrib import admin
from django import forms
from django.shortcuts import render
from django.urls import path
from django.http import HttpResponseRedirect
import pandas as pd
from .models import Book

# Form for CSV File Upload in Django Admin
class CSVImportForm(forms.Form):
    """
    Form for uploading a CSV file to import book data into the database.
    """
    csv_file = forms.FileField()  # File upload field

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    """
    Custom Django Admin configuration for the `Book` model.
    Provides a CSV import functionality to add multiple books at once.
    """
    list_display = ("title", "author", "category")  # Fields to display in admin panel
    change_list_template = "admin/book_changelist.html"  # Custom admin template for list view

    def get_urls(self):
        """
        Adds a custom URL for the CSV import feature in the Django Admin panel.
        """
        urls = super().get_urls()  # Get default admin URLs
        custom_urls = [
            path('import-csv/', self.import_csv, name='import_csv'),  # Add custom import route
        ]
        return custom_urls + urls  # Append custom URLs to default URLs

    def import_csv(self, request):
        """
        Handles CSV file upload and imports book data into the database.
        Reads the uploaded CSV file, processes each row, and creates `Book` objects.
        """
        if request.method == "POST":
            csv_file = request.FILES["csv_file"]  # Get uploaded CSV file
            df = pd.read_csv(csv_file)  # Read CSV into a pandas DataFrame

            # Iterate through each row and create Book objects
            for _, row in df.iterrows():
                Book.objects.create(
                    title=row["Title"],  # Extract title from CSV
                    author=row["Author"],  # Extract author from CSV
                    description=row["Description"],  # Extract description from CSV
                    category=row["Category"]  # Extract category from CSV
                )

            self.message_user(request, "CSV file imported successfully!")  # Show success message
            return HttpResponseRedirect("../")  # Redirect back to admin page

        # Render file upload form if not a POST request
        form = CSVImportForm()
        return render(request, "admin/csv_form.html", {"form": form})  