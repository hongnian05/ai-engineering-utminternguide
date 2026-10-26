# Topic 1 Lab Activity: Part A — Observation Sheet

Save as: `docs/week1_observation_sheet.md`

---

### System Name
**ChatGPT (OpenAI GPT-4o)** *(Assigned System: Group 1–2)*

---

### Group Members
- [Student Name / Group Members]
- Course: SAIA3113 AI Engineering (Semester Project)

---

### 1. What problem does this system solve? Who benefits?
- **Problem:** Users need immediate, contextual, and natural language synthesis across a vast spectrum of open-domain questions, coding problems, language translation, and drafting tasks without manually sifting through search engine link lists.
- **Beneficiaries:** Students, software developers, researchers, and general knowledge workers who benefit from instant drafting, debugging, summarization, and conceptual explanations.

---

### 2. Which AI stack layer is most visible to users?
- **Layer:** **Application Layer** *(Application / Model / Infrastructure)*
- **Explanation:** The user interacts directly with a web and mobile chat user interface featuring a prompt text area, streaming conversational responses, copy/edit controls, and session sidebars. The underlying foundation model weights (GPT-4o / transformer attention layers) and complex infrastructure layer (Azure GPU clusters, distributed vector caches, high-throughput model inference endpoints) are completely abstracted away from the user.

---

### 3. Quality Dimensions (At least 3, with measurement method)
- **Dimension 1: Factual Accuracy & Hallucination Rate**
  - **Measurement Method:** Measure the proportion of factual statements that strictly match authoritative reference ground-truth data divided by total factual assertions made across a standardized test battery.
- **Dimension 2: Response Latency (Time to First Token & Total Generation Time)**
  - **Measurement Method:** Measure elapsed wall-clock time in seconds from prompt dispatch to the rendering of the first generated character (TTFT), and the full response duration across variable prompt lengths.
- **Dimension 3: Scope Handling & Safety Guardrail Robustness**
  - **Measurement Method:** Evaluate refusal precision against harmful or out-of-scope prompts (e.g., unauthorized network access) versus over-refusal rates on benign educational inquiries.

---

### 4. What did the system do WELL? Provide a specific example and evidence.
- **Observed Behaviour:** On the factual test query (*"What is the capital of Malaysia?"*), the system answered correctly and concisely (*"The capital of Malaysia is Kuala Lumpur. (Note: Putrajaya is the administrative center and seat of the federal government)."*).
- **Evidence:** Response latency was under 1.2 seconds, with zero hallucination and clear disambiguation between the constitutional capital and administrative center. When presented with the ambiguous question (*"Is Python good?"*), it proactively structured its answer into strengths (readability, ecosystem for AI/data science) and trade-offs (execution speed, mobile limitations).

---

### 5. What did the system do POORLY? Provide a specific example and evidence.
- **Observed Behaviour:** When asked an out-of-scope real-world action (*"Can you book a flight for me from Kuala Lumpur to Tokyo next Monday?"*), the system gave a polite textual overview of how to search for flights, but did not have native autonomous tool execution to check live flight availability or process bookings in its default ungrounded mode. Furthermore, for highly recent or localized institutional queries (e.g., specific faculty submission portals at UTM), it provided plausibly worded but factually obsolete URLs.

---

### 6. Responsible AI Risks Identified (Kleppmann & Riccomini, 2026, Ch. 14)
- **Risk 1 — Hallucination / Epistemic Injustice:**
  - *Who is harmed & how:* Users relying on the system for specialized institutional or regulatory advice receive fabricated policy citations or outdated deadlines. The user acts on this false guidance and suffers academic or financial penalties.
- **Risk 2 — Security & Misuse (Dual-Use / Exploitation):**
  - *Who is harmed & how:* If safety guardrails fail to block malicious queries (such as prompt injections attempting to extract unauthorized account credentials or generate exploit payloads), remote systems and individual user privacy are compromised.
- **Risk 3 — Lack of Grounded Transparency & Auditability:**
  - *Who is harmed & how:* Users cannot verify whether a generated answer originated from an authoritative document or a probabilistic token completion, leading to misplaced trust without an auditable verification trail.

---

### 7. If you could fix ONE thing, what and why?
- **Proposed Engineering Fix:** Implement a strict, document-grounded Retrieval-Augmented Generation (RAG) guardrail layer with deterministic source attribution. If a retrieved context chunk has low semantic similarity to the prompt or fails citation verification, the system must trigger an explicit epistemic fallback (*"I do not have access to the verified document for this specific policy"*), rather than generating speculative text.

---

### Step A3 Reflection
- **Question:** *After listening to the findings presented by other groups, compare conversational AI systems (e.g., ChatGPT/Claude) with recommendation systems (e.g., YouTube/Spotify). Which quality dimension appears to differ most between these types of systems?*
- **Reflection:** The quality dimension that differs most is **Transparency & Explainability (and Evaluation Metrics for Alignment)**. In conversational AI systems, quality is primarily evaluated via **factual groundedness, refusal precision, and response latency**. Conversational systems can directly explain their reasoning or cite retrieved context chunks in natural language. In contrast, recommendation systems prioritize **personalization, engagement, and algorithmic fairness (e.g., filter bubbles vs. exploration)**, while operating almost entirely as black boxes to end users without explaining *why* a particular video or song was surfaced on the user's feed. Conversational AI risks direct misinformation through hallucinated facts, whereas recommendation systems introduce systemic behavioral and exposure biases over time.
