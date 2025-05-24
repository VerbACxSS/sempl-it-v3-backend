# SEMPL-IT V3 Backend
This is the backend of the SEMPL-IT, a web app designed to simplify Italian administrative document using three different fine-tuned LLMs.

Check out the [frontend](https://github.com/VerbACxSS/semp-it-v3-frontend) and the [inference](https://github.com/VerbACxSS/semp-it-v3-inference) of the SEMPL-IT web app.

## Getting started
### Pre-requisites
This web application is developed using FastAPI framework and Hugging Face Transformers library. The following software are required to run the application:
* Python (tested with version 3.12.8)
* Pip (tested with version 23.2.1)

Alternatively, you can use a containerized version by installing:
* Docker (tested on version 28.0.1)

### Configuration
The application can be configured using the following environment variable:
```
PYTHONUNBUFFERED=1
SEMPL_IT_ENDPOINT=...
SEMPL_IT_API_KEY=...
```

### Using `python` and `pip`
Create python virtual environment
```shell
python3 -m venv venv
```
Activate the virtual environment
```shell
source venv/bin/activate   # Linux/macOS
./venv/Scripts/activate    # Windows
```
Install all dependencies in requirements.txt
```shell
pip install -r requirements.txt
```
Start the server
```shell
python -m uvicorn app.app:app --host=0.0.0.0 --port=30010 --log-level=info --workers=2 --timeout-keep-alive=120
```

### Using `docker`
Run the application using `docker compose`
```sh
docker compose up --build -d
```

## Usage
The web application will be running at `http://localhost:30010` by default. 

Make a POST request to the following endpoint to simplify an administrative text:
```sh
curl -X POST "http://localhost:30010/api/v1/simplify/" \
-H "Content-Type: application/json" \
-d '{
    "text": "Nella fattispecie, il presente documento ha lo scopo di fornire indicazioni operative per la gestione del personale."
}'
```

Make a POST request to the following endpoint to analyze an administrative text:
```sh
curl -X POST "http://localhost:30010/api/v1/analyze/text" \
-H "Content-Type: application/json" \
-d '{
    "text": "Nella fattispecie, il presente documento ha lo scopo di fornire indicazioni operative per la gestione del personale."
}'
```

Make a POST request to the following endpoint to compare two administrative text:
```sh
curl -X POST "http://localhost:30010/api/v1/analyze/comparison" \
-H "Content-Type: application/json" \
-d '{
    "text1": "Nella fattispecie, il presente documento ha lo scopo di fornire indicazioni operative per la gestione del personale.",
    "text2": "Nello specifico, questo documento descrive indicazioni operative per la gestione del personale."
}'
```

## Built with
* [FastAPI](https://fastapi.tiangolo)
* [langchain](https://www.langchain.com)
* [italian-ats-evaluator](https://pypi.org/project/italian-ats-evaluator/)

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgements
This contribution is a result of the research conducted within the framework of the PRIN 2020 (Progetti di Rilevante Interesse Nazionale) "VerbACxSS: on analytic verbs, complexity, synthetic verbs, and simplification. For accessibility" (Prot. 2020BJKB9M), funded by the Italian Ministero dell'Università e della Ricerca.