## Backend

## Setup

1. **Clone the Repository:**

```bash
    git clone https://github.com/AbyvargheseMandapathel/speer-assignment.git
    cd speer-assignment
```
2. **Create and activbate virtualenv**
```bash
    python -m venv env
```

```bash
    .\env\Scripts\activate
```

3. **Install Dependencies**
```bash
    pip install -r requirements.txt
```

4.**Apply Migrations**
```bash
    python manage.py makemigrations
    python manage.py migrate
```

5.**Run the Development Server**
```bash
python manage.py runserver
```

# Postman
You can see the [API documentation](https://documenter.getpostman.com/view/21242095/2s9YsGhYMc) here in Postman and test it out yourself easily :)

# Testing

```bash
python manage.py test
```

# API Rate LIMITING

For Anonymous Users API Rate Limit is 2 per minute and for Authenticated Users API Rate Limit is 5/ Minute

Feel free to change them from settings.py

'DEFAULT_THROTTLE_RATES': {
        'anon': '2/minute',
        'user': '5/minute',
    },
