import os
import json
import fitz
from datetime import datetime

def load_persona(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)

def extract_chunks_from_pdfs(folder):
    chunks = []
    for fname in os.listdir(folder):
        if not fname.endswith(".pdf"):
            continue
        doc = fitz.open(os.path.join(folder, fname))
        for page_num in range(doc.page_count):
            text = doc.load_page(page_num).get_text()
            if text.strip():
                chunks.append({
                    "document": fname,
                    "page": page_num + 1,
                    "text": text
                })
        doc.close()
    return chunks

def score_chunks(chunks, persona, job):
    # Refined keywords based on persona and job description
    keywords = [
        "influential nodes", "network centrality", "random walk", "SIR model",
        "dismantling", "real-world", "robust", "complex networks", "diffusion",
        "performance", "IC model", "k-shell", "betweenness", "gravity model"
    ]
    persona_keywords = persona.lower().split() + job.lower().split()
    all_keywords = list(set(persona_keywords + keywords))

    scored = []
    for chunk in chunks:
        score = sum(chunk["text"].lower().count(k) for k in all_keywords)
        chunk["score"] = score
        scored.append(chunk)

    return sorted(scored, key=lambda x: -x["score"])[:5]  # top 5 relevant

def format_output(scored, persona, job):
    timestamp = datetime.utcnow().isoformat() + "Z"
    output = {
        "metadata": {
            "documents": list({c["document"] for c in scored}),
            "persona": persona,
            "job": job,
            "timestamp": timestamp
        },
        "extracted_sections": [],
        "subsection_analysis": []
    }

    for i, chunk in enumerate(scored, 1):
        output["extracted_sections"].append({
            "document": chunk["document"],
            "page": chunk["page"],
            "section_title": chunk["text"][:60].replace('\n', ' '),
            "importance_rank": i
        })
        output["subsection_analysis"].append({
            "document": chunk["document"],
            "page": chunk["page"],
            "refined_text": chunk["text"][:500].replace('\n', ' '),
            "importance_rank": i
        })

    return output

def main():
    persona_data = load_persona("input/persona.json")
    persona = persona_data["persona"]
    job = persona_data["job"]

    chunks = extract_chunks_from_pdfs("input/docs")
    scored_chunks = score_chunks(chunks, persona, job)
    output = format_output(scored_chunks, persona, job)

    os.makedirs("output", exist_ok=True)
    with open("output/result.json", "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    main()