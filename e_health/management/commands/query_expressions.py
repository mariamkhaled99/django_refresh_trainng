# https://docs.djangoproject.com/en/5.1/ref/models/expressions/

# from django.db.models import F

# reporter = Reporters.objects.get(name="Tintin")
# reporter.stories_filed = F("stories_filed") + 1
# reporter.save()


"""_summary_
    reporter = Reporters.objects.filter(name="Tintin")
reporter.update(stories_filed=F("stories_filed") + 1)
We can also use update() to increment the field value on multiple objects - which could be very much faster than pulling them all into Python from the database, looping over them, incrementing the field value of each one, and saving each one back to the database:

Reporter.objects.update(stories_filed=F("stories_filed") + 1)
F() therefore can offer performance advantages by:

getting the database, rather than Python, to do work

reducing the number of queries some operations require
    """
    
"""from django.db.models import DateTimeField, ExpressionWrapper, F

Ticket.objects.annotate(
    expires=ExpressionWrapper(
        F("active_at") + F("duration"), output_field=DateTimeField()
    )
)
"""


""">>> car = Company.objects.annotate(built_by=F("manufacturer"))[0]
>>> car.manufacturer
<Manufacturer: Toyota>
>>> car.built_by
3"""


"""Company.objects.update(is_active=~F("is_active"))o swap the activation status of companies"""

""">>> from django.db.models import Avg, F, Max, Min, Window
>>> window = {
...     "partition_by": [F("studio"), F("genre")],
...     "order_by": "released__year",
... }
>>> Movie.objects.annotate(
...     avg_rating=Window(
...         expression=Avg("rating"),
...         **window,
...     ),
...     best=Window(
...         expression=Max("rating"),
...         **window,
...     ),
...     worst=Window(
...         expression=Min("rating"),
...         **window,
...  """