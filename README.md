# django_refresh_trainng
This is a Django app for refreshing knowledge of Django's main concepts.

## Working with the Command Folder

Inside the `e_health/management/commands/` folder, you will find custom Django management commands. These commands can be executed using the Django `manage.py` script.

### How to Run a Custom Command

1. Open your terminal and navigate to your project directory.
2. Use the following syntax to run a command:

	```powershell
	python manage.py <command_name>
	```

	For example, to run the `aggregate` command:

	```powershell
	python manage.py aggregate
	```

3. Each command may have its own options or arguments. Check the command file for details or use:

	```powershell
	python manage.py <command_name> --help
	```

### Available Commands

The following custom commands are available:

- `aggregate`
- `conditional_expressions`
- `custom_model`
- `insert_data_raw`
- `query_expressions`
- `search`
- `transactions`

Explore each command in the `e_health/management/commands/` directory to learn more about its functionality.
