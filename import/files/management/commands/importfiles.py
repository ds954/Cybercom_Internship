from django.core.management.base import BaseCommand
from files.models import Book  # Import the Book model
import os
from django.conf import settings
import pandas as pd

class Command(BaseCommand):
    """
    Custom Django management command to import book data from a CSV file into the database.
    Usage: python manage.py import_books
    """
    help = "Import book data from a CSV file located in the 'data' directory."

    def handle(self, *args, **options):
        """
        Reads a CSV file and imports book data into the database.
        """
        # Define the directory where the CSV file is located
        data_dir = os.path.join(settings.BASE_DIR, 'data')
        print(f"Data Directory: {data_dir}")

        # Define the full path to the CSV file
        csv_file_path = os.path.join(data_dir, 'books_extended.csv')
        print(f"CSV File Path: {csv_file_path}")


        # Read the CSV file into a Pandas DataFrame
        df = pd.read_csv(csv_file_path)
        print(df)  # Print DataFrame content for debugging

        # Iterate through each row in the DataFrame and create Book objects
        for _, row in df.iterrows():
            Book.objects.create(
                title=row['Title'],  # Extract title from CSV
                author=row['Author'],  # Extract author from CSV
                description=row['Description'],  # Extract description from CSV
                category=row['Category']  # Extract category from CSV
            )

        # Print success message in the console
        self.stdout.write(self.style.SUCCESS("Successfully imported data from CSV!"))
