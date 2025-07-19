                                                           Bluewisdom Chatbot ✨

Welcome to BlueWisdom, a modern and intelligent conversational AI chatbot built with Python and Streamlit. Powered by the Google Gemini API, Bluwidom offers a sleek, professional dark-themed interface for seamless interaction, featuring both text and voice input, along with multi-chat session management.


-> Features
  1. Intelligent Conversations: Leverages the power of the Google Gemini API (gemini-1.5-flash) for fast, accurate, and context-aware responses.

  2. Professional UI: A sophisticated dark-themed interface designed for a comfortable and immersive user experience.

  3. Voice-to-Text: Includes an "Ask with Voice" feature that uses your microphone to transcribe speech into text prompts.

  4. Multi-Chat Management:

  5. I Start new conversations at any time.

  6. Previous chats are saved in a history sidebar.

  7. Seamlessly switch between different chat sessions to continue where you left off.

  8. Secure API Key Handling: Your API key is handled securely within the session and is never stored in the code.

-> Technologies Used
 - Backend: Python

 - Frontend: Streamlit

 - AI Model: Google Gemini API (google-generativeai)

 - Voice Recognition: SpeechRecognition

 - Microphone Access: PyAudio (dependency for SpeechRecognition)

-> Getting Started
 - Follow these instructions to set up and run the project on your local machine.

->Prerequisites
 - Python 3.8 or higher

 - A Google Gemini API Key

-> Installation
  ->Clone the repository:

   - git clone https://github.com/syed-roshan-786/AI_ChatBot.git
   - cd nexusai-chatbot

-> Create and activate a virtual environment:

-> Windows:

python -m venv venv
.\venv\Scripts\activate

-> macOS / Linux:

python3 -m venv venv
source venv/bin/activate

-> Install the required libraries:
 - The requirements.txt file contains all the necessary packages. Install them with pip:

 - pip install -r requirements.txt

-> Get your API Key:

- Go to Google AI Studio.

- Sign in and click Get API key > Create API key in new project.

- Copy the generated API key.

-> Running the Application
- Run the Streamlit app from your terminal:

streamlit run app.py

-> Enter your API Key:

- The application will open in your web browser.

- Paste your Google Gemini API key into the input field at the top of the page.

-> Start Chatting:
Once the model is initialized, you can start your conversation with NexusAI!

📂 File Structure
.
├── app.py              # The main Streamlit application script
├── requirements.txt    # A list of all necessary Python packages
└── README.md           # This file

🤝 Contributing
Contributions are welcome! If you have ideas for new features or improvements, feel free to fork the repository, make your changes, and open a pull request.
