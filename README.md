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

## Elasticsearch

Both pipelines use Wikipedia Database, which must be running on an Elastic Search installation. The following [https://github.com/AlonEirew/wikipedia-to-elastic](project) contains instructions and source code to import a wikipedia archive. To be able to run this project one needs to install specifically Java 11. Afterwards one needs to build the gradle project, unzip the downloaded Wikipedia archive and place the archive in the dumps folder. Then the import process can be started. After the dump has been imported successfully, one needs to clone the entire index, for the NLI pipeline to use it. DPR embeddings should be generated on the old index, for DPR(embeddings.py). The script requires slightly other field names, one needs to rename parsedParagraphs to content and name to meta.title. There are dedicated http calls for that. One needs to join all parsed paragraphs at first, run concat-pipeline and trigger-pipeline for that. Then one needs to run rename-pipeline and trigger-rename calls. Finally, one can move all documents with renamed fields to another index, for convenience.

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
