dj_shell:
	python manage.py shell

migrate:
	python manage.py migrate

comp_migrate:
	python manage.py makemigrations && python manage.py migrate

create_su:
	python manage.py createsuperuser

run:
	python manage.py runserver