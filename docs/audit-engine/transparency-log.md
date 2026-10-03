# Certification Transparency Log & Cryptographic Ledger

## Design
Inspired by **Certificate Transparency (RFC 6962)** and **Sigstore Rekor**, the Certification Authority maintains an append-only cryptographic ledger (`transparency_log.jsonl`) recording every certificate issued.

## Hash Chaining Scheme

Each entry calculates:
$$\text{Entry Hash}_i = \text{SHA256}(\text{Entry ID}_i \,\|\, \text{Cert ID}_i \,\|\, \text{Merkle Root}_i \,\|\, \text{Prev Hash}_{i-1} \,\|\, \dots)$$

Where $\text{Prev Hash}_0 = \text{SHA256}(\text{"GENESIS\_BLOCK"})$.

```mermaid
flowchart LR
    Genesis["Genesis Block"] --> Entry1["Entry #1: v1.0.0"]
    Entry1 --> Entry2["Entry #2: v1.1.0"]
    Entry2 --> Entry3["Entry #3: v1.2.0"]
```

## Tamper Evidence
Any retroactive modification, deletion, or reordering of historical records breaks the cryptographic hash chain downstream, causing `verify_log_integrity()` to immediately detect the tampering.

## Verification
```bash
python -m enterprise_audit_engine.cli.main verify-transparency-log --repo-root .
```
