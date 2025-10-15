# Architecture Notes

- MCPCoordinator orchestrates the review flow.
- Replace `call_llm` with your provider (OpenAI/Anthropic/Local model).
- Add embedding + vector store (FAISS/Chroma) for RAG retrieval.
- Use language-specific linters and static analyzers for higher fidelity.
