#  ResolveIQ

<p align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&color=0:0E1117,100:1c1f26&height=200&section=header&text=ResolveIQ&fontSize=40&fontColor=ffffff&animation=fadeIn" />
</p>
![Python](https://img.shields.io/badge/Python-3.11-blue)
![Streamlit](https://img.shields.io/badge/Framework-Streamlit-red)
![AI](https://img.shields.io/badge/AI-Generative-green)
![Database](https://img.shields.io/badge/Database-SQLite-yellow)

ResolveIQ is a web-based application that automatically analyzes and categorizes support tickets using Artificial Intelligence. It helps organizations prioritize issues, detect urgency, and visualize ticket analytics in real-time.

The application is built using **Python, Streamlit, SQLite, and Open Router API**.

---

##  Features

- 🔐 **User Authentication**
  - Login and Registration system
  - Secure user data storage using SQLite

-  **AI Ticket Analysis**
  - Uses Gemini API to analyze support tickets
  - Automatically identifies:
    - Ticket Category
    - Priority Level
    - Suggested Solution

-  **Analytics Dashboard**
  - View ticket distribution
  - Track categories and priority levels
  - Visual insights for better decision making

-  **Persistent Data Storage**
  - Tickets and users stored in SQLite database
  - Data remains even after refreshing the app

---

## 🛠️ Tech Stack

- **Frontend / UI:** Streamlit  
- **Backend:** Python  
- **Database:** SQLite  
- **AI Model:** Google Gemini API  
- **Visualization:** Streamlit Charts

## Project Structure
resolveiq/
│
├── app.py              # Main Streamlit application
├── auth.py             # Authentication logic (login/signup)
├── database.py         # Database operations (users & tickets)
├── logo.png            # Custom application logo
├── tickets.db          # SQLite database
├── requirements.txt    # Dependencies
└── README.md

## Installation & Setup

Clone the repository:

git clone https://github.com/YOUR_USERNAME/resolveiq.git
cd resolveiq

Install dependencies:

pip install -r requirements.txt

Set up environment variables:

Create a .env file and add your OpenRouter API key:

OPENROUTER_API_KEY=your_api_key_here

Run the application:

streamlit run app.py

## How It Works
User registers and logs into the system
A support ticket is submitted
AI analyzes the ticket and extracts:
Category
Priority
Sentiment
Summary
Suggested resolution
Customer reply
Ticket is stored in the database
Dashboard visualizes insights and trends
🎯 Future Enhancements
Role-based access (Admin / Support Agent)
Email notifications for critical tickets
Integration with external helpdesk tools
Deployment on cloud platforms (AWS / Streamlit Cloud)
AI-based similar ticket retrieval (RAG)

## Author

Developed by Vanshika Gupta

## Support
If you found this project useful, consider giving it a ⭐ on GitHub!


