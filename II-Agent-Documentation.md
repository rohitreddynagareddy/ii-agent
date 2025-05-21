# II-Agent Project Documentation

## 1. Project Overview

II-Agent is an AI-powered agent capable of interacting with web browsers and performing tasks based on user instructions. It leverages Large Language Models (LLMs) to understand and execute complex commands, utilizing a suite of tools for various functionalities. The project aims to provide a seamless interface for users to automate web-based workflows and interact with web content in an intelligent manner.

## 2. Architecture

The II-Agent system is composed of distinct backend and frontend components that work in tandem.

### 2.1. Backend

The backend is responsible for the core logic of the agent, including processing user commands, interacting with LLMs, managing tools, and handling browser automation.

*   **Programming Language:** Python (see `.python-version` for specific version, e.g., if it contains "3.11.x", then Python 3.11.x is expected).
*   **Key Libraries/Frameworks:** Likely an ASGI framework such as FastAPI or Quart (inferred from `ws_server.py` which suggests WebSocket usage, common in these frameworks), Poetry (as indicated by `pyproject.toml` for dependency management). LLM client implementations exist for Anthropic (`src/ii_agent/llm/anthropic.py`) and OpenAI (`src/ii_agent/llm/openai.py`).
*   **Core Modules Overview:** The backend logic is primarily organized within `src/ii_agent/` with subdirectories for `core/`, `llm/`, `browser/`, `tools/`, and `db/`.

### 2.2. Frontend

The frontend provides the user interface for interacting with the II-Agent, displaying information, and managing tasks.

*   **Programming Language:** TypeScript
*   **Framework:** Next.js (confirmed by `frontend/next.config.ts`)
*   **Key Libraries/Frameworks:** React (inherent to Next.js), Tailwind CSS (implied by `frontend/postcss.config.mjs` and common Next.js practice), UI components likely from a library like Shadcn/ui (inferred from `frontend/components/ui/`). Package management is handled by Yarn (due to `frontend/yarn.lock`) or npm.

## 3. Core Components

This section details the critical components of the II-Agent system.

### 3.1. Agent

*   **Description:** The central orchestrator of the backend. It receives user input, communicates with the LLM to understand intent, and coordinates the use of various tools and browser automation capabilities to achieve the user's goals.
*   **Key Responsibilities:**
    *   Input parsing and processing.
    *   LLM interaction and prompt engineering.
    *   Tool selection and execution.
    *   State management.
    *   Workflow execution.

### 3.2. LLM Clients

*   **Description:** Modules responsible for interacting with different Large Language Models. Specific clients are implemented for OpenAI (see `src/ii_agent/llm/openai.py`) and Anthropic models (see `src/ii_agent/llm/anthropic.py`).
*   **Key Responsibilities:**
    *   Formatting requests to LLM APIs.
    *   Handling API responses and errors.
    *   Managing different LLM configurations and authentication.

### 3.3. Tools

*   **Description:** A collection of specialized modules that the agent can use to perform specific actions.
*   **Examples (derived from `src/ii_agent/tools/` directory structure):**
    *   `bash_tool.py`: Enables execution of shell commands.
    *   Browser manipulation tools (located in `src/ii_agent/tools/browser_tools/`).
    *   `complete_tool.py`: Tool to signify task completion.
    *   `deep_research_tool.py`: For conducting in-depth research.
    *   `list_html_links_tool.py`: Extracts hyperlinks from HTML content.
    *   `markdown_converter.py`: Converts text to Markdown format.
    *   `presentation_tool.py`: Aids in creating presentations.
    *   `sequential_thinking_tool.py`: Helps in breaking down tasks sequentially.
    *   `static_deploy_tool.py`: For deploying static web content.
    *   `str_replace_tool.py`: For replacing string occurrences.
    *   `text_inspector_tool.py`: Inspects textual content.
    *   `visit_webpage_tool.py`: Navigates to and loads webpages.
    *   `web_search_tool.py`: Performs searches on the web.
    *   `youtube_transcript_tool.py`: Fetches transcripts from YouTube videos.
    *   More specialized tools can be found in `src/ii_agent/tools/advanced_tools/`.
*   **Key Responsibilities:**
    *   Encapsulating specific functionalities.
    *   Providing a standardized interface for the agent.

### 3.4. Browser Automation

*   **Description:** Component responsible for controlling and interacting with web browsers, with its core logic in `src/ii_agent/browser/browser.py`.
*   **Technology:** Appears to be a custom browser automation solution, likely built on top of a library like Playwright or Puppeteer. This is suggested by the use of JavaScript injection (e.g., `findVisibleInteractiveElements.js`) for enhanced browser interaction.
*   **Key Responsibilities:**
    *   Launching and closing browsers.
    *   Navigating to URLs.
    *   Interacting with web elements (clicking, typing, scraping).
    *   Managing browser sessions and cookies.

### 3.5. Event System

*   **Description:** Facilitates communication and data flow within the backend (see `src/ii_agent/core/event.py`) and potentially between the backend and frontend.
*   **Type:** The specific architecture (e.g., Asynchronous, Pub/Sub) would require inspection of `src/ii_agent/core/event.py`.
*   **Key Responsibilities:**
    *   Decoupling components.
    *   Broadcasting important events (e.g., task completion, errors).
    *   Enabling real-time updates.

### 3.6. Database

*   **Description:** Handles persistent storage of data, managed by components in `src/ii_agent/db/manager.py` and defined by models in `src/ii_agent/db/models.py`.
*   **Type:** The specific database system (e.g., PostgreSQL, SQLite, MongoDB) is not immediately clear from the file structure. It often involves an ORM like SQLAlchemy for relational databases.
*   **Key Responsibilities:**
    *   Storing user information and preferences.
    *   Logging agent activities and task history.
    *   Caching data.

### 3.7. Frontend Components

#### 3.7.1. Home (`frontend/components/home.tsx`)

*   **Description:** The main landing page or dashboard for the II-Agent user interface.
*   **Functionality:** Likely displays an overview, recent activities, and provides a way to initiate new tasks with the agent.

#### 3.7.2. ChatMessage (`frontend/components/chat-message.tsx`)

*   **Description:** Component responsible for rendering individual messages within the chat interface, representing both user inputs and agent responses.
*   **Functionality:** Displays text, potentially formatted code blocks, images, and timestamps associated with each message.

#### 3.7.3. Editor (`frontend/components/code-editor.tsx`)

*   **Description:** An integrated code or text editor embedded within the user interface.
*   **Functionality:** Allows users to view, write, or modify scripts and text files that the agent might use or generate.

#### 3.7.4. Terminal (`frontend/components/terminal.tsx`)

*   **Description:** An integrated terminal emulator within the frontend.
*   **Functionality:** Provides users with the ability to execute command-line interface (CLI) commands or view logs/output from the backend processes.

#### 3.7.5. Browser View (`frontend/components/browser.tsx`)

*   **Description:** A component that renders a view of the web browser instance being controlled by the II-Agent.
*   **Functionality:** Offers a real-time or near real-time visual stream of the automated browser's actions, possibly with interactive elements for user guidance or intervention.

## 4. Setup and Configuration

### 4.1. Environment Variables

*   **`.env.example`:** A template file is provided. Copy it to `.env` and fill in the necessary values.
*   **Key Variables (refer to `.env.example` for a complete list):**
    *   `OPENAI_API_KEY`: Your API key for accessing OpenAI models.
    *   `ANTHROPIC_API_KEY`: Your API key for accessing Anthropic models.
    *   `DATABASE_URL`: Connection string for the application's database.
    *   Other keys for specific tools or services (e.g., search API keys).

### 4.2. Python Backend

1.  **Prerequisites:**
    *   Python: The specific version is typically defined in the `.python-version` file (e.g., Python 3.11.x).
    *   Poetry: For managing Python dependencies, as specified in `pyproject.toml`.
2.  **Installation:**
    ```bash
    # Ensure Poetry is installed (see https://python-poetry.org/docs/#installation)
    poetry install
    ```
    *(If a `requirements.txt` is provided and maintained, alternative `pip install -r requirements.txt` could be an option for non-Poetry users, but Poetry is primary).*
3.  **Running the Backend:**
    *   **WebSocket Server (Primary Agent Interface):** The main server for agent interaction is likely `ws_server.py`.
        ```bash
        poetry run python ws_server.py
        ```
    *   **Command Line Interface (CLI):** A CLI for direct interaction or scripting is available through `cli.py`.
        ```bash
        poetry run python cli.py --help  # Check for available commands and options
        ```
    *   **GAIA Benchmark Script:** The `run_gaia.py` script is likely used for running evaluations, possibly related to the GAIA benchmark.
        ```bash
        poetry run python run_gaia.py --help # Check for usage instructions
        ```

### 4.3. Next.js Frontend

1.  **Prerequisites:**
    *   Node.js: A recent LTS version (e.g., 18.x or 20.x). Check `frontend/package.json` for an `engines` field for specific version constraints.
    *   Yarn: Preferred package manager due to the presence of `frontend/yarn.lock`. npm can also be used.
2.  **Installation:**
    ```bash
    cd frontend
    yarn install   # Preferred method
    # OR
    # npm install
    ```
3.  **Running the Frontend (Development Mode):**
    ```bash
    npm run dev
    # or
    yarn dev
    ```
4.  **Building for Production:**
    ```bash
    npm run build
    # or
    yarn build
    ```

## 5. Workflow

### 5.1. Web UI Workflow

1.  User accesses the II-Agent application through their web browser.
2.  User inputs a command or task description into the chat interface.
3.  The frontend sends the request to the backend.
4.  The Agent component in the backend processes the request, potentially using an LLM client to understand the intent.
5.  The Agent selects and executes appropriate tools or browser automation actions.
6.  The Browser View may display the automated browser interactions in real-time.
7.  Results and feedback are sent back to the frontend and displayed in the chat interface.
8.  The Editor and Terminal components can be used for auxiliary tasks like script editing or command execution.

### 5.2. CLI Workflow (If Applicable)

*   **Description:** Detail how a user would interact with the agent via a Command Line Interface.
*   **Example Commands:**
    ```bash
    # Example based on typical CLI agent interaction, actual commands via `python cli.py --help`
    poetry run python cli.py --task "Summarize the main points from https://example.com/article"
    poetry run python cli.py --script "path/to/myscript.json" 
    ```
    *(Actual commands and their structure should be verified by running `poetry run python cli.py --help`)*

---

*This document is a living document and will be updated as the project evolves.*
