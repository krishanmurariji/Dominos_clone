# Install Python 3.9 and pip
# Use the appropriate package manager for the Vercel build environment
apk add --no-cache python3.9 python3.9-dev py3-pip

# Install Django and other dependencies
python3.9 -m pip install django djangorestframework

# Collect static files
python3.9 manage.py collectstatic --no-input

echo "BUILD END"