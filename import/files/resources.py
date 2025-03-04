from import_export import resources
from .models import Book

class SampleResource(resources.ModelResource):

    class Meta:
        model = Book
        fields = ('id', "title", "author", "category") # optional, only specified fields gets exported, else all the fields
        export_order = ('id', "title", "author", "category") # optional, describes how order of export



