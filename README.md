# Smart-Ticket-Engine-for-Internal-Operations  
AI-driven classification, duplicate handling, and team coordination — built with FastAPI.

---

## 🧠 Overview  
This project provides a minimal yet powerful internal ticketing solution powered by OpenAI's GPT-3.5.  
Designed for small to medium-sized businesses, the system enables employees to submit issues or requests through a user-friendly interface. The ticket is automatically classified by department using AI, and duplicate tickets are detected and consolidated.

> **🧩 Open Project**  
This is a living project under active development.  
We welcome contributions, ideas, improvements, or redesigns to take this system to the next level.

---

## 🖼️ Preview  
Here’s a visual preview of the Smart Ticket Engine interface in action:

![Smart Ticket Interface](media/Captura%20de%20pantalla%202025-06-24%20222440.png)

The system enhances internal communication, reduces redundant tasks, and ensures teams only work on relevant, verified incidents.

---

## 🔧 Key Features

### ✅ AI-Based Department Classification  
When an employee submits a new ticket, GPT-3.5 evaluates the message and determines whether it belongs to:

- **Operations**: Issues related to customers, provider contracts, sales, contract closures, or business reports.  
- **Technical Support**: Requests about malfunctions, equipment, software, or hardware.  
- **Human Resources**: Inquiries about personal documents, salaries, leaves, team conflicts, or internal HR policies.

### 🧠 Smart Duplicate Detection  
Each new ticket is compared in real-time with past messages from the same department. If the issue has already been reported, the system:
- Notifies that the ticket is a duplicate  
- Appends the reporting employee's name to the existing ticket  
  (helping track how many people are affected by the same issue)

### 📝 File-Based Storage for Simplicity  
No database. Each department has its `.txt` file:
- Easy to edit manually  
- Easy to deploy and maintain  
- New vector index is regenerated after each ticket

---

## 🌐 Clean Web Interface

The app offers a simple interface with:
- Text input for ticket content  
- Field to enter the employee name  
- Visual confirmation of ticket processing and classification

🎨 **Looking to improve the UI/UX** — Frontend contributions are welcome!

---

## ⚙️ Installation & Setup

### 📁 1. Clone the Repository

```bash
git clone https://github.com/Veronika-iv-st/ai-ticket-routing-agent.git
cd ai-ticket-routing-agent
```

### 🐍 2. Create and Activate a Virtual Environment

```bash
python -m venv venv
.\venv\Scripts\activate       # On Windows
# source venv/bin/activate   # On macOS/Linux
```

### 📦 3. Install Required Dependencies

```bash
pip install fastapi uvicorn langchain langchain-openai langchain-community scikit-learn python-dotenv jinja2
```

> Make sure you're using **LangChain 0.3+** and GPT 3.5 or later via `langchain-openai`.

### 🔑 4. Set Your OpenAI API Key

Create a `.env` file in the root folder with the following:

```env
OPENAI_API_KEY=your_openai_api_key_here
```

---

## 📁 Project Structure

```
.
├── app/
│   ├── main.py                 # FastAPI app and endpoints
│   ├── core.py                 # Ticket processing and classification logic
│   └── templates/
│       └── index.html          # Frontend interface
├── data/                       # Ticket files per department (editable manually)
│   ├── operaciones.txt
│   ├── soporte_tecnico.txt
│   └── recursos_humanos.txt
├── media/                      # Screenshots or media (optional)
│   └── Captura de pantalla 2025-06-24 222440.png
├── .env                        # Contains your OpenAI API key
├── requirements.txt            # Optional - for saving dependencies
└── README.md
```

---

## 🔄 How It Works (Step-by-Step)

1. The employee submits a ticket via web form (name + issue).
2. The ticket is sent to GPT-3.5 via LangChain using a prompt that defines departmental responsibilities.
3. The model classifies it into a department.
4. The corresponding `.txt` file is loaded and checked for semantic duplicates using FAISS + cosine similarity.
5. If a match is found → the employee’s name is added.
6. If not → a new line is saved.
7. Each submission triggers live vector re-indexing.

---

## 🏢 Adaptability to Any Company

- 🔁 No database required — lightweight and editable `.txt` storage  
- 💼 Scalable logic — redefine prompts, expand departments  
- 🧩 Fully customizable — adjust to your internal process  
- ✅ Manual validation — just delete a line to mark a task as completed

---

## 🌟 Key Benefits

- ✅ Zero database overhead  
- 🧠 AI-powered triage with GPT-3.5  
- 📌 Live duplicate tracking  
- 🧑‍🤝‍🧑 Track team-wide issues  
- 🔧 Manual control with editable files  
- 🌐 Fully local and dependency-light

---

## 🚀 Future Roadmap & Community Involvement

> This project is open for collaboration — help us grow it together!

Here are some improvements we’re considering:
- 🧭 Admin dashboard to manage tickets
- 🖼️ Web interface redesign and theming
- 📊 Analytics or stats dashboard
- 🗃️ Optional database for larger deployments
- 🧠 Enhanced prompt tuning or multilingual support

---

## 🤝 How to Contribute

- 🌟 Star the repo to show support  
- 🐛 Open an issue to suggest a feature or report a bug  
- 🔧 Fork and submit a Pull Request  
- 🎨 Help improve the frontend interface  
- 📥 Share ideas in the Discussions tab

Let’s build something that small teams can really use in production.
