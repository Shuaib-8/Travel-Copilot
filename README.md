# Travel Copilot

## Overview

The Travel Copilot is an AI-powered assistant designed to help users explore and ideate around travel plans. By leveraging LLMs, the Travel Copilot can understand user preferences, provide personalized recommendations, and assist with various travel-related tasks over a Question-Answering (QA) chat interface. 


## Features

- **Cohere LLM grounded travel assistant**: Users can input their travel preferences, and the Travel Copilot will generate ideas around their trip, places of interest, accommodations, and activities etc. It avoids veering out of scope by focusing on travel-related queries only. 
- **User-friendly interface**: The chat interface allows users to interact with the assistant in a natural and intuitive way i.e. not just one shot reponses but is also geared towards multi-turn conversations.
- **Short term session persistence**: The assistant can remember the context of the conversation within a session, allowing for more coherent and relevant responses. Even after a refresh, the session context is maintained for a limited time. A full restart of the app will clear the session permanently.
- **API integration**: The Travel Copilot can be easily integrated into other applications or services via its API - although it's not stateful and as such does not maintain long-term user sessions or accomodate multi-turn conversations across sessions.

## Stack 

- **Backend**: Django Ninja API framework for building the backend services.
- **Frontend**: A combination of Tailwind CSS, Alpine.js, and HTMX for a responsive and interactive user interface.
- **LLM**: Cohere's LLM for generating travel-related responses.

## Future Considerations 

- **User management, authentication, and authorization**: Implementing user accounts to allow for personalized experiences and session management.
- **Persistent storage**: Using a production database such as PostgreSQL to store user preferences, past interactions, and other relevant data.
- **Asynchronous processing**: Use of Cohere's Async client to handle long-running tasks and improve responsiveness.

## Design 

