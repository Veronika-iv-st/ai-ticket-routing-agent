
import os
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import Runnable
from sklearn.metrics.pairwise import cosine_similarity

load_dotenv()

DEPARTMENTS = {
    "technical support": "technical_support.txt",
    "human resources": "human_resources.txt",
    "operations": "operations.txt"
}

# 🧠 LLM-based classifier with clear responsibilities
llm_model = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)

prompt = PromptTemplate.from_template("""
Classify the following internal message into one of these three departments, based on the real-world tasks each one handles:

- technical support: issues related to computers, laptops, networks, email, software, digital tools, tech devices, internet access, systems, or printers.

- human resources: manages internal staff matters like payroll, vacations, absences, employee contracts, sick leave, attendance, permissions, or workplace conflicts.

- operations: handles strategic and external topics like client issues, vendor contracts, sales, deal closures, business reports, external documentation, or third-party relationships.

Message: {ticket}

Respond with only one lowercase word:
technical support, human resources or operations.
""")

ticket_classifier: Runnable = prompt | llm_model | (lambda x: x.content.strip().lower())

def classify_department(ticket: str) -> str:
    return ticket_classifier.invoke({"ticket": ticket})

def load_tickets_and_names(file_path: str) -> list[tuple[list[str], str]]:
    """Returns a list of tuples: ([names], ticket_content)"""
    if not os.path.exists(file_path):
        return []
    result = []
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line.startswith("[") and "]" in line:
                names, text = line.split("]", 1)
                names = [n.strip() for n in names[1:].split(",") if n.strip()]
                result.append((names, text.strip()))
    return result

def save_all_tickets(file_path: str, data: list[tuple[list[str], str]]):
    with open(file_path, "w", encoding="utf-8") as f:
        for names, text in data:
            line = f"[{', '.join(names)}] {text}"
            f.write(line.strip() + "\n")

def build_faiss_index(tickets: list[str], embeddings) -> FAISS:
    docs = [Document(page_content=t) for t in tickets]
    return FAISS.from_documents(docs, embeddings)

def find_similar(ticket: str, faiss_index, embeddings, threshold: float = 0.90):
    if not faiss_index:
        return None
    ticket_embedding = embeddings.embed_query(ticket)
    results = faiss_index.similarity_search_by_vector(ticket_embedding, k=1)
    if not results:
        return None

    similarity = cosine_similarity(
        [ticket_embedding],
        [embeddings.embed_query(results[0].page_content)]
    )[0][0]

    if similarity >= threshold:
        return results[0].page_content
    return None

def process_ticket(ticket: str, employee: str):
    embeddings = OpenAIEmbeddings()
    department = classify_department(ticket)
    file_path = f"data/{DEPARTMENTS[department]}"

    # Load existing tickets
    named_tickets = load_tickets_and_names(file_path)
    ticket_texts = [t[1] for t in named_tickets]

    faiss_index = build_faiss_index(ticket_texts, embeddings) if ticket_texts else None
    duplicate = find_similar(ticket, faiss_index, embeddings)

    if duplicate:
        updated = []
        for names, text in named_tickets:
            if text == duplicate:
                if employee not in names:
                    names.insert(0, employee)
                updated.append((names, text))
            else:
                updated.append((names, text))
        save_all_tickets(file_path, updated)
        return f"A similar ticket already exists:\n“{duplicate}”", department

    # New ticket
    named_tickets.append(([employee], ticket))
    save_all_tickets(file_path, named_tickets)
    return "Ticket successfully saved.", department

if __name__ == "__main__":
    employee = input("Employee name: ")
    ticket = input("Submit your ticket: ")
    result, department = process_ticket(ticket, employee)
    print("\n✅ Result:", result)
    print("📂 Assigned department:", department)
