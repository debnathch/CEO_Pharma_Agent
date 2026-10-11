# ADR-007: Deferral of Semantic Memory and Vector Databases from Foundation Phase

## Status
Accepted

## Context
Multi-agent projects often prematurely introduce vector databases (Pinecone, Chroma, Qdrant), embeddings models, and complex semantic memory layers before basic workflow boundaries, deterministic accounting, and regression suites exist. Vector databases introduce embedding drift, index maintenance overhead, and latency without solving core structured business reporting needs.

## Decision
We explicitly **defer vector databases, semantic memory, and RAG embeddings** from the foundation phase.
We distinguish four explicit memory and state tiers:
1. **Workflow Execution State**: Ephemeral LangGraph state passed through the bounded graph.
2. **Current Conversation History**: Client-managed session context.
3. **Authoritative Business Records**: Structured transactional records owned by Marg ERP, Ordering Portal, and HR.
4. **Future Long-Term Semantic Memory**: Deferred to a subsequent phase when unstructured document search (medical literature, SOP PDFs) is implemented.

## Alternatives Considered
1. **Embedding all synthetic invoices into ChromaDB / pgvector**:
   - *Rejected*: Invoices and sales ledgers are structured relational data. Querying financial figures via cosine similarity is an architectural anti-pattern that leads to hallucinated accounting.

## Consequences & Trade-offs
- **Positive**:
  - Eliminates vector DB dependencies, embedding costs, and local GPU RAM overhead.
  - Keeps data retrieval 100% deterministic and auditable.
- **Negative / Trade-offs**:
  - Semantic similarity search across arbitrary text documents is deferred to later phases.
