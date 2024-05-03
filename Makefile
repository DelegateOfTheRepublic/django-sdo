dj_shell:
	python manage.py shell

migrate:
	python manage.py migrate

comp_migrate:
	python manage.py makemigrations && python manage.py migrate

revert:
	python manage.py migrate sdo_app ${prev}

create_su:
	python manage.py createsuperuser

run:
	python manage.py runserver