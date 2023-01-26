# Fact Checking Backend

This is the repository for the backend service for the [Fact Checking Frontend](https://gitlab.lrz.de/fact-checking-tool/fact-checking-frontend-2) of the Fact Checking Tool. The Fact Checking Tool is an app that supports document search, evidence retrieval, and realtime claim verification. It employs natural language processing to create a standard pipeline for automated fact checking.

## Features

- Document search using the Google API, Bing API and Elasticsearch
- Utilizes Farm-Haystack to create automated pipeline for various tasks
- Utilizes pretrained models from Hugging face for natural language processing

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

- Python >= 3.8.10
- Django >= 4.1.3
- Poetry >= 1.2
- Farm-Haystack >= 1.11.1
- transformers >= 4.25.1
- Prospector >= 1.7.7

### Installing

1. Clone the repository to your local machine

```
git clone https://gitlab.lrz.de/fact-checking-tool/fact-checking-backend.git
```

2. Change into the project directory

```
cd fact-checking-backend
```

3. Install Poetry

```
curl -sSL https://install.python-poetry.org | python3 -
```

4. Use poetry to install the dependencies

```
poetry install
```

5. Run the migrations

```
python manage.py makemigrations
python manage.py migrate
```

6. Start the development server

```
python manage.py runserver 8000
```

7. The backend should now be running on http://127.0.0.1:8000/

## Built With

- [Django](https://www.djangoproject.com/) - The web framework used
- [Poetry](https://python-poetry.org/) - Dependency management
- [Prospector](https://prospector.landscape.io/) - Python code analysis
- [Farm-Haystack](https://docs.haystack.deepset.ai/) - Automated pipeline creation
- [Hugging face](https://huggingface.co/) - Pretrained models for natural language processing

## Note

Please make sure you configure the Google and Bing API key and other runtime dependencies as per the requirement of your project.

## Authors

- **[Giang Vu](https://gitlab.lrz.de/ge86yog)**
- **[Abdelrahman Salem](https://gitlab.lrz.de/00000000014A40B6)**
- **[Dmytro Polityka](https://gitlab.lrz.de/ga92nur)**

## Acknowledgments

- Inspiration from other fact checking tools such as [Google Fact Check Tools](https://toolbox.google.com/factcheck/explorer), etc.
- The project uses the following models from Hugging Face:
  - [MoritzLaurer/DeBERTa-v3-large-mnli-fever-anli-ling-wanli](https://huggingface.co/MoritzLaurer/DeBERTa-v3-large-mnli-fever-anli-ling-wanli)
  - [sentence-transformers/all-MiniLM-L6-v2](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2),
  - [facebook/dpr-question_encoder-single-nq-base](https://huggingface.co/facebook/dpr-question_encoder-single-nq-base)
  - [facebook/dpr-ctx_encoder-single-nq-base](https://huggingface.co/facebook/dpr-ctx_encoder-single-nq-base)
  - [deepset/bert-base-cased-squad2](https://huggingface.co/deepset/bert-base-cased-squad2),
