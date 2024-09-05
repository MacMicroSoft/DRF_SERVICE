# Running the DRF Project


## Option to Run Either via Docker or Manually

## Manual Setup

### Installation Steps (**Manual Setup**)###

1. Clone the repository to your local machine:
   git clone https://github.com/MacMicroSoft/DRF_SERVICE.git

2. Create a virtual environment:
   - For Windows:
     python -m venv venv
   - For Linux/macOS:
     python3 -m venv venv

3. Activate the virtual environment:
   - For Windows:
     venv\Scripts\activate
   - For Linux/macOS:
     source venv/bin/activate

4. Install the required dependencies:
 ```plaintext
   pip install -r requirements.txt
```
6. Create a .env file
Into .env file write :
```plaintext
SECRET_KEY=your_secret_key
DEBUG=True
DB_NAME=your_db_name
TEST_DB_NAME=your_db_test_name
DB_USER=your_user
DB_PASSWORD=your_pass
DB_HOST=your_host
DB_PORT=your_port
```

6. Run migrations
```plaintext
python manage.py makemigrations
python manage.py migrate
```
8. Run application
```plaintext
python manage.py runserver
```

### Installation Steps (**Docker**)###
 

1. Create .env file with that data:
```plaintext
SECRET_KEY=your_secret_key
DEBUG=True
DB_NAME=postgres
TEST_DB_NAME=test_rest
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
```
2. Run command
```plaintext
docker-compose up -d db
```

4. Run command
```plaintext
docker compose build
```

5. Run command
```plaintext
docker compose up
```

# Start work with app

## This app has Swagger UI for easier testing.

1. **Registering a User:**
   To get started, register a user by running:
   python manage.py createsuperuser

2. **Logging in to Admin Panel:**
   After registering, log in to the admin panel:
   http://127.0.0.1:8000/admin

3. **Using Swagger UI:**
   This app provides Swagger UI for easy interaction. Access it at:
   http://127.0.0.1:8000/api/schema/redoc/
   or
   http://127.0.0.1:8000/api/schema/swagger-ui/


