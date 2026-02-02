You are an expert AI Engineer completing a project. Your task is to **design, implement, and document a complete system** that converts a long‑form PDF document into a **two‑host podcast script**, with a **verification layer** that checks factual accuracy and coverage.

This is not just a coding task. You are evaluated on **engineering judgment, architecture choices, tradeoffs, and clarity of explanation**. Prefer a simple, well‑justified system over a complex one.

Assume you are allowed to use modern AI tooling (LLMs, embeddings, agents, etc.). Preserve all prompts, iterations, and reasoning artifacts.

---

## 1. PROBLEM OVERVIEW

### Objective

Build a system that:

1. Takes a **long‑form PDF document** as input
2. Extracts **specific configurable sections**
3. Generates a **~2,000 word / ~10 minute two‑host podcast script**
4. Produces a **verification report** that checks:

   * Claim traceability
   * Hallucinations
   * Coverage of key information

The system will be tested on **unseen PDFs** with **different section configurations**, so your design must generalize.

---

## 2. INPUTS

### Required Inputs

* A **PDF document** (assume clean, digital text; not scanned)
* A **section configuration**, which may be defined using one of the following (choose and justify):

  * Page ranges
  * Headings / TOC‑based sections
  * Another reasonable approach

### Test Document (For Example Output)

* **Document**: Vestas Annual Report 2024 (221‑page PDF)
* **Sections to cover**:

  * Letter from the Chair & CEO (pages 3–4)
  * Market outlook (pages 17–18)
  * Corporate strategy (pages 19–21)
  * Service (page 31)

---

## 3. OUTPUTS

Your repository must include:

### 3.1 Podcast Script

A generated podcast script that:

* Is ~2,000 words (≈10 minutes spoken)
* Uses **two hosts** with natural conversational flow
* **Teaches the content** (substantive understanding, not vibes)
* Sounds like **real dialogue**, not alternating monologues
* Includes **friction** (at least one disagreement, challenge, or pushback)
* Lands a clear **"so what" takeaway** at the end
* Includes **lightweight, professional emotional cues** (e.g., curiosity, skepticism)

### 3.2 Verification Report

Produce a verification report (Markdown, JSON, or hybrid — justify your choice) containing:

1. **Claim Traceability**

   * Identify factual claims in the script
   * Map each claim to one or more **specific source passages**
   * Factual claims include assertions about:

     * Business facts
     * Market conditions
     * Strategy
     * Numbers
     * Stated intentions
   * Exclude opinions, framing, or host banter

2. **Hallucination Flags**

   * Explicitly flag claims that **cannot be traced** to the source document

3. **Coverage Analysis**

   * Measure how much key information from each specified section made it into the script
   * Categorize coverage as:

     * Full
     * Partial
     * Omitted
   * List what was omitted
   * Favor realism and "good enough" over perfect recall

---

## 4. TECHNICAL REQUIREMENTS

### Architecture

* Use an **agentic architecture** (or explicitly justify why you did not)
* Clearly define agent responsibilities (e.g., extraction, scripting, verification)
* Keep orchestration understandable and debuggable

### Configuration

* Section selection must be **configurable** and reusable
* Explain why your sectioning approach is robust for unseen documents

### Implementation

* Language: **Python or TypeScript** (choose one and justify)
* Must be **runnable locally** with clear setup instructions
* Minimal but functional dependency stack

---

## 5. REPOSITORY REQUIREMENTS

Generate a GitHub‑ready repository structure containing:

### Required Files

* `README.md`

  * Setup instructions
  * How to run the system
  * High‑level overview

* `process.md`

  * System overview and architecture diagram (textual is fine)
  * Why you structured it this way
  * All prompts used (including iterations and dead ends)
  * Examples where you **rejected or modified AI‑generated suggestions**, and why
  * Answers to reflection questions (see below)

* `example_output/`

  * Generated podcast script for the Vestas test document
  * Corresponding verification report

* `src/` (or equivalent)

  * Core implementation
  * Clear separation of concerns

---

## 6. CONSTRAINTS & GUIDANCE

* Do **not** over‑engineer UI or frontend
* Keep testing minimal (MVP‑level is sufficient)
* Assume documents similar to the provided PDF
* Preserve messy prompt history — do not sanitize it
* Favor clarity of reasoning over clever tricks

---

## 7. EXPECTATIONS FOR YOU (THE AGENT)

* Make and explain tradeoffs explicitly
* Prefer simple, robust solutions
* Annotate code where decisions matter
* Think like a production‑minded AI engineer, not a demo hacker

Your final output should be a **complete, runnable project** that could realistically be reviewed by a hiring team.

Begin by proposing the architecture, then implement the system, then generate example outputs, and finally produce documentation.

Do not ask follow‑up questions unless something is ambiguous — make reasonable assumptions and document them.
