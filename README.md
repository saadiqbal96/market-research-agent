Udaplay Project – RAG & Agent-Based QA System

This project implements an end-to-end Retrieval-Augmented Generation (RAG) pipeline and a stateful, tool-using agent to answer questions about video games using both local knowledge and web-based fallback search.

Part 1 – Offline RAG Pipeline

In Part 1, a persistent vector database is constructed to support semantic retrieval over a curated video game dataset.

Key Features

Loads and processes structured video game data from JSON files

Converts each game record into a semantically searchable document

Generates vector embeddings and stores them in a persistent ChromaDB collection

Demonstrates semantic similarity search over the vector database

Wraps the vector database in a reusable VectorStore abstraction for clean integration

This stage establishes the knowledge base used by the agent in Part 2.

Part 2 – Agent Implementation

In Part 2, a stateful, tool-driven agent is built on top of the RAG pipeline to answer user queries intelligently.

Agent Capabilities

Implements three core tools:

Internal Retrieval Tool – retrieves relevant game information from the vector database

Evaluation Tool – assesses the quality and completeness of retrieved results

Web Search Tool – performs external search when internal knowledge is insufficient

Orchestrates tool usage using a state machine–based workflow

Maintains session-based memory, allowing the agent to handle multiple queries within the same session while preserving conversational context

Produces clear, structured responses with citations when applicable

Demonstrates agent behavior through multiple example queries, including cases requiring web search fallback

Project Structure

Udaplay_01_solution_project.ipynb
Builds and validates the offline RAG pipeline and vector database.

Udaplay_02_solution_project.ipynb
Implements and demonstrates the stateful agent, tool usage, and session-based reasoning.

Summary

This project showcases a complete RAG-powered agent system that:

Combines local vector-based retrieval with external web search

Uses structured agent workflows for transparency and scalability

Supports multi-turn, session-aware interactions

Produces well-formatted, explainable answers

The implementation follows best practices for modular design, extensibility, and reproducibility.
