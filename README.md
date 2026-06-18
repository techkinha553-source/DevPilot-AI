🚀 DevPilot AI

An AI-powered codebase assistant that allows developers to upload a project repository and ask natural language questions about the codebase.

DevPilot AI analyzes source code, creates vector embeddings, performs semantic search, and generates intelligent answers using a local Large Language Model (LLM).

⸻

✨ Features

Repository Upload

* Upload project repositories as ZIP files
* Automatic extraction of repository contents
* Support for multiple programming languages

Code Parsing

* Reads source files from uploaded repositories
* Extracts meaningful code content
* Builds a searchable knowledge base

Local Embeddings

* Uses Sentence Transformers
* No OpenAI embedding costs
* Fast local vector generation

Semantic Search

* Finds the most relevant files for a question
* Context-aware code retrieval
* Retrieval-Augmented Generation (RAG)

AI Code Assistant

Ask questions such as:

* Where is authentication implemented?
* What does this project do?
* Explain the database schema.
* How does user login work?
* Which file contains API routes?
* Explain the project architecture.

Local LLM Support

Powered by Ollama + Qwen3

Benefits:

* No API cost
* Unlimited usage
* Privacy-friendly
* Runs locally on your machine

⸻

🏗 Architecture

User Uploads ZIP
↓
Repository Extraction
↓
Document Loader
↓
Sentence Transformers Embeddings
↓
Vector Store
↓
Relevant Context Retrieval
↓
Qwen3 (Local LLM)
↓
Answer Generation

⸻

🛠 Tech Stack

Backend

* Python
* FastAPI
* Uvicorn

AI / ML

* Sentence Transformers
* Ollama
* Qwen3

Data Processing

* ZipFile
* Pathlib
* UUID

Storage

* In-Memory Repository Store
* Vector Embeddings

⸻

📂 Project Structure

devpilot-ai/
│
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── upload.py
│   │   │   ├── chat.py
│   │   │   └── repository.py
│   │   │
│   │   ├── services/
│   │   │   ├── embedding_service.py
│   │   │   ├── rag_builder.py
│   │   │   ├── openai_service.py
│   │   │   └── repository_store.py
│   │   │
│   │   └── main.py
│   │
│   ├── uploads/
│   └── .env
│
├── frontend/
│
└── README.md

⸻

⚙️ Prerequisites

Before running the project, install:

Python

Version:

Python 3.11+

Ollama

Download:

https://ollama.com

Install and verify:

ollama --version

Qwen3 Model

Pull the model:

ollama pull qwen3

Verify:

ollama list

⸻

🚀 Installation

Clone Repository

git clone https://github.com/yourusername/devpilot-ai.git
cd devpilot-ai

⸻

Create Virtual Environment

Mac/Linux

python3 -m venv .venv
source .venv/bin/activate

Windows

python -m venv .venv
.venv\Scripts\activate

⸻

Install Dependencies

pip install -r requirements.txt

⸻

▶️ Run Backend

Navigate:

cd backend

Start server:

uvicorn app.main:app --reload

Server:

http://127.0.0.1:8000

Swagger Docs:

http://127.0.0.1:8000/docs

⸻

📤 Upload Repository

Endpoint:

POST /upload

Upload:

ZIP file of repository

Response:

{
  "repository_id": "123abc",
  "total_files": 15,
  "documents_loaded": 15
}

Save the repository_id.

⸻

💬 Ask Questions

Endpoint:

POST /chat

Request:

{
  "repository_id": "123abc",
  "question": "Where is authentication implemented?"
}

Response:

{
  "answer": "Authentication is implemented in auth.py..."
}

⸻

📚 Supported Questions

Examples:

What does this project do?
Explain the architecture.
Where are API routes defined?
How does authentication work?
Which file handles database connections?
Summarize the repository.

⸻

🔒 Privacy

All repository processing happens locally.

Benefits:

* No source code sent to external services
* No OpenAI dependency required
* Developer-friendly privacy

⸻

🧪 Future Roadmap

Phase 8

* GitHub Repository Import
* GitHub URL Analysis

Phase 9

* Frontend Dashboard
* Repository Management UI

Phase 10

* Multi-Repository Search
* Cross-Repository Analysis

Phase 11

* Code Explanation Mode
* Bug Detection
* Refactoring Suggestions

Phase 12

* Deployment
* Docker Support
* Cloud Hosting

⸻

🤝 Contributing

Contributions are welcome.

Steps:

1. Fork repository
2. Create feature branch
3. Commit changes
4. Push branch
5. Open Pull Request

⸻

👨‍💻 Author

Nikhil Kinha

B.Tech CSE Student

VIT Bhopal University

Interested in AI, Machine Learning, Full Stack Development, and Developer Productivity Tools.

⸻

⭐ Support

If you find this project useful:

⭐ Star the repository

🍴 Fork the repository

🛠 Contribute to the project

📢 Share with other developers