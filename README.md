# Language Learning System

A modular language learning platform designed to simulate structured training similar to professional language courses (e.g., Goethe exam preparation).  
The system combines **AI-assisted exercises**, **structured learning modules**, and **persistent session tracking** to guide users through vocabulary, reading, writing, and speaking practice.

The architecture separates **backend learning logic**, **frontend UI**, and **data persistence**, allowing the platform to scale and evolve into a full learning environment.

---

# Cognitive Limitations and AI Interaction

People with dementia often experience memory loss, difficulty maintaining context, and cognitive overload when faced with complex instructions. Tasks that involve multiple steps, long explanations, or frequent topic changes can quickly become confusing. Effective support strategies typically involve structured routines, small task segments, repeated context reminders, and clear boundaries between activities.

Large language models such as ChatGPT show different but structurally similar limitations. They may lose context in long conversations, struggle with overloaded prompts, or drift away from the original task when too much information is provided. This application addresses these issues by structuring learning into clear modules, storing session history, and delivering exercises step-by-step. By controlling context and task flow, the system improves reliability and makes AI-assisted learning more stable and predictable.

# Project Goals

The project aims to build a **structured AI-assisted language learning system** with the following goals:

- Provide **step-by-step language training modules**
- Track **learning progress across sessions**
- Simulate **real exam-style exercises**
- Allow **AI-guided explanations and corrections**
- Maintain a **persistent learning history**

The system is designed to support structured learning workflows such as:

- Vocabulary training
- Domain-specific vocabulary
- Reading comprehension exercises
- Writing practice
- Speaking simulations
- Mixed exam simulations

---

# Architecture Overview

The system consists of four main components:

```
Browser (UI)
     ↓
Nginx (reverse proxy)
     ↓
Flask API (learning logic + OpenAI integration)
     ↓
MySQL database (learning progress + sessions)
```

Components:

- **UI**
  - Lightweight JavaScript frontend
  - Handles rendering exercises and user input
  - Communicates with backend via REST API

- **API**
  - Flask application
  - Controls learning modules and exercises
  - Manages sessions and messages
  - Integrates with OpenAI for AI responses

- **Database**
  - MySQL
  - Stores vocabulary, exercises, sessions, and messages

- **Infrastructure**
  - Docker-based environment
  - Nginx reverse proxy
  - phpMyAdmin for database inspection

---

# Learning Model Structure

The learning system is structured into multiple layers:

```
training_lesson
    ↓
modules
    ↓
sessions
    ↓
session_messages
```

### Training Lesson
Represents a training day or learning unit.

### Modules
A lesson contains multiple modules:

1. Core Vocabulary  
2. Domain Vocabulary  
3. Reading Exam  
4. Writing Exam  
5. Speaking Exam  

### Sessions
Each module creates sessions that represent exercise interactions.

### Session Messages
All user and assistant messages are stored to reconstruct conversations and learning progress.

---

# Installation

## Requirements

- Docker
- Docker Compose
- Python 3.12+

---

## Setup

Clone the repository:

```bash
git clone <repository_url>
cd learning_system
```

Create a `.env` file with required variables:

```
MYSQL_ROOT_PASSWORD=yourpassword
DATABASE_NAME=learning_system
OPENAI_API_KEY=your_api_key
FLASK_SECRET_KEY=your_secret
```

Start the environment:

```bash
docker compose up --build
```

---

# Running the System

After starting Docker:

| Service | URL |
|------|------|
| Application | http://localhost:8000 |
| phpMyAdmin | http://localhost:8080 |

The UI allows selecting a module and starting a training session.

---

# Usage

1. Open the application in the browser.
2. Select a learning module.
3. The backend generates a learning session.
4. Exercises and explanations appear in the interface.
5. User responses are processed by the backend and stored in the database.

Each session keeps a full history of interactions.

---

# Modules

The system currently supports:

| Module | Description |
|------|------|
| Core Vocabulary | Core German vocabulary training |
| Domain Vocabulary | Specialized vocabulary learning |
| Reading | Reading comprehension tasks |
| Writing | Structured writing exercises |
| Speaking | Simulated speaking tasks |

Each module can contain multiple exercises and AI-generated feedback.

---

# Testing

The backend includes a full unit test suite using **pytest**.

Run tests:

```bash
pytest api/tests
```

Coverage is tracked using **pytest-cov**.

---

# Development Workflow

The project uses:

- **pytest** for testing
- **pre-commit hooks** for test coverage enforcement
- **Docker containers** for consistent environments

Before committing, tests and coverage checks are executed automatically.

---

# Future Improvements

Planned improvements include:

- Adaptive learning difficulty
- Progress tracking dashboards
- AI-based pronunciation feedback
- Exercise analytics
- Expanded domain vocabulary modules
- Multi-user account support

---

# License

GNU General Public License v3.0