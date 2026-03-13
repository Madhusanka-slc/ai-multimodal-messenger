# Nova - AI Multimodal Messenger

**Nova** is a Python-based AI-powered multimodal messenger that integrates text, voice, and image inputs for interactive conversations. It leverages memory, context, and workflow orchestration to provide intelligent, personalized responses.

---

## Features

- Text, voice, and image input support
- AI-driven natural language understanding
- Memory management for context-aware responses
- Modular workflow orchestration
- Text-to-Speech and Text-to-Image generation
- Easy deployment with Docker or local Python environment

---

## Architecture

Below is a high-level architecture diagram of **Nova**:

![Architecture Diagram](images/architecture_diagram.svg)

**Main Components:**

1. **Memory Layer**  
   - **DuckDB** for short-term memory (recent messages)  
   - **Qdrant** for long-term memory (retrieval and embeddings)  

2. **Workflow Layer**  
   - **LangGraph** orchestrates the nodes for conversation, image/audio generation, and summarization  

3. **AI Models**  
   - **TogetherAI / Groq** for text-based responses  
   - **Whisper** for speech-to-text  
   - **ElevenLabs** for text-to-speech  
   - **Black Forest Labs (FLUX.1)** for text-to-image generation  

4. **Configuration & APIs**  
   - Managed via **Pydantic Settings** (`.env` file)  

---

## Workflow Graph

Below is the workflow that Nova follows for processing user input:

![Workflow Graph](images/graph_diagram.svg)

**Node Functions:**

1. **Memory Extraction Node** – Extracts and stores key info from user messages.  
2. **Router Node** – Determines whether the next response is text, image, or audio.  
3. **Context Injection Node** – Adds contextual info like current activity or schedule.  
4. **Memory Injection Node** – Retrieves relevant memories to maintain conversation continuity.  
5. **Conversation Node** – Generates AI text responses based on context and memories.  
6. **Image Node** – Generates images from recent messages and appends to conversation.  
7. **Audio Node** – Converts Nova’s text responses into audio using TTS.  
8. **Summarize Conversation Node** – Summarizes long conversations to condense memory.  
9. **Conditional Edges** – `select_workflow` decides response type; `should_summarize_conversation` triggers summarization.

---

## Tech Stack Summary

| Component | Technology | Purpose |
|-----------|-----------|---------|
| Short-term memory | DuckDB | Fast local storage of recent messages |
| Long-term memory | Qdrant | Stores embeddings of past messages and memories |
| Workflow orchestration | LangGraph | Executes Nova’s conversation/image/audio workflow |
| Text-to-Speech | ElevenLabs | Converts AI responses into audio |
| Text/Multimodal AI | TogetherAI, Groq | Generates text-based responses |
| Text-to-Image | Black Forest Labs (FLUX.1) | Generates images from prompts |
| Speech-to-Text | Whisper | Converts audio inputs into text |
| Configuration | Pydantic Settings | Manages API keys, models, and workflow settings |

---

## Installation

1. Clone the repository:

```bash
git clone https://github.com/Madhusanka-slc/ai-multimodal-messenger.git
cd ai-multimodal-messenger
```

2. Create a virtual environment and install dependencies:

```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
pip install -r requirements.txt
```

3. Copy `.env.example` to `.env` and configure your API keys and settings.

---

## Running Nova

* **Local Python run**:

```bash
python -m src.ai_companion.main
```

* **Using Docker**:

```bash
docker-compose up --build
```