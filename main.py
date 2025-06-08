import os
from dotenv import load_dotenv

from agent import Agent


def main():
    """
    The main entry point for the College Essay Coach application.
    """
    # Load environment variables from .env file
    load_dotenv()

    # NOTE: The API key is loaded from the environment variable OPENAI_API_KEY.
    # Make sure to create a .env file in the root of the project and add your key.
    # For example: OPENAI_API_KEY="your-key-here"
    if not os.getenv("OPENAI_API_KEY"):
        print("Error: OPENAI_API_KEY not found.")
        print("Please create a .env file and add your OpenAI API key.")
        return

    print("Welcome to the College Essay Coach!")
    print("I'm here to help you brainstorm and outline your college essay.")
    print("Let's start with a few questions to get to know you better.")
    print("-" * 50)

    agent = Agent()
    agent.run()

    print("-" * 50)
    print("Thank you for sharing. This is a great starting point!")
    print("In our next session, we can start brainstorming some essay ideas.")


if __name__ == "__main__":
    main() 