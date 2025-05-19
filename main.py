# 1. Install requests (usually preinstalled in Colab)
!pip install requests

import requests
import groq
from typing import List, Dict

# ✅ Set your Groq API key directly here
groq_api_key = "ENTER YOUR OWN QROQ API KEY HERE"  # <-- Replace with your valid Groq key

# ✅ Initialize the Groq client
groq_client = groq.Client(api_key=groq_api_key)

# ✅ Serper API key
serper_api_key = "ENTER YOUR OWN SERPER API KEY HERE"  # Replace if needed

def web_search(query: str) -> List[Dict]:
    headers = {
        "X-API-KEY": serper_api_key,
        "Content-Type": "application/json"
    }
    data = {
        "q": query,
        "gl": "us",
        "hl": "en"
    }
    try:
        response = requests.post("https://google.serper.dev/search", json=data, headers=headers)
        response.raise_for_status()
        result = response.json()
        return result.get("organic", [])
    except Exception as e:
        print(f"Serper API error: {e}")
        return []

class MarketingStrategistAgent:
    def __init__(self, model: str = "llama3-70b-8192"):
        self.model = model
        self.system_prompt = (
            "You are a world-class Marketing Strategist AI Agent. "
            "Your task is to conduct market research, competitor analysis, campaign planning, content ideation, budget optimization, "
            "and performance tracking strategies. Provide actionable, data-driven recommendations."
        )
        self.history = []

    def chat(self, user_message: str) -> str:
        trigger_keywords = ["competitor", "competition", "market research", "top tools", "best platforms", "industry trends"]

        if any(keyword in user_message.lower() for keyword in trigger_keywords):
            search_results = web_search(user_message)
            if search_results:
                summary = "Based on recent web search results:\n"
                for i, item in enumerate(search_results[:3], start=1):
                    title = item.get("title", "No title")
                    snippet = item.get("snippet", "")
                    link = item.get("link", "")
                    summary += f"{i}. {title}\n   {snippet}\n   {link}\n"
                self.history.append({"role": "system", "content": f"Use this web search data to assist your reply:\n{summary}"})
            else:
                self.history.append({"role": "system", "content": "No relevant web search data was found."})

        messages = [{"role": "system", "content": self.system_prompt}]
        messages.extend(self.history)
        messages.append({"role": "user", "content": user_message})

        response = groq_client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.7,
            max_tokens=800
        )
        reply = response.choices[0].message.content.strip()

        self.history.append({"role": "user", "content": user_message})
        self.history.append({"role": "assistant", "content": reply})

        return reply

    def run(self):
        print("\n🧠 Marketing Strategist AI Agent is online with Serper web search! Type 'exit' to quit.\n")
        while True:
            user_input = input("You: ")
            if user_input.lower() in ["exit", "quit"]:
                print("Agent: Goodbye! Happy marketing. 📈")
                break
            reply = self.chat(user_input)
            print(f"Agent: {reply}\n")

if __name__ == "__main__":
    agent = MarketingStrategistAgent()
    agent.run()
