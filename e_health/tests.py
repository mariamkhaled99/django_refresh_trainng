

from django.test import TestCase
from .models import TestCustomFielModel

class TestCustomModelFieldTest(TestCase):
	def test_comma_separated_char_field(self):
		"""
		Test that CommaSeparatedCharField stores and retrieves lists of integers correctly.
		"""
		# Create a model instance with a list of integers
		numbers = [1, 2, 3, 4, 5]


		obj = TestCustomFielModel.objects.create(number=10, comma_separated_numbers=numbers)
		print(f"Created object: {obj}")
		print(f"Created value: {obj.comma_separated_numbers}")
		print(f"Type of created value: {type(obj.comma_separated_numbers)}")

		# Retrieve the instance from the database
		retrieved = TestCustomFielModel.objects.get(pk=obj.pk)
		print(f"Retrieved object: {retrieved}")
		print(f"Retrieved value: {retrieved.comma_separated_numbers}")
		print(f"Type of retrieved value: {type(retrieved.comma_separated_numbers)}")

		# The field should return a list of integers
		self.assertEqual(retrieved.comma_separated_numbers, numbers)

		# The field should store as a comma-separated string in the DB
		# (Django's ORM handles conversion, so we test the Python value)

		# Test saving a string directly
		obj2 = TestCustomFielModel.objects.create(number=20, comma_separated_numbers='6,7,8')
		print(f"Created object (string input): {obj2}")
		print(f"Created value (string input): {obj2.comma_separated_numbers}")
		print(f"Type of created value (string input): {type(obj2.comma_separated_numbers)}")

		retrieved2 = TestCustomFielModel.objects.get(pk=obj2.pk)
		print(f"Retrieved object (string input): {retrieved2}")
		print(f"Retrieved value (string input): {retrieved2.comma_separated_numbers}")
		print(f"Type of retrieved value (string input): {type(retrieved2.comma_separated_numbers)}")
		self.assertEqual(retrieved2.comma_separated_numbers, [6, 7, 8])
