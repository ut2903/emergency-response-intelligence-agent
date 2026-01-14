# Emergency Response Intelligence Agent (Dial 122)

## Overview

This repository presents a **voice-first, agentic AI backend** designed for real-time emergency call handling and post-call incident intelligence.

The system is inspired by real-world emergency response workflows, where calls are **short, high-stress, and time-critical**, and where **post-call analytics** play a crucial role in incident review, response optimization, and pattern analysis.

The agent operates as the **first point of contact** during an emergency call, gathers minimal critical information, and produces a **structured post-call summary** only after the call concludes.

> ⚠️ **Important**
> This is a **fictionalized, demo-safe system** created for engineering demonstration purposes.
> All identifiers (e.g., Dial 122) are non-operational and used only to showcase system design.

---

## Key Characteristics

* **Voice-first agent design** (ASR → Agent → TTS compatible)
* **Agentic workflow orchestration** using LangGraph
* **Strict low-latency constraints** for live calls
* **No looping or prolonged conversations**
* **Post-call analytics only after call termination**
* **Structured, auditable JSON outputs**
* **Production-style backend architecture**

This is **not a chatbot** and **not a toy demo** — it models real operational constraints.

---

## High-Level Architecture

```
Caller (Voice)
   ↓
ASR (Speech-to-Text)
   ↓
LLM Call Agent (FastAPI + LangGraph)
   ↓
[ Call Ongoing? ]
   ├── YES → End graph execution (return response)
   └── NO  → Post-call Summarization Node
                ↓
              Structured Incident Summary (JSON)
```

### Design Rationale

* Emergency calls must remain **short and focused**
* Any heavy analytics must be **decoupled from live interaction**
* The system explicitly avoids:

  * Long back-and-forth conversations
  * Speculative reasoning
  * On-call report generation

---

## Agent Workflow Logic

The LangGraph workflow follows a **simple and intentional control flow**:

1. **LLM Call Node**

   * Handles live emergency interaction
   * Collects minimal critical information
   * Determines call termination via structured output

2. **Conditional Branch**

   * If `call_status == "ONGOING"` → graph ends immediately
   * If `call_status == "END"` → post-call summarization is triggered

3. **Post-Call Summarization Node**

   * Runs only after call completion
   * Generates structured operational intelligence
   * Outputs clean, machine-readable JSON

This design ensures **low latency**, **predictable behavior**, and **clear auditability**.

---

## Post-Call Intelligence

After call termination, the system generates a structured summary including (when available):

* Call disposition
* Emergency type
* Risk / severity level
* Location and landmarks
* Injuries or threats mentioned
* Language used
* Agent actions taken
* Neutral factual summary of the incident

All summaries follow a **strict JSON contract**:

* No markdown
* No free-form explanations
* No hallucinated data
* Missing fields are set to `null`

This makes the output suitable for:

* Dashboards
* Incident review
* Analytics pipelines
* Downstream decision systems

---

## Technology Stack

* **Backend Framework:** FastAPI
* **Agent Orchestration:** LangGraph
* **LLMs:** GPT-4o-mini (configurable / swappable)
* **Prompting:** Strict system-level behavioral prompts
* **State Management:** Explicit conversation state
* **Output Contracts:** JSON-only structured responses

> The system is **model-agnostic by design**.
> The live-call and summarization models can be replaced with:
>
> * Self-hosted LLMs
> * Regional / Indic language models
> * Enterprise LLM endpoints
>   without changing the workflow logic.

---

## Repository Structure

```
emergency-response-intelligence-agent/
│
├── app.py            # FastAPI entrypoint
├── agent.py          # LangGraph workflow & agent logic
├── prompt.py         # Live-call system prompt (sanitized)
├── analytics.py      # Post-call summarization logic
├── state.py          # Conversation state definition
├── config.py         # Environment-based configuration
│
├── README.md
├── requirements.txt
└── LICENSE
```

---

## Scope & Limitations

### Included

* Live emergency call handling
* Agentic decision flow
* Post-call summarization
* Structured incident intelligence
* Low-latency design

### Intentionally Excluded

* Authentication / authorization
* UI or frontend components
* Automatic dispatch systems
* Legal or medical advice
* Real government integrations

These exclusions are **intentional** to keep the repository focused on **agentic AI backend design**.

---

## Intended Audience

This repository is intended for:

* AI / ML Engineers
* Backend Engineers
* System Designers
* Product teams exploring agentic AI
* Recruiters evaluating real-world AI systems

It demonstrates **engineering judgment**, **tradeoff awareness**, and **production-style thinking**, rather than model experimentation.

---

## Disclaimer

This project is a **technical demonstration**.

It does **not** represent a deployed emergency system and should **not** be used in real emergency scenarios.

---

## Author

**Utkarsh Dwivedi**
AI/ML Engineer | Agentic AI & LLM Systems
🔗 GitHub: [https://github.com/ut2903](https://github.com/ut2903)

---

