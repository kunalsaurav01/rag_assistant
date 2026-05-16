# LangGraph Documentation Overview

LangGraph is a library for building stateful, multi-actor applications with LLMs. 
It is built on top of LangChain and allows you to create cyclic graphs, which are common in agentic workflows.

## Key Concepts

### StateGraph
The `StateGraph` is the core class. It represents a graph where each node updates a shared state.

### Nodes
Nodes are functions that take the current state and return an updated state.

### Edges
Edges define the flow between nodes. Conditional edges allow for decision-making logic.

## Why use LangGraph?
LangGraph provides fine-grained control over loops and state, which is difficult with standard linear chains.
It is ideal for self-corrective RAG where you might need to rewrite a query and try again.
