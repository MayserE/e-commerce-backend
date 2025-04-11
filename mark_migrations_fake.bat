@echo off
echo Marcando migraciones como aplicadas (fake)...

call env\Scripts\activate

python manage.py migrate branch_offices --fake
python manage.py migrate categories --fake
python manage.py migrate products --fake
python manage.py migrate branch_office_products --fake
python manage.py migrate users --fake

echo ✔ Migraciones marcadas como aplicadas con éxito.
pause