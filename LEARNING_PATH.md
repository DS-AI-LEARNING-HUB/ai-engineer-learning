# GenAI / AI Engineer Learning Path

**Profile:** Advanced Python/ML background · 6-10 hrs/week · Full-time employee
**Tools:** VS Code (local) + Databricks (no other cloud platform)
**Pace:** ~20 weeks (~5 months), skips ML/Python fundamentals, goes straight into GenAI-specific skills

Check items off as you go (`[x]`). Revisit this file weekly — reorder or skip anything that's redundant given what you already know.

---

## Phase 0 — Environment Setup (Week 0, ~5-6 hrs)

- [x] Install/verify Python 3.11+, `uv` or `venv` for environment management — Python 3.12.10 + `uv` confirmed
- [x] VS Code extensions: Python, Pylance, Jupyter, **Databricks** (official extension — enables Databricks Connect, notebook sync, job run from VS Code)
- [x] Confirm access to your org's Databricks workspace — connected via VS Code Databricks extension, catalogs visible
- [x] Set up Git + GitHub (bonus, not originally listed): repo created at `DS-AI-LEARNING-HUB/ai-engineer-learning`, local `master` tracks `origin/dev-branch` — see [GIT_LEARNING.md](GIT_LEARNING.md)
- [x] Get API access to a hosted LLM: using **Databricks Foundation Model APIs** — `databricks-claude-opus-5` endpoint, tested end-to-end from VS Code via `src/test_databricks_llm.py`
- [ ] ~~Install [Ollama](https://ollama.com) locally~~ — skipped for now, already have a working hosted model via Databricks Foundation Model APIs; revisit later if local/offline model experimentation becomes useful
- [ ] Skim: Anthropic's [Claude docs](https://docs.claude.com) and Databricks' [Generative AI docs](https://docs.databricks.com/en/generative-ai/index.html) — bookmark, don't deep-read yet

---

## Phase 1 — LLM Foundations & Prompt Engineering (Weeks 1-3, ~18-24 hrs)

**Topics**
- [x] Transformer/LLM mental model: next-token prediction, tokens vs. words (`tiktoken` hands-on), context window, "lost in the middle"
- [x] Embeddings: what they are, cosine similarity, hands-on with `system.ai.gte-large-en` comparing sentence similarity
- [x] Prompt engineering: zero/few-shot, chain-of-thought, structured/JSON output, system prompts — `prompt_playground.py`
- [x] LLM API mechanics: streaming (`streaming_playground.py`), tool/function calling (`tool_calling_playground.py`), token limits/cost/latency (`token_limit_playground.py`, incl. reasoning-model thinking budgets), response object anatomy (`inspect_response.py`)
- [ ] ~~Anthropic's prompt engineering guide~~ — optional background reading, not required to proceed

**Hands-on (in VS Code)**
- [x] Structured output extraction via tool/function calling
- [x] **Project 1:** prompt/tool/streaming/embedding playground scripts in `src/`, all calling Databricks Foundation Model APIs (`databricks-claude-opus-5`, `system.ai.gte-large-en`)
- [ ] ~~CLI comparing Claude API + local Ollama~~ — skipped, no local Ollama; used Databricks-hosted models throughout instead

---

## Phase 2 — Retrieval-Augmented Generation (RAG) (Weeks 4-6, ~18-24 hrs)

**Topics**
- [x] Chunking strategies: naive fixed-size (and its failure modes) → header/structure-aware → recursive paragraph fallback with atomic-unit protection (never split an image link) — `src/RAG/chunking.py`
- [x] Multimodal document parsing: extracting text + embedded images from a real PDF in reading order (`pdf_extract_ordered` logic), captioning images via Claude's vision input, merging captions back into the text flow — `src/RAG/pdf_to_text.py`
- [x] Vector stores: built locally with **Chroma** (open-source, no cloud/account needed) — `src/RAG/build_index.py`. Databricks Vector Search version still to do.
- [x] Retrieval pipeline: embed → store → retrieve → generate, fully working end-to-end — `src/RAG/query.py`
- [ ] ~~Framework: LangChain/LlamaIndex~~ — deliberately built the pipeline from scratch first for understanding; may revisit a framework later
- [ ] Databricks-specific: Unity Catalog Volumes for document storage, Databricks Vector Search index creation

**Hands-on**
- [x] Built a RAG pipeline locally: Chroma + `databricks-claude-opus-5` + `system.ai.gte-large-en`, over a synthetic doc set (3 markdown docs + 1 PDF with a real embedded chart)
- [x] **Project 2 (local version):** a working RAG system that correctly answers questions using data that only existed inside a chart image (proving the multimodal captioning step actually works) — `src/RAG/query.py`
- [ ] Rebuild the same pipeline on Databricks: load docs into a Volume, create a Vector Search index, query it from a notebook

---

## Phase 3 — Agents & Tool Use (Weeks 7-9, ~18-24 hrs)

**Topics**
- [ ] Tool/function calling in depth — designing tool schemas an LLM can reliably use
- [ ] ReAct pattern (reason → act → observe loop)
- [ ] Agent orchestration framework: **LangGraph** (most transferable, works with any model provider)
- [ ] Model Context Protocol (MCP) basics — how Claude Code itself uses it; build a toy MCP server
- [ ] Multi-agent patterns: when to split into sub-agents vs one agent with more tools (keep it simple — most production agents don't need multi-agent complexity)

**Hands-on**
- [ ] Build a single-agent tool-using assistant (e.g., calculator + web search + file read tools)
- [ ] Build a minimal MCP server exposing one custom tool, connect it to Claude Code or another MCP client
- [ ] **Project 3:** A data-analysis agent that answers natural-language questions by querying a Databricks SQL warehouse (agent writes SQL, executes via a tool, summarizes results)

---

## Phase 4 — Fine-Tuning & Model Customization (Weeks 10-12, ~18-24 hrs)

**Topics**
- [ ] Decision framework: prompt engineering vs RAG vs fine-tuning (fine-tune last, and rarely)
- [ ] PEFT concepts: LoRA / QLoRA — why full fine-tuning is usually unnecessary
- [ ] Hugging Face `transformers` + `peft` libraries
- [ ] Databricks: Mosaic AI Fine-Tuning API (fine-tune foundation models using Databricks compute — no external cloud needed since it runs inside your workspace)
- [ ] MLflow experiment tracking basics (runs, params, metrics, model registry)

**Hands-on**
- [ ] Fine-tune a small open model (Llama 3.2 1B/3B or Qwen 2.5 0.5B) locally with LoRA on a narrow task (e.g., a classification or style-transfer task) — CPU/small-GPU friendly
- [ ] Repeat using Databricks compute + Mosaic AI Fine-Tuning API, track the run in MLflow
- [ ] **Project 4:** A fine-tuned small model for one specific task relevant to your job, with an MLflow-tracked before/after comparison against the base model

---

## Phase 5 — Evaluation & LLMOps (Weeks 13-16, ~18-24 hrs)

**Topics**
- [ ] GenAI evaluation: LLM-as-judge, RAGAS metrics (faithfulness, relevance, context precision/recall)
- [ ] Guardrails: input/output filtering, prompt-injection awareness, PII handling
- [ ] MLflow GenAI features: tracing, `mlflow.evaluate` for LLM apps, prompt versioning
- [ ] Databricks: Model Serving (deploy an endpoint for your RAG/agent app), Unity Catalog governance for AI assets, Lakehouse Monitoring for drift/quality
- [ ] Cost and latency monitoring for production LLM apps

**Hands-on**
- [ ] Add an evaluation harness (RAGAS or custom LLM-judge) to your Project 2 RAG chatbot — quantify answer quality
- [ ] Deploy your RAG or agent app behind a Databricks Model Serving endpoint
- [ ] **Project 5:** Turn Project 2 or 3 into a governed, monitored, deployed service: MLflow tracing + eval scores + Model Serving endpoint + basic dashboard of quality/cost over time

---

## Phase 6 — Capstone & Portfolio (Weeks 17-20, ~18-24 hrs)

- [ ] Combine RAG + agent tool-use + (optionally) your fine-tuned model + evaluation + Databricks deployment into **one coherent capstone application** solving a real problem (ideally something useful at work)
- [ ] Write a README/case-study for the capstone: problem, architecture diagram, tradeoffs, what you'd do differently
- [ ] Clean up and document all 5 prior projects in the GitHub repo
- [ ] Optional: write 1-2 short blog posts or internal share-outs on what you learned (great for visibility as a full-time employee)

---

## Weekly Rhythm (suggested, ~7 hrs/week)

- 2 weekday evenings × 1.5 hrs → new concept + small hands-on exercise
- 1 weekend block × 4 hrs → project work
- Adjust freely — consistency matters more than the exact split

## Staying Current (ongoing, low time cost)

- [ ] Subscribe to Anthropic's [blog](https://www.anthropic.com/news) and Databricks' [GenAI blog](https://www.databricks.com/blog/category/generative-ai)
- [ ] Skim one GenAI-related paper or blog post a week (don't chase every model release)

## Notes / Deviations

*(Use this space to jot down what you skip, reorder, or what turned out to be redundant given your existing background.)*
