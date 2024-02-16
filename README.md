# Rk_kaizntree_challange


## Running this project

To get this project up and running you should start by having Python installed on your computer. Install mysql and create a database(Note: Update Database details in .env file)



Clone or download this repository and open it in your editor of choice. In a terminal, run the following command in the base directory of this project to install the project dependencies

```
pip install -r requirements.txt
```

Then run database migrations((Note: Update Database details in .env file)

```
python manage.py migrate
```

Now you can run the project with this command

```
python manage.py runserver
```
Visit 'http://127.0.0.1:8000/' in your web browser.

To Stop the server

```
Control + C 
```
## Running Testcases

To run tests, use the following command:
```
python manage.py test
```
