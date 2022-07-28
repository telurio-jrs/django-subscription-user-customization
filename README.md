# Django Project About User-Customized Area for General Recommendations

Python3.10

## Setup

##### Clone this repository

```bash
git remote add origin <repository_path>
```

##### Create your virtual environment

```bash
python3 -m venv venv
```

##### Activate env with the following command in the project folder

```bash
source venv/bin/activate
```

##### Install requirements

```bash
pip3 install -r requirements.txt
```

Create a .env file to keep all env variables with their respective values. The variables names are located in .env-example

##### Migrate Database

```bash
python manage.py makemigrations
python manage.py migrate
```

##### Load data to Database
Load data using json files "db/fixtures" folder. please check below command for reference.

```bash
python manage.py loaddata user_data.json
```

Run script to load articles table

```bash
python manage.py runscript load
```

##### Login

Launch the app and use the following credentials to login

```bash
python3 manage.py runserver

Username: admin@longevityintime.dev
Password: @dmin1234
```
