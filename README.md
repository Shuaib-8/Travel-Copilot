# Travel Copilot

![alt text](https://github.com/Shuaib-8/Travel-Copilot/blob/main/extra%20/travel-copilot-design.png)

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

## Future Considerations 

- **User management, authentication, and authorization**: Implementing user accounts to allow for personalized experiences and session management.
- **Persistent storage**: Using a production database such as PostgreSQL to store user preferences, past interactions, and other relevant data.
- **Asynchronous processing**: Use of Cohere's Async client to handle long-running tasks and improve responsiveness.


