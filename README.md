[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/IwJY4g24)
# Bank-app

## Author:
name: **Maksim**

surname: **Krauchyk**

group: **2**

## How to start the app

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. (Optional) Start MongoDB using Docker
For API tests with persistence:
```bash
docker-compose -f mongo.yml up -d
```

### 3. Run the Flask API server
```bash
python -m src.api
```

The API will be available at `http://127.0.0.1:5000`

## How to execute tests

### Unit tests
Run all unit tests with coverage:
```bash
python -m coverage run -m pytest tests/unit/
python -m coverage report --include="src/*.py"
python -m coverage html
```

### API tests
1. Start MongoDB (if not running):
```bash
docker-compose -f mongo.yml up -d
```

2. Start the Flask API server in a separate terminal:
```bash
python -m src.api
```

3. Run API tests:
```bash
python -m pytest tests/api/
```

### Performance tests
With Flask API server running:
```bash
python -m pytest tests/perf/
```

### BDD tests (Behave)
With Flask API server running:
```bash
behave
```

### Run all unit tests
```bash
python -m pytest tests/unit/ -v
```