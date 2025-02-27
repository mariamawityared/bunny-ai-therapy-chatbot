from flask import Flask, request, jsonify
import random

class TherapyChatbot:
    def __init__(self, use_openai=False, openai_key=None):
        """
        Initialize the therapy chatbot.
        """
        self.use_openai = use_openai and openai_key is not None
        self.memory = {}  # Stores user responses
        self.state = "intro"  # Start with an introduction
        self.exit_triggers = ["no", "nothing else", "that's all", "i'm good now", "all done", "nope"]
        self.closing_responses = ["bye", "goodbye", "you too", "thanks, you too", "take care", "i'm done, bye"]
        self.greeting_responses = ["hi", "hello", "hey", "what's up"]
        self.emotions = {
            "happy": ["happy", "great", "good", "excited", "joyful", "fantastic", "amazing", "wonderful"],
            "neutral": ["okay", "alright", "fine", "not sure", "i don't know", "maybe"],
            "anxiety": ["anxious", "nervous", "worried", "overwhelmed", "uneasy"],
            "stress": ["stressed", "burned out", "exhausted", "frustrated", "pressured"],
            "depression": ["depressed", "sad", "down", "hopeless", "lost"],
            "loneliness": ["lonely", "alone", "isolated", "disconnected"],
            "confusion": ["confused", "unsure", "uncertain", "lost"],
            "hopeful": ["hopeful", "optimistic", "relieved", "grateful"]
        }
        self.predefined_responses = {
            "anxiety": "I hear you. Anxiety can feel overwhelming, but it’s temporary. Try this deep breathing exercise: [https://www.healthline.com/health/deep-breathing] 🌿",
            "stress": "Stress can feel consuming, but breaking things into small steps can help. You might find this helpful: [https://www.apa.org/topics/stress] ✨",
            "depression": "You are not alone. Talking about what you’re feeling is a great first step. If you need more resources, check: [https://www.nimh.nih.gov/health/topics/depression] 💙",
            "loneliness": "Feeling lonely is tough, but even small connections can help. Maybe reaching out to someone or journaling your thoughts could make a difference. 💞",
            "confusion": "Uncertainty is part of growth. If you're feeling lost, grounding yourself in the present moment may help. What’s something that’s been on your mind? 🌀",
            "hopeful": "Hope is powerful. I love that you're holding onto it! What’s something you’re looking forward to? 🌟"
        }
        self.recommendations = {
            "anxiety": ["Song: 'Weightless' by Marconi Union 🎵", "Movie: 'Inside Out' (2015) 🎬", "Art: 'The Starry Night' by Vincent van Gogh 🎨"],
            "stress": ["Song: 'Clair de Lune' by Debussy 🎶", "Movie: 'The Secret Life of Walter Mitty' (2013) 🎥", "Art: 'Water Lilies' by Monet 🌿"],
            "depression": ["Song: 'Here Comes the Sun' by The Beatles ☀️", "Movie: 'Soul' (2020) 🎬", "Art: 'Girl with a Pearl Earring' by Vermeer 💎"],
            "loneliness": ["Song: 'Lean on Me' by Bill Withers 🎶", "Movie: 'Cast Away' (2000) 🎬", "Art: 'The Lovers' by René Magritte 💞"],
            "confusion": ["Song: 'Lost Stars' by Adam Levine 🎵", "Movie: 'Eternal Sunshine of the Spotless Mind' (2004) 🎬", "Art: 'The Persistence of Memory' by Salvador Dalí 🌀"],
            "hopeful": ["Song: 'Don't Stop Believin'' by Journey 🌈", "Movie: 'The Pursuit of Happyness' (2006) 🎬", "Art: 'Impression, Sunrise' by Claude Monet 🌅"]
        }

    def get_response(self, user_input):
        """
        Generate a response based on user input.
        """
        text = user_input.lower().strip()

        # **🚪 Immediate Exit if User Says "I'm done, bye"**
        if text in self.closing_responses:
            return ""  # Empty response = No further conversation; chat ends immediately

        # **🐰 Step 1: Respond to "Hi" or "Hello"**
        if text in self.greeting_responses:
            return "Hi there! 😊 How can I assist you today?"

        # **🐰 Step 2: Bunny's Introduction**
        if self.state == "intro":
            self.state = "waiting_for_feeling"
            return "Hi! I’m Bunny, your therapist in your phone! 🌸 How would you say you’re feeling today? 😊"

        # **🤖 Step 3: Recognize and Respond to Emotions**
        for emotion, keywords in self.emotions.items():
            if any(word in text for word in keywords):
                self.memory["emotion"] = emotion
                self.state = "providing_advice"
                return f"I hear you. {self.predefined_responses.get(emotion, 'Your feelings are valid. Let’s talk about what might help. 💛')}"

        # **📝 Step 4: If User Journals/Vents, Validate & Encourage**
        if len(text.split()) > 20:  # If user writes a longer response, assume it’s journaling
            self.state = "closing_prompt"
            return "That was lovely of you to share. Thank you for opening up. Expressing yourself like this can help you process emotions and feel lighter. Is there anything else on your mind? 💬"

        # **💡 Step 5: If Input Isn’t Recognized, Move the Conversation Forward**
        self.state = "closing_prompt"
        return "I'm glad we talked. Is there anything else on your mind before we wrap up? 💬"

        # **👋 Step 6: If User Says No, Close Chat Gracefully**
        if self.state == "closing_prompt" and text in self.exit_triggers:
            self.state = "final_goodbye"
            return "I’m really glad we got to chat today! 💛 Remember, you matter. I’m always here if you need me. Take care! 🐰✨"

        # **🎵 Step 7: End Chat with Thoughtful Goodbye & Recommendation**
        if self.state == "final_goodbye" and text in self.closing_responses:
            emotion = self.memory.get("emotion", "general")
            rec = random.choice(self.recommendations.get(emotion, ["A nice walk outside might help. 🌿"]))
            return f"Before you go, here’s something that might bring you joy: {rec} \nTake care! 🐰✨"

        return "I'm here to listen. Feel free to share more. 💛"

# **🐰 CLI Mode**
if __name__ == "__main__":
    bot = TherapyChatbot()
    print(bot.get_response(""))  # Start with the introduction
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit", "bye", "i'm done, bye"]:
            print("Bunny: Take care! I'm always here if you need me. 🐰💖")
            break
        response = bot.get_response(user_input)
        if response == "":
            break  # Stops chat if Bunny detects a final goodbye
        print("Bunny:", response)
