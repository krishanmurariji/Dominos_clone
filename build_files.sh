# Install Python 3.9 and pip
apt-get update && apt-get install -y python3.9 python3.9-venv python3.9-dev

# Install project dependencies
python3.9 -m venv env
source env/bin/activate
pip install -r requirements.txt

# Collect static files
python3.9 manage.py collectstatic

echo "BUILD END"