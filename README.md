# Travel Copilot

![Travel Copilot Design](https://github.com/Shuaib-8/Travel-Copilot/blob/main/extra/travel-copilot-design.png)

## Overview

The Travel Copilot is an AI-powered assistant designed to help users explore and ideate around travel plans. By leveraging the **Cohere LLM**, the Travel Copilot can understand user preferences, provide personalized recommendations (travel guidance), and assist with various travel-related tasks over a Question-Answering (QA) chat interface. 

## Design & Requirements

The inital draft of the project has the following requirements:

- Chat interface - A user can submit an input query and receive a response from the LLM in the Chat interface UI.
- Threaded conversations - In the main the chat interface is a thread of discussion between the user and the LLM. User query is labelled on top followed by a LLM response with the generated text. The LLM is grounded to have multi-turn style discussions, being context aware.
- Reset - Users can discard the session as they please by scrolling and excuting to the 'Reset' button
- API integration (optional) - There's a chance to navigate to the API docs to potentially integrate more specialised workflows to respond to the LLM, however with the caveat that these conversations aren't stateful, and no memory management is considered as in the frontend
- LLM Grounding and Safety - The LLM is designed to only provide and respond to questions around travel guidance. Anything outside its realm it should decline to respond

## Features

- **Cohere LLM grounded travel assistant**: Users can input their travel preferences, and the Travel Copilot will generate ideas around their trip, places of interest, accommodations, and activities etc. It avoids veering out of scope by focusing on travel-related queries only. 
- **User-friendly interface**: The chat interface allows users to interact with the assistant in a natural and intuitive way i.e. not just one shot reponses but is also geared towards multi-turn conversations.
- **Short term session persistence**: The assistant can remember the context of the conversation within a session, allowing for more coherent and relevant responses. Even after a refresh, the session context is maintained for a limited time. A full restart of the app will clear the session permanently.
- **API integration**: The Travel Copilot can be easily integrated into other applications or services via its API - although it's not stateful and as such does not maintain long-term user sessions or accomodate multi-turn conversations across sessions.

## Stack 

- **Backend**: Django Ninja API framework for building the backend services.
- **Frontend**: A combination of Tailwind CSS, Alpine.js, and HTMX for a responsive and interactive user interface.
- **LLM**: Cohere's LLM for generating travel-related responses.
- **Testing**: Pytest/pytest-django for automated testing of the application.

## Future Considerations 

- **User management, authentication, and authorization**: Implementing user accounts to allow for personalized experiences and session management.
- **Persistent storage**: Using a production database such as PostgreSQL to store user preferences, past interactions, and other relevant data.
- **Asynchronous processing**: Use of Cohere's Async client to handle long-running tasks and improve responsiveness.


## Installation and Setup

To proceed with the installation and setup of the Travel Copilot, follow these steps:
- COHERE API Key: [Sign up for a Cohere account and obtain an API key](https://dashboard.cohere.com/api-keys). Set the `COHERE_API_KEY` environment variable with your key e.g. `export COHERE_API_KEY=your_api_key` or setup a `.env` file in the root of the project like so:

```env
# .env file
COHERE_API_KEY=your_api_key
```

### Local Development

Clone the repository and install the dependencies:

```bash
$ git clone https://github.com/Shuaib-8/Travel-Copilot.git
$ cd travel-copilot
$ pip install -r requirements.txt
```
Then run the migrations and start the development server:

```bash
$ python manage.py makemigrations
$ python manage.py migrate
$ python manage.py runserver
```

You can now access the Travel Copilot at `http://localhost:8000`.

If you want to run the test suite, you can do so with:

```bash
$ pip install -r requirements-dev.txt  # Install development dependencies
$ pytest .
```

An example of test suite output:

```
$ pytest . 
=================================================================================== test session starts ===================================================================================
platform linux -- Python 3.13.5, pytest-8.4.1, pluggy-1.6.0
django: version: 5.1.2, settings: travel_copilot.settings (from env)
rootdir: /app
configfile: pyproject.toml
plugins: django-4.11.1, cov-6.2.1, anyio-4.9.0
collected 20 items                                                                                                                                                                        

tests/test_api.py ...........                                                                                                                                                       [ 55%]
tests/test_views.py ....                                                                                                                                                            [ 75%]
tests/test_llm_service.py .....                                                                                                                                                     [100%]
============================================================================= 20 passed, 3 warnings in 0.25s ==============================================================================
```

### Docker Setup

To run the Travel Copilot using Docker, ensure you have Docker installed on your machine. Then, build and run the Docker container:

```bash
$ docker build -t travel-copilot .
# Ensure you have a .env file in the root directory with your COHERE_API_KEY
$ docker run -p 8000:8000 --env-file .env travel-copilot
``` 

You can now access the Travel Copilot at http://localhost:8000.

If you want to run the test suite in Docker, you can do so with:

```bash
# You can find the container ID with `docker ps`
$ docker exec -it <CONTAINER_ID> bash
$ pytest .
```

### Deployment

My deployment strategy for this django based full stack application is to use [Fly.io](https://fly.io/) for hosting the Travel Copilot. 

It can be accessed at [https://drf-fs-travel-copilot-polished-grass-5647.fly.dev/](https://drf-fs-travel-copilot-polished-grass-5647.fly.dev/).

If there are any issues accessing the deployed app please email me at [shuaib.ahmed45@gmail.com](mailto:shuaib.ahmed45@gmail.com).

Also consider whether Cohere LLM service is down or not, as this can affect the app's functionality. This is visiible via the Cohere Status Checker: [https://status.cohere.com/](https://status.cohere.com/).

### Walkthrough of the App

The Travel Copilot is designed to be user-friendly and intuitive. Here's a brief walkthrough.

1. **Home Page**: When you first visit the app, you'll see a chat interface where you can start interacting with the Travel Copilot.

![Travel Copilot Landing](https://github.com/Shuaib-8/Travel-Copilot/blob/main/extra/travel-copilot-landing.png)

2. **Chat Interface**: You can type your travel-related queries into the input box and hit enter/button to submit. The Travel Copilot will respond with relevant information based on your query like so for the example query 'Tell me about Paris':

![Travel Copilot Chat](https://github.com/Shuaib-8/Travel-Copilot/blob/main/extra/travel-copilot-one-shot-response.png)

3. **Multi-turn Conversations**: You can continue the conversation by asking follow-up questions or providing more context. The Travel Copilot will maintain the context of the conversation within the session. An example of a multi-turn conversation is shown below where the user follows up with a question 'What about the restaurants' and the LLM responds with a relevant answer still in the context of Paris:

![Travel Copilot follow up](https://github.com/Shuaib-8/Travel-Copilot/blob/main/extra/travel-copilot-follow-up-response.png)

Again showing further the context awareness of the LLM with the follow-up about 'How much to buy a ticket to Paris?'

![Travel Copilot Multi-Turn part 2](https://github.com/Shuaib-8/Travel-Copilot/blob/main/extra/travel-copilot-multi-turn-response.png)

4. **Resetting the Session**: If you want to start a new conversation, you can click the 'Reset' button to clear the current session. This will remove all previous messages and allow you to start fresh.

![Travel Copilot Reset](https://github.com/Shuaib-8/Travel-Copilot/blob/main/extra/travel-copilot-reset-conversation.png)

5. **Accessing the API Docs from the App**: You can find the API documentation by clicking on the 'API Docs' link in the app's navigation menu. This will provide you with detailed information about the available endpoints and how to use them.

![Travel Copilot API Docs hyperlink](https://github.com/Shuaib-8/Travel-Copilot/blob/main/extra/travel-copilot-api-docs.png)

6. **Swagger API Documentation**: The API documentation provides detailed information about the available endpoints, request parameters, and response formats. You can use this documentation to integrate the Travel Copilot into your own applications or services. The workhorse is the POST request via `/api/travel-guidance/` which takes a JSON payload with the user's query and returns a response from the LLM. A health check endpoint is also available at `/api/health/` to ensure the service is running correctly.

![Travel Copilot Swagger API Docs](https://github.com/Shuaib-8/Travel-Copilot/blob/main/extra/travel-copilot-api-docs-swagger.png)

