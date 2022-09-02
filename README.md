# How to run

## local environment

0. Create `app.env` file and specify database settings in it

    ```bash
    copy app.env.example app.env
    ```

1. Setup virtual environment:

    ```bash
    python -m venv venv
    source venv/bin/activate
    ```

2. Install dev requirements for project
   
    ```bash
    pip install -r requirements/dev.txt
    ```

3. Apply migrations

    ```bash
    python manage.py migrate
    ```

4. Run local server

    ```bash
    python manage.py runserver
    ```

## docker-compose

1. Create `compose.env` file

    ```bash
    copy compose.env.example compose.env
    ```

2. Build docker images

    ```bash
    docker-compose build
    ```

3. Apply migrations:

    ```bash
    docker-compose run application django-admin migrate
    ```

4. Run compose environment
   
    ```bash
    docker-compose up
    ```

5. API now can be accessed via localhost:8000/api/