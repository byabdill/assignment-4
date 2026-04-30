# AI Football Scout Agent

This project is an automated football player analysis pipeline built for **Assignment 4 (AIPE)**.

## How it works:
- **Node 1**: Cleans and prepares the input match report.
- **Node 2**: Uses **Gemini LLM** with **Pydantic** to extract structured technical ratings.
- **Node 3**: Uses **Gemini LLM** to generate a final recruitment recommendation and market value.

## Requirements:
- Python 3.10+
- LangGraph
- LangChain Google GenAI
- Pydantic