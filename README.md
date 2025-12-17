Part 1 - RAG Pipeline
- Sets up a ChromaDB vector database
- Processes and embed game data from JSON files
- Implements semantic search functionality
- Creates a reusable vector store manager
  
Part 2 - Agent Implementation
- Builds an agent with three core tools:
  ~ retrieve_game: Search the vector database
  ~ evaluate_retrieval: Assess answer quality
  ~ game_web_search: Fall back to web search
- Implements a state machine for agent workflow
- Creates a reporting system for clear output
