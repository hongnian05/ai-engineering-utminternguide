"""
UTM-InternGuide — Main Chatbot Orchestrator & Interactive CLI
Connects the persistent vector store, faculty-aware retriever, and grounded answer generator.
"""

from __future__ import annotations

import argparse
import sys
import time
from typing import Any

from src.config import DEFAULT_TOP_K, VECTOR_INDEX_PATH
from src.generator import generate_grounded_response
from src.retriever import FacultyAwareRetriever
from src.vector_store import LocalVectorStore


class UTMInternGuideChatbot:
    """Document-grounded RAG assistant for UTM Industrial Training."""

    def __init__(self, index_path=VECTOR_INDEX_PATH) -> None:
        self.store = LocalVectorStore.load(index_path)
        self.retriever = FacultyAwareRetriever(self.store)

    def ask(
        self,
        question: str,
        faculty: str | None = None,
        top_k: int = DEFAULT_TOP_K,
        exclude_historical: bool = False,
    ) -> dict[str, Any]:
        start = time.perf_counter()
        retrieval = self.retriever.retrieve(
            query=question,
            faculty=faculty,
            top_k=top_k,
            exclude_historical=exclude_historical,
        )
        result = generate_grounded_response(question, retrieval)
        latency_ms = round((time.perf_counter() - start) * 1000, 2)

        return {
            "question": question,
            "requested_faculty": faculty,
            "detected_faculty": retrieval.detected_faculty,
            "allowed_faculties": retrieval.allowed_faculties,
            "needs_faculty_clarification": result["needs_faculty_clarification"],
            "mode": result["mode"],
            "abstained": result["abstained"],
            "latency_ms": latency_ms,
            "answer": result["answer"],
            "citations": result["citations"],
            "retrieved_chunks": [
                {
                    "chunk_id": c["chunk_id"],
                    "source_id": c["source_id"],
                    "faculty": c["faculty"],
                    "section": c["section"],
                    "page_number": c.get("page_number"),
                    "similarity_score": c.get("similarity_score"),
                }
                for c in retrieval.chunks
            ],
        }


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description="UTM-InternGuide RAG Chatbot CLI")
    parser.add_argument("--question", "-q", type=str, help="Ask a single question and exit.")
    parser.add_argument("--faculty", "-f", type=str, default=None, help="Optional faculty filter (e.g., FC, FKT, FKE, Civil, MJIIT, FKM).")
    args = parser.parse_args()

    bot = UTMInternGuideChatbot()

    if args.question:
        res = bot.ask(args.question, faculty=args.faculty)
        print(res["answer"])
        print(f"\n[Latency: {res['latency_ms']} ms | Mode: {res['mode']}]")
        return

    print("=" * 72)
    print("  UTM-InternGuide — Interactive Document-Grounded Internship Assistant")
    print("  Type 'exit' or 'quit' to stop. Optional prefix: [FC], [FKT], [FKE], [Civil], [MJIIT], [FKM]")
    print("=" * 72)
    current_faculty = args.faculty

    while True:
        try:
            q = input("\nStudent Question > ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break
        if not q or q.lower() in ("exit", "quit"):
            print("Goodbye!")
            break
        res = bot.ask(q, faculty=current_faculty)
        print("\n" + res["answer"])
        print(f"\n[Latency: {res['latency_ms']} ms | Scope: {res['detected_faculty'] or 'University-Wide/Auto'}]")


if __name__ == "__main__":
    main()
