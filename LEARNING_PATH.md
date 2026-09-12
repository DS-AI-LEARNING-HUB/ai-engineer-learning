# GenAI / AI Engineer Learning Path

**Profile:** Advanced Python/ML background · 6-10 hrs/week · Full-time employee
**Tools:** VS Code (local) + Databricks (no other cloud platform)
**Pace:** ~20 weeks (~5 months), skips ML/Python fundamentals, goes straight into GenAI-specific skills

Check items off as you go (`[x]`). Revisit this file weekly — reorder or skip anything that's redundant given what you already know.

---

## Phase 0 — Environment Setup (Week 0, ~5-6 hrs)

- [ ] Install/verify Python 3.11+, `uv` or `venv` for environment management
- [ ] VS Code extensions: Python, Pylance, Jupyter, **Databricks** (official extension — enables Databricks Connect, notebook sync, job run from VS Code)
- [ ] Create a [Databricks Free Edition](https://www.databricks.com/product/faq/community-edition) account if you don't already have workspace access, or confirm access to your org's workspace
- [ ] Set up Databricks Connect from VS Code (run a cluster command from local VS Code against a Databricks cluster)
- [ ] Get API access to at least one hosted LLM: Anthropic Claude API or Databricks Foundation Model APIs (pay-per-token, no separate cloud infra needed)
- [ ] Install [Ollama](https://ollama.com) locally — run small open models (Llama 3.2, Qwen2.5, Phi-4) with zero cloud dependency
- [ ] Create a GitHub repo (e.g. `genai-learning`) to commit every project below — this becomes your portfolio
- [ ] Skim: Anthropic's [Claude docs](https://docs.claude.com) and Databricks' [Generative AI docs](https://docs.databricks.com/en/generative-ai/index.html) — bookmark, don't deep-read yet

---

## Phase 1 — LLM Foundations & Prompt Engineering (Weeks 1-3, ~18-24 hrs)

**Topics**
- [ ] Transformer architecture refresher (attention, context window, tokenization) — you know ML, so 1-2 hrs is enough
- [ ] Embeddings: what they are, cosine similarity, when text is "close" in vector space
- [ ] Prompt engineering: zero/few-shot, chain-of-thought, structured/JSON output, system prompts
- [ ] LLM API mechanics: streaming, tool/function calling, token limits, cost/latency tradeoffs
- [ ] Anthropic's [prompt engineering guide](https://docs.claude.com/en/docs/build-with-claude/prompt-engineering/overview) — read fully, it's the best free resource for this

**Hands-on (in VS Code)**
- [ ] Build a small Python CLI that calls Claude API + a local Ollama model side by side, compare outputs
- [ ] Implement structured output extraction (e.g., parse messy text into JSON using tool-use/function-calling)
- [ ] **Project 1:** A command-line "prompt playground" script — swap models/prompts via config, log results to a file

---

## Phase 2 — Retrieval-Augmented Generation (RAG) (Weeks 4-6, ~18-24 hrs)

**Topics**
- [ ] Chunking strategies (fixed-size, semantic, recursive) and why chunk size matters
- [ ] Vector stores: FAISS/Chroma (local, no cloud) vs Databricks Vector Search (managed)
- [ ] Retrieval pipeline: embed → store → retrieve → rerank → generate
- [ ] Framework: pick **one** of LangChain or LlamaIndex (don't learn both) — LlamaIndex is more RAG-focused and lighter-weight
- [ ] Databricks-specific: Unity Catalog Volumes for document storage, Databricks Vector Search index creation

**Hands-on**
- [ ] Build a RAG pipeline locally first (Chroma + Ollama or Claude) over a small personal doc set (PDFs, notes)
- [ ] Rebuild the same pipeline on Databricks: load docs into a Volume, create a Vector Search index, query it from a notebook
- [ ] **Project 2:** A RAG chatbot over a real corpus you care about (e.g., internal docs, a subject you're studying) — one version running locally, one running on Databricks

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
