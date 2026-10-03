"""
Synthetic Benchmark Dataset Generator for AI & OCR Verification.
"""
import random
import string
import hashlib
from typing import List, Dict, Any

def generate_synthetic_documents(count: int = 100) -> List[Dict[str, Any]]:
    docs = []
    for i in range(count):
        doc_id = f"syn_doc_{i:04d}"
        text = " ".join(
            "".join(random.choices(string.ascii_letters, k=random.randint(3, 10)))
            for _ in range(50)
        )
        checksum = hashlib.sha256(text.encode("utf-8")).hexdigest()
        docs.append({
            "doc_id": doc_id,
            "text": text,
            "char_count": len(text),
            "sha256": checksum,
            "category": random.choice(["INVOICE", "PASSPORT", "CONTRACT", "RECEIPT"])
        })
    return docs

if __name__ == "__main__":
    res = generate_synthetic_documents(5)
    print(f"Generated {len(res)} synthetic benchmark records.")
