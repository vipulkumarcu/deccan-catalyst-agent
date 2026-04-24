from agents.catalyst_agent import CatalystAgent

def main():
    # Initialize our agent
    agent = CatalystAgent()

    print("--- Catalyst AI Agent Active ---")
    print("(Type 'exit' to stop)")

    while True:
        user_msg = input("\nYou: ")

        if user_msg.lower() in ["exit", "quit", "bye"]:
            print("Shutting down... Good luck with the hackathon!")
            break

        # The Brain processes the message
        reply = agent.chat(user_msg)

        print(f"\nAgent: {reply}")

if __name__ == "__main__":
    main()