# https://docs.djangoproject.com/en/5.1/ref/models/conditional-expressions/


"""# Update the account_type for each Client from the registration date
>>> Client.objects.update(
...     account_type=Case(
...         When(registered_on__lte=a_year_ago, then=Value(Client.PLATINUM)),
...         When(registered_on__lte=a_month_ago, then=Value(Client.GOLD)),
...         default=Value(Client.REGULAR),
...     ),
... )
>>> Client.objects.values_list("name", "account_type")"""

