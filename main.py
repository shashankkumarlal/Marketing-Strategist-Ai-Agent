# Marketing Strategist AI Agent (using Groq API)
# Paste this into Google Colab and run

# 1. Install dependencies
!pip install --quiet groq

# 2. Set up Groq API key directly (no .env required)
import os
from typing import List, Dict
import groq

# ✅ Set your Groq API key directly here
groq_api_key = "ENTER YOUR OWN GROQ API KEY"  # <-- Replace with your valid Groq key

# ✅ Initialize the Groq client
groq_client = groq.Client(api_key=groq_api_key)

# 3. Define the Marketing Strategist Agent class
class MarketingStrategistAgent:
    def __init__(self, model: str = "llama3-70b-8192"):  # or try: "mixtral-8x7b-32768"
        self.model = model
        self.system_prompt = (
            "You are a world-class Marketing Strategist AI Agent. "
            "Your task is to conduct market research, competitor analysis, campaign planning, content ideation, budget optimization, "
            "and performance tracking strategies. Provide actionable, data-driven recommendations, but in a brief short and accurate to the point manner without using much unnecessary words."
        )

    def chat(self, user_message: str, history: List[Dict] = None) -> str:
        messages = []
        messages.append({"role": "system", "content": self.system_prompt})
        if history:
            messages.extend(history)
        messages.append({"role": "user", "content": user_message})

        response = groq_client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.7,
            max_tokens=800
        )
        return response.choices[0].message.content.strip()

    def run(self):
        print("\n🧠 Marketing Strategist AI Agent is online via Groq! Type 'exit' to quit.\n")
        history = []
        while True:
            user_input = input("You: ")
            if user_input.lower() in ["exit", "quit"]:
                print("Agent: Goodbye! Happy marketing. 📈")
                break
            reply = self.chat(user_input, history)
            print(f"Agent: {reply}\n")
            history.append({"role": "user", "content": user_input})
            history.append({"role": "assistant", "content": reply})

# 4. Instantiate and run the agent
if __name__ == "__main__":
    agent = MarketingStrategistAgent()
    agent.run()

