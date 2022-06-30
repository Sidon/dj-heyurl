#! /bin/zsh

# Redesign and boilerplates for tree structure
touch heyurl/routes/metrics_url.py


mkdir -p heyurl/utils
touch heyurl/utils/__init__.py
touch heyurl/utils/cross_helper.py
touch heyurl/utils/data_helper.py
touch heyurl/utils/db_services.py

mkdir -p tests/utils
touch tests/__init__.py
touch tests/conftest.py
touch tests/test_views.py

touch tests/utils/__init.py__
touch tests/utils/test_cross_helper.py
touch tests/utils/test_db_services.py

# creating virtualenv
python3 -m venv --upgrade-deps .fs_env
source .fs_env/bin/activate

# Install requirements
cp ~/fsl/requirements.txt .
pip install -r requirements.txt

# minimal comon pytest config
cp ~/fsl/pytest.ini .

# Recreating database
rm -rf db.sqlite3
python manage.py makemigrations
python manage.py migrate

# Fixtures
cp ~/fsl/sdn_fixture.json heyurl/fixtures/
python manage.py loaddata sdn_fixture.json
