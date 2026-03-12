"""
llm.py - LLM answer generation via the Mistral API.

Builds a retrieval-augmented prompt from the top-k passages returned by the
search engine and calls the Mistral chat completion endpoint to generate a
grounded, source-cited answer.

Requires:
    MISTRAL_API_KEY environment variable to be set.
"""

import os
from typing import List, Dict
from mistralai.client import Mistral


# ---------------------------------------------------------------------------
# Prompt construction
# ---------------------------------------------------------------------------

def build_prompt(query: str, passages: List[Dict]) -> str:
    """
    Build the RAG prompt by injecting retrieved context passages.

    Each passage is clearly labelled with its source document identifier so
    the model can cite it in the answer.

    Args:
        query:    The user's question.
        passages: List of chunk dicts (must contain 'source_id' and 'text').

    Returns:
        Formatted prompt string ready to send to the chat API.
    """
    context_parts = []
    for i, p in enumerate(passages, 1):
        context_parts.append(f"[Source {i}: {p['source_id']}]\n{p['text']}")
    context = "\n\n---\n\n".join(context_parts)

    prompt = f"""You are a precise document assistant specialised in legal and regulatory matters. \
Answer the question using ONLY the provided context passages.
If the answer is not found in the context, respond with: \
"I don't have enough information in the provided documents to answer this question."
Always cite your sources by referencing the source name in your answer \
(e.g., "According to [source_name], ...").
Be concise and factual. Do not speculate beyond what the documents state.

Context:
{context}

Question: {query}

Answer:"""
    return prompt


# ---------------------------------------------------------------------------
# Answer generation
# ---------------------------------------------------------------------------

def generate_answer(
    query: str,
    passages: List[Dict],
    model: str = "mistral-small-latest",
) -> str:
    """
    Generate a grounded answer using the Mistral chat completion API.

    Args:
        query:    The user's question.
        passages: Top-k retrieved passages from hybrid_search().
        model:    Mistral model identifier. Options:
                    - "mistral-small-latest"  (faster, cheaper)
                    - "mistral-large-latest"  (more capable)

    Returns:
        The assistant's answer as a plain string.

    Raises:
        ValueError: If MISTRAL_API_KEY is not set.
        Exception:  On API errors.
    """
    api_key = os.environ.get("MISTRAL_API_KEY")
    if not api_key:
        raise ValueError(
            "MISTRAL_API_KEY environment variable not set. "
            "Copy .env.example to .env and fill in your key."
        )

    client = Mistral(api_key=api_key)
    prompt = build_prompt(query, passages)

    response = client.chat.complete(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.1,   # Low temperature for factual, deterministic answers
        max_tokens=800,
    )

    return response.choices[0].message.content.strip()
