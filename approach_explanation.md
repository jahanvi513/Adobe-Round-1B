# Adobe Hackathon Round 1B – Approach Explanation

## Overview

This solution is built to address the Round 1B challenge: to design a generic, offline-compatible system that extracts the most relevant content from a set of documents, personalized to a user's persona and job-to-be-done. Our system is designed to generalize across domains (research papers, textbooks, financial reports) and personas (researchers, students, analysts, etc.), while remaining lightweight and Docker-executable.

## Input Format

The system accepts:

* A folder containing 3 to 10 PDF documents.
* A `persona.json` file with two fields:

  * `persona`: Describes the user’s role and expertise.
  * `job`: A concrete task to be completed using the documents.

## Architecture and Pipeline

### 1. Document Parsing

We use the PyMuPDF (`fitz`) library to load and extract text from each page of every PDF. Each page becomes a text "chunk," tagged with its document name and page number.

### 2. Persona-Job Relevance Modeling

We define a scoring function that evaluates each chunk’s relevance to the persona and task. To keep the system model-free and efficient:

* We tokenize the persona and job descriptions.
* We include a curated set of domain-relevant keywords when the domain is known (e.g., network science).
* Each chunk is scored based on the frequency of these terms.

Chunks are sorted by score, and the top 5 are selected.

### 3. Output Structure

The output is saved as a `result.json` file containing:

* Metadata: Document names, persona, job, timestamp.
* Extracted Sections: Top passages with ranking and page info.
* Subsection Analysis: Full refined text of the top chunks.

This format allows downstream tasks like summarization, comparison, or further question answering.

## Generalizability

To make this approach work across domains:

* The text extraction process is domain-agnostic.
* The keyword-based scoring allows adaptation by simply updating the keyword strategy per persona/job.
* The system does not rely on internet access or external APIs, complying with the offline inference requirement.

## Test Case Implementation

For this round, we used 5 research papers on "influential node identification in complex networks."

* **Persona**: Senior Researcher in Network Science
* **Job**: Compare and extract node ranking algorithms with proven performance on real-world datasets using SIR/IC or dismantling methods.

Our scoring prioritized terms like "influential nodes," "SIR model," "real-world networks," and algorithm names like "k-shell," "betweenness," and "random walk."

## Conclusion

This solution is robust, extensible, and lightweight. It ensures consistent chunk extraction and prioritization across domains, while remaining fully compatible with Docker-based CPU-only offline inference environments.
