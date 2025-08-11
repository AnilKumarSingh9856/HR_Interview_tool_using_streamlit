🤖 AI Interview Coach
An interactive, AI-powered interview simulator built with Streamlit and the high-speed Groq API. This tool allows users to practice for behavioral interviews, customize the interview scenario, and receive instant, actionable feedback on their performance.

✨ Key Features
🚀 Blazing-Fast Responses: Powered by the Groq LPU™ Inference Engine for a seamless, real-time conversation.

** customizable Scenarios:** Tailor the interview by setting your name, experience, skills, target role, and company.

📊 Adjustable Difficulty: Choose between Easy, Medium, and Difficult question levels to match your preparation needs.

🗣️ Behavioral Focus: The AI acts as an HR executive, asking non-technical questions to evaluate soft skills.

📈 Instant Performance Feedback: After a 5-question interview, receive a detailed performance review and an overall score out of 10.

🎨 Modern & Intuitive UI: A clean, visually appealing interface built with Streamlit for a great user experience.

🛠️ Tech Stack
Framework: Streamlit

Language: Python 3.9+

LLM API: Groq

⚙️ Setup and Installation
Follow these steps to get the AI Interview Coach running on your local machine.

1. Clone the Repository
git clone [https://github.com/your-username/ai-interview-coach.git](https://github.com/your-username/ai-interview-coach.git)
cd ai-interview-coach

2. Create a Virtual Environment
It's recommended to use a virtual environment to manage dependencies.

# For Windows
python -m venv venv
venv\Scripts\activate

# For macOS/Linux
python3 -m venv venv
source venv/bin/activate

3. Install Dependencies
Install all the required Python packages from the requirements.txt file.

pip install -r requirements.txt

(Note: If you don't have a requirements.txt file yet, you can create one by running pip freeze > requirements.txt after installing the necessary libraries like streamlit and groq.)

4. Configure Your API Key
This project requires a Groq API key.

Create a folder named .streamlit in the root of your project directory.

Inside this folder, create a file named secrets.toml.

Add your Groq API key to the secrets.toml file like this:

GROQ_API_KEY="your_api_key_here"

Important: The .gitignore file is already configured to ignore the .streamlit/secrets.toml file, ensuring your API key is not accidentally pushed to GitHub.

5. Run the Streamlit App
Launch the application from your terminal:

streamlit run app.py

Your web browser should open with the application running!

🚀 How to Use
Fill in Your Details: Complete the setup form with your personal information, target role, and desired interview difficulty.

Start the Interview: Click the "Start Interview" button to begin. The AI will ask you the first of five questions.

Answer the Questions: Type your answers into the chat input at the bottom.

Get Feedback: Once you've answered all five questions, a "Get Feedback" button will appear. Click it to receive your performance analysis.

Restart: You can choose to restart the interview with the same details or edit your information for a new scenario.

🤝 Contributing
Contributions, issues, and feature requests are welcome! Feel free to check the issues page.

📄 License
This project is licensed under the MIT License. See the LICENSE file for details.
