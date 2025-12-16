UdaPlay — AI Game Research Agent

Author: Saad Iqbal

Project Overview

UdaPlay is an AI-powered research agent designed specifically for the video game domain. The objective of this project is to demonstrate the design and implementation of an intelligent system that can accurately answer game-related queries by combining locally indexed knowledge with live web search capabilities.

The project has been intentionally divided into two distinct phases. Each phase focuses on a different technical competency, and together they result in a fully functioning research agent capable of reasoning, retrieving information, and responding in a structured and reliable manner.

Project Breakdown
Part 1: Offline Retrieval-Augmented Generation (RAG)

The first phase of the project focuses on building a persistent vector-based knowledge store using ChromaDB. This component enables the agent to retrieve relevant video game information efficiently without relying on external sources for every query.

Key implementation steps include:

Initialising ChromaDB as a persistent client to ensure data is retained across sessions

Creating a collection configured with suitable embedding functions

Loading and preprocessing structured game data stored in JSON format

Indexing each game as a document containing the following attributes:

Game title

Platform(s)

Genre

Publisher

Descriptive summary

Year of release

This phase establishes the foundation for fast and accurate semantic retrieval, which is later used by the AI agent during inference.

Part 2: AI Agent Development

The second phase builds on the vector database by introducing an intelligent AI agent that can dynamically choose between local retrieval and external web search. The agent is designed to behave like a research assistant rather than a static chatbot.

The agent supports the following functionality:

Answering questions directly from the local vector database (RAG)

Performing web searches when information is missing, ambiguous, or unavailable locally

Maintaining conversation context across multiple user interactions

Producing structured and consistent outputs

Persisting useful information for potential future reuse

Tools Implemented

As part of the agent architecture, the following tools were implemented and integrated:

retrieve_game

Queries the ChromaDB vector store to fetch relevant game documents

evaluate_retrieval

Assesses the relevance and quality of retrieved results before response generation

game_web_search

Uses web search (via Tavily) to supplement local knowledge when necessary

These tools allow the agent to make informed decisions about how and where to source information.

Technical Requirements
Environment Configuration

A .env file is required to securely manage API credentials. The following keys must be provided:

OPENAI_API_KEY="YOUR_KEY"
CHROMA_OPENAI_API_KEY="YOUR_KEY"
TAVILY_API_KEY="YOUR_KEY"

Dependencies

The project was developed using the following technologies and libraries:

Python 3.11 or higher

ChromaDB for vector storage and retrieval

OpenAI for language model interaction

Tavily for web search functionality

python-dotenv for environment variable management

Project Directory Layout

The repository follows a structured layout to separate data, logic, and experimentation:

project/
├── starter/
│   ├── games/           # JSON files containing video game data
│   ├── lib/             # Custom library modules
│   │   ├── llm.py       # Language model abstractions
│   │   ├── messages.py  # Conversation and message handling
│   │   ├── ...
│   │   └── tooling.py   # Tool definitions and integrations
│   ├── Udaplay_01_starter_project.ipynb  # Part 1: Vector DB implementation
│   └── Udaplay_02_starter_project.ipynb  # Part 2: AI agent implementation

Execution Instructions

To run and evaluate the project:

Create and activate a Python virtual environment

Install all required dependencies

Configure the .env file with valid API keys

Execute the notebooks in the following order:

Part 1 notebook to build and populate the vector database

Part 2 notebook to construct and test the AI agent

Completing both notebooks is required for full system functionality.

Validation and Testing

After implementation, the agent can be validated using representative queries such as:

“When were Pokémon Gold and Silver released?”

“Which Mario title was the first 3D platformer?”

“Was Mortal Kombat X released on PlayStation 5?”

These examples intentionally test both local retrieval and web-based reasoning.

Optional Enhancements

Beyond the core requirements, the system can be extended with additional capabilities, including:

Long-term memory for retaining knowledge across sessions

Expanded tooling and reasoning capabilities for more advanced use cases

Final Notes

Robust error handling has been considered throughout the implementation

API credentials are managed securely and excluded from version control

Code is clearly documented to support readability and assessment

The system has been tested against a variety of query types to ensure reliability
