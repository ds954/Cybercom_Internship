from import_export import resources, fields
from import_export.widgets import BooleanWidget, IntegerWidget
from .models import Book,BookCopy

class BookResource(resources.ModelResource):
    # Explicitly declare fields if you want to control order or widgets
    id = fields.Field(attribute='id', column_name='id')
    title = fields.Field(attribute='title', column_name='title')
    author = fields.Field(attribute='author', column_name='author')
    category = fields.Field(attribute='category', column_name='category')
    description = fields.Field(attribute='description', column_name='description')
    is_available = fields.Field(attribute='is_available', column_name='is_available',
                                widget=BooleanWidget())
    quantity = fields.Field(attribute='quantity', column_name='quantity',
                            widget=IntegerWidget())

    class Meta:
        model = Book
        # import_id_fields = ('id',)  # optional if you want to update by ID
        fields = ('id', 'title', 'author', 'category', 'description', 'is_available', 'quantity')
        export_order = ('id', 'title', 'author', 'category', 'description', 'is_available', 'quantity')

    def after_save_instance(self, instance, new, row_number=None, **kwargs):
        existing_copies_count = BookCopy.objects.filter(book=instance).count()

        if instance.quantity > existing_copies_count:
            new_copies = [
                BookCopy(book=instance, copy_number=i)
                for i in range(existing_copies_count + 1, instance.quantity + 1)
            ]
            BookCopy.objects.bulk_create(new_copies)

        elif instance.quantity < existing_copies_count:
            BookCopy.objects.filter(book=instance, copy_number__gt=instance.quantity).delete()