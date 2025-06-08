import os
import json
import glob
from datetime import datetime
from openai import OpenAI

from prompts import INITIAL_QUESTIONS, SYSTEM_PROMPT


class Agent:
    """
    The conversational agent for the College Essay Coach.
    """

    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.conversation_history = self._load_or_initialize_conversation()
        self.initial_questions = INITIAL_QUESTIONS

    def _load_or_initialize_conversation(self):
        """
        Checks for previous sessions and asks the user if they want to resume one.
        If not, it starts a new conversation.
        """
        if not os.path.exists("sessions"):
            os.makedirs("sessions")

        session_files = sorted(glob.glob("sessions/conversation_*.json"), reverse=True)

        if not session_files:
            print("Starting a new session.")
            return [{"role": "system", "content": SYSTEM_PROMPT}]

        print("\nFound previous sessions:")
        for i, f in enumerate(session_files):
            print(f"  {i + 1}: {os.path.basename(f)}")

        while True:
            try:
                choice = input(
                    "\nEnter the number of the session to resume, or 'n' for a new session: "
                )
                if choice.lower() == "n":
                    print("\nStarting a new session.")
                    return [{"role": "system", "content": SYSTEM_PROMPT}]

                choice_index = int(choice) - 1
                if 0 <= choice_index < len(session_files):
                    selected_file = session_files[choice_index]
                    print(f"\nResuming session from {os.path.basename(selected_file)}.")
                    with open(selected_file, "r") as f:
                        return json.load(f)
                else:
                    print("Invalid number. Please try again.")
            except ValueError:
                print("Invalid input. Please enter a number or 'n'.")

    def run(self):
        """
        Runs the conversational agent. If resuming, it skips the initial interview.
        """
        is_resuming = len(self.conversation_history) > 1

        if not is_resuming:
            # Initial interview phase
            for question in self.initial_questions:
                user_input = input(f"AI: {question}\nYou: ")
                self.conversation_history.append({"role": "user", "content": user_input})

                # Get a brief, non-question follow-up
                response = self._get_agent_response(
                    extra_prompt="Provide a brief, encouraging, and supportive validation of the user's response. Do not ask a follow-up question."
                )
                print(f"AI: {response}")
                self.conversation_history.append(
                    {"role": "assistant", "content": response}
                )

            # Transition to the open-ended brainstorming phase
            response = self._get_agent_response(
                extra_prompt="The initial questions are complete. Now, transition to the broader, exploratory phase as instructed in the main system prompt. Acknowledge the shift and ask your first open-ended exploratory question based on the student's initial answers."
            )
            print(f"AI: {response}")
            self.conversation_history.append({"role": "assistant", "content": response})
        else:
            print("\n--- Resuming conversation ---")
            # When resuming, get a re-orienting response from the agent.
            response = self._get_agent_response(
                extra_prompt="You are resuming a previous conversation. Briefly summarize the last one or two exchanges to re-orient the user, and then ask a natural follow-up question to continue the brainstorming."
            )
            print(f"AI: {response}")
            self.conversation_history.append({"role": "assistant", "content": response})

        # Main conversation loop
        while True:
            user_input = input("You: ")
            if user_input.lower() in ["exit", "quit", "end", "goodbye", "bye"]:
                break

            self.conversation_history.append({"role": "user", "content": user_input})

            response = self._get_agent_response()
            print(f"AI: {response}")
            self.conversation_history.append({"role": "assistant", "content": response})

        self._save_conversation_history()

    def _save_conversation_history(self):
        """
        Saves the conversation history to a file.
        """
        if not os.path.exists("sessions"):
            os.makedirs("sessions")

        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"sessions/conversation_{timestamp}.json"

        with open(filename, "w") as f:
            json.dump(self.conversation_history, f, indent=4)

        print(f"\nAI: This has been a great session. Thanks for sharing your story with me. Our conversation has been saved to {filename}")

    def _get_agent_response(self, extra_prompt=None):
        """
        Gets a response from the OpenAI API based on the conversation history.
        """
        messages = list(self.conversation_history)
        if extra_prompt:
            messages.append({"role": "system", "content": extra_prompt})

        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            temperature=0.7,
            max_tokens=150,
        )
        return response.choices[0].message.content 