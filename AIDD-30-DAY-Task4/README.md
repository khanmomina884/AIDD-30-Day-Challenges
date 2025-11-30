# PDF Summarizer & Quiz Generator

This project is a Streamlit web application that uses Google's Gemini generative AI to analyze PDF documents. It provides a concise summary, extracts key learning points, and automatically generates a quiz to test comprehension.

## 🌟 Features

- **PDF Text Extraction**: Upload any PDF file and the application will extract its text content using PyPDF2.
- **AI-Powered Summarization**:
  - Generates a short summary (5-7 lines).
  - Identifies 5 key takeaways.
  - Creates 3 study questions to guide learning.
- **Automatic Quiz Generation**:
  - Produces 5 Multiple Choice Questions (MCQs) with options and correct answers.
  - Generates 3 short-answer questions.
  - Delivers all quiz content in a clean, structured JSON format.
- **Interactive UI**: A user-friendly interface built with Streamlit that allows for easy file uploads and displays results in an organized manner.

## 📂 Project Structure

```
.
├── agent.py              # Core logic for PDF processing and AI interaction.
├── streamlit_app.py      # Main Streamlit application file for the UI.
├── requirements.txt      # Python dependencies for the project.
└── README.md             # This file.
```

## 🚀 Getting Started

Follow these steps to set up and run the project locally.

### 1. Prerequisites

- Python 3.8 or higher.
- A Google Gemini API Key. You can obtain one from [Google AI Studio](https://aistudio.google.com/app/apikey).

### 2. Installation

Clone the repository or download the source code into a local directory.

**Create a virtual environment:**

It is highly recommended to use a virtual environment to manage dependencies.

```bash
# For Windows
python -m venv venv
.\venv\Scripts\activate

# For macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

**Install the required packages:**

```bash
pip install -r requirements.txt
```

### 3. Configuration

This application requires a Google Gemini API key to function. The Streamlit interface provides a secure input field to enter your API key directly, so you do not need to set up a `.env` file.

## ▶️ How to Run the Project

With your virtual environment activated and dependencies installed, run the following command in your terminal:

```bash
streamlit run streamlit_app.py
```

Your web browser will automatically open a new tab with the running application.

1.  **Enter your API Key** in the sidebar.
2.  **Upload a PDF file**.
3.  Click the **"Generate Insights"** button.
4.  View the generated summary, key points, and quiz in the main panel.

---

Built with Python, Streamlit, and Google Gemini.
