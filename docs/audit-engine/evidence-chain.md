# Cryptographic Evidence Chain & Merkle Tree Verification

## 1. Merkle Tree Architecture

```
                    [ Merkle Root Hash ]
                           /     \
                [ Node H12 ]     [ Node H34 ]
                  /     \           /     \
             [ Leaf H1 ] [ Leaf H2 ] [ Leaf H3 ] [ Leaf H4 ]
                 |           |           |           |
              [EV-001]    [EV-002]    [EV-003]    [EV-004]
```

## 2. Leaf Hashing Strategy
Every `EvidenceRecord` contains:
- Unique canonical ID (`EV-XXXXX`)
- Normalized JSON payload
- Collector metadata
- Category & timestamp

Leaf hash calculation:
```python
SHA256(canonical_json_string(evidence_record))
```

## 3. Audit Proof Generation & Verification
Auditors can verify an individual evidence record without having the entire database:
```python
is_valid = MerkleEvidenceTree.verify_proof(leaf_hash, proof_path, merkle_root)
```

## 4. `audit_merkle_root.json` Schema
```json
{
  "merkle_root": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
  "total_leaves": 10,
  "tree_depth": 5,
  "timestamp": "2026-09-20T18:30:00Z",
  "leaf_evidence_map": {
    "EV-00001": "hash_1...",
    "EV-00002": "hash_2..."
  }
}
```
