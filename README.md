# Pricing assignemt
Setup

1. Within terminal, clone the project in desired directory

```commandline
git clone https://github.com/ristic90/pricing_assignment.git
```

2. Create virtual environment

```commandline
cd pricing_assignment
python -m venv .venv
```

3. Activate virtual environment

```commandline
source .venv/bin/activate
```

4. Install dependencies for local development and testing

```commandline
pip install -r requirements_dev.txt
```

There is also `requirements.txt` which is used by the FastAPI container app.

5. Run tests

```commandline
pytest
```

6. Build and run the images

```commandline
docker compose up -d
```

FastAPI app will be available on localhost:8080.  
The database is initialized with the `init.sql` script to prepopulate it with data.

7. Run `assignment_tests.py` file which contains tests specified in the assignment.

```commandline
python  assignment_tests.py
```

