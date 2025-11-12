# 🧠 Quizipedia – AI Wiki Quiz Generator

Transform any **Wikipedia article** into an **AI-generated quiz** instantly. Enter a Wikipedia URL → content is scraped, analyzed by an LLM, and turned into a structured quiz with questions, answers, and insights.

---

## 🚀 Overview

**Quizipedia** is a full-stack web app that blends AI and knowledge discovery.  
It takes a Wikipedia URL, scrapes the content using **BeautifulSoup**, processes it through an **LLM (via LangChain)**, and generates:
- A brief **summary**
- **Key people**, entities & topics
- **5 MCQs** with difficulty level, correct answer & explanation  
- **Related topics** for further learning

All quizzes are stored in a **MySQL** database and can be viewed later in the **History tab**.

---

## ⚙️ Tech Stack

### Frontend  
- **React.js** + **Vite** + **Tailwind CSS**  
- Responsive UI with Dark Mode  

### Backend  
- **FastAPI** (Python)  
- **BeautifulSoup4** for scraping  
- **LangChain + Gemini LLM** for AI quiz generation  
- **SQLAlchemy + MySQL** for data storage  

---

## 🔄 How It Works

```mermaid
graph TD
A[User enters Wikipedia URL] --> B[FastAPI Backend]
B --> C[Scrape Wikipedia via BeautifulSoup]
C --> D[Send to LLM via LangChain]
D --> E[Generate Quiz JSON]
E --> F[Store in MySQL]
F --> G[Return to Frontend]
G --> H[Display Quiz + History]
```


## 🧩 Example Output by Backend

```json
{
  "title": "Artificial Intelligence",
  "summary": "AI is intelligence demonstrated by machines...",
  "key_entities": {
    "people": ["Alan Turing", "John McCarthy"],
    "organizations": ["DARPA"]
  },
  "quiz": [
    {
      "question": "Who is known as the father of AI?",
      "options": ["Turing", "McCarthy", "Minsky", "Shannon"],
      "answer": "John McCarthy",
      "difficulty": "medium",
      "explanation": "He coined the term 'Artificial Intelligence'."
    }
  ],
  "related_topics": ["Machine Learning", "Robotics"]
}
```

## 🖼️ Screenshots

- Generate Quiz

<img width="1342" height="933" alt="Screenshot 2025-11-12 175755" src="https://github.com/user-attachments/assets/f2ebf3a0-7fb8-49e3-aafd-f044b9d545ca" />


- Past Quizzes (History)

<img width="1371" height="921" alt="Screenshot 2025-11-12 175818" src="https://github.com/user-attachments/assets/abd985c8-84da-4265-abcf-a6dd7c8d4d3a" />


- Quiz Details

<img width="896" height="921" alt="Screenshot 2025-11-12 175840" src="https://github.com/user-attachments/assets/2053c9fd-7df8-44e6-9258-89786c4a35b9" />


## 💬 Thank You

- Thank you for checking out Quizipedia — where Wikipedia meets AI to make learning fun and interactive.
- ⭐ Contributions, feedback, and ideas are always welcome!
