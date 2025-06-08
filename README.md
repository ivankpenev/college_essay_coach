# College Essay Coach MVP

This project is a command-line-based Minimum Viable Product (MVP) for a College Essay Coach, an AI-powered conversational agent designed to help high school students brainstorm and structure their college application essays.

## 1. Project Structure

- `main.py`: The main entry point to run the application.
- `agent.py`: Contains the core logic for the conversational agent.
- `prompts.py`: Stores the system prompts and initial questions for the agent.
- `pyproject.toml`: Configuration for Poetry.
- `.env.example`: An example file for environment variables. You will need to create your own `.env` file.

## 2. Setup and Installation

Follow these steps to set up and run the project on your local machine.

### Prerequisites

- Python 3.7+
- [Poetry](https://python-poetry.org/docs/#installation) for package management
- An OpenAI API Key

### Installation

1.  **Clone the repository (or set up the files as provided):**
    Make sure you have all the project files (`main.py`, `agent.py`, `prompts.py`, `pyproject.toml`).

2.  **Install the dependencies:**
    From the root of the project directory, run the following command. This will create a virtual environment and install all the necessary packages.
    ```bash
    poetry install
    ```

3.  **Set up your environment variables:**
    Create a file named `.env` in the root of the project directory. Copy the contents of `.env.example` into it and add your OpenAI API key:
    ```
    OPENAI_API_KEY="your-actual-openai-api-key"
    ```

## 3. How to Run the Application

Once you have completed the setup, you can run the application directly using Poetry. This command will execute the script within the project's virtual environment.

```bash
poetry run python main.py
```

The conversational agent will start, and you can interact with it directly in your terminal.
