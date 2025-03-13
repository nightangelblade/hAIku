# hAIku

## Goal
Routinely request a haiku from LLMs, write haiku data to file, commit changes to github, generate and host data on static site.

## Setup
Python version: `3.12.5` or so

Virtual Environment: `venv` version `20.26.3`

Formatting: `black`

If you don't have venv, install it with `pip install virtualenv`

Create a virtual environment called venv with: `python3 -m venv venv`

Start virtual environment:

On Windows: `venv\Scripts\activate`
On Mac: `source venv/bin/activate`

Dependency Requirements list: `requirements.txt`

Create new requirements.txt: `pip freeze > requirements.txt`

Environment variables can be stored in a local `.env` file. This uses `python-dotenv`

Variables needed:
- OpenAI API Key as `OPENAI_API_KEY`