from import_export import resources, fields
from import_export.widgets import BooleanWidget, IntegerWidget
from .models import Book, BookCopy

class BookResource(resources.ModelResource):
    """
    A resource class to handle import/export operations for the Book model,
    with custom widgets for certain fields and logic to synchronize BookCopy instances
    based on quantity changes during import.
    """

    # Define explicit fields to customize the order and how values are parsed
    id = fields.Field(attribute='id', column_name='id')
    title = fields.Field(attribute='title', column_name='title')
    author = fields.Field(attribute='author', column_name='author')
    category = fields.Field(attribute='category', column_name='category')
    description = fields.Field(attribute='description', column_name='description')
    is_available = fields.Field(attribute='is_available', column_name='is_available',
                                widget=BooleanWidget())  # Use Boolean widget for parsing
    quantity = fields.Field(attribute='quantity', column_name='quantity',
                            widget=IntegerWidget())  # Use Integer widget for parsing

    class Meta:
        model = Book
        # Define which fields to import/export
        fields = ('id', 'title', 'author', 'category', 'description', 'is_available', 'quantity')
        export_order = ('id', 'title', 'author', 'category', 'description', 'is_available', 'quantity')

    def after_save_instance(self, instance, new, row_number=None, **kwargs):
        """
        Synchronizes BookCopy instances after a Book is saved during import.

        - If the imported quantity is greater than existing BookCopy entries, new copies are created.
        - If the imported quantity is less, excess BookCopy entries are deleted.
        
        Args:
            instance (Book): The saved book instance.
            new (bool): True if the instance was newly created, False if it was updated.
            row_number (int, optional): The row number in the import file.
            **kwargs: Additional keyword arguments.
        """
        # Count how many copies currently exist for this book
        existing_copies_count = BookCopy.objects.filter(book=instance).count()

        # If quantity increased, create new BookCopy records
        if instance.quantity > existing_copies_count:
            new_copies = [
                BookCopy(book=instance, copy_number=i)
                for i in range(existing_copies_count + 1, instance.quantity + 1)
            ]
            BookCopy.objects.bulk_create(new_copies)

        # If quantity decreased, delete the extra BookCopy records
        elif instance.quantity < existing_copies_count:
            BookCopy.objects.filter(book=instance, copy_number__gt=instance.quantity).delete()