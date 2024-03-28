# Install pip for system Python
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python3.9 get-pip.py

# Install Django and other dependencies
python3.9 -m pip install django djangorestframework

# Collect static files
python3.9 manage.py collectstatic --no-input

# Remove temporary file
rm get-pip.py
echo "Static files generated in $(pwd)/staticfiles_build/static"
echo "BUILD END"