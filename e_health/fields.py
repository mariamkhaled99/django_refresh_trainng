from django.db import models
from django.utils.translation import gettext_lazy as _  



class IntegerList:
    """Stores a dynamic list of integers."""

    def __init__(self, *numbers):
        self.numbers = [int(n) for n in numbers]

    def __str__(self):
        return str(self.numbers)

    def __repr__(self):
        return f"IntegerList({', '.join(map(str, self.numbers))})"


class CommaSeparatedCharField(models.Field):
    """
    Custom field to store a list of integers as a comma-separated string.
    """
    
    description = _("Store a list of integers as a comma-separated string.")
    def __init__(self, *args, **kwargs):
        # separator: character used to join/split integers in the string
        self.separator = kwargs.pop('separator', ',')
        # max_length: maximum length of the stored string
        kwargs['max_length'] = kwargs.get('max_length', 255)
        super().__init__(*args, **kwargs)

    def deconstruct(self):
        """
        Returns enough information to recreate the field for migrations.
        Only includes non-default values for cleaner migration files.
        """
        name, path, args, kwargs = super().deconstruct()
        if self.separator != ',':
            kwargs['separator'] = self.separator
        if self.max_length != 255:
            kwargs['max_length'] = self.max_length
        return name, path, args, kwargs

    def db_type(self, connection):
        """
        Returns the database column type for this field.
        """
        return f"char({self.max_length})"

    def get_prep_value(self, value):
        """
        Prepares the value before saving to the database.
        Accepts a list of integers or a comma-separated string, and stores as a string.
        """
        if value is None:
            return ''
        if isinstance(value, list):
            return self.separator.join(str(int(v)) for v in value)
        if isinstance(value, str):
            # Accepts a comma-separated string, ensures it's stored as is
            return value
        return str(value)

    def from_db_value(self, value, expression, connection):
        """
        Converts the database value (comma-separated string) to a Python list of integers.
        """
        if value is None or value == '':
            return []
        return [int(v) for v in str(value).split(self.separator)]

    def to_python(self, value):
        """
        Converts the value to a Python list of integers.
        Accepts a list or a comma-separated string and always returns a list of integers.
        """
        if value is None or value == '':
            return []
        if isinstance(value, list):
            return [int(v) for v in value]
        if isinstance(value, str):
            return [int(v) for v in value.split(self.separator)]
        return [int(value)]
    
    
    def value_to_string(self, obj):
        value = self.value_from_object(obj)
        return self.get_prep_value(value)
    
    
# TODO: create custom field that handle ml models performance saving and loading
        
        