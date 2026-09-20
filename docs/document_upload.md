# Document Upload & Storage Foundation Architecture

**Platform**: AI Document Processing Platform  
**Target Directory**: `C:\Users\User\Desktop\ai_document_processing_platform`  
**Module**: Document Ingestion Pipeline (Prompt 3 Baseline)  

---

## 1. Executive Summary

The Document Upload & Storage Subsystem provides a secure, transactional, and scalable document ingestion pipeline. It handles file validation (file size limits, path sanitization, extension whitelisting, double-extension blocking, and byte-level magic signature verification), SHA-256 content deduplication, date-partitioned storage abstraction (`LocalStorageProvider`), and database metadata persistence.

---

## 2. Document Upload Lifecycle

```
 Client (POST /documents/upload)
              │
              ▼
   [1] Security & Magic Bytes Validation
              │
              ▼
   [2] Compute SHA-256 Hash
              │
              ▼
   [3] SHA-256 Duplicate Check ──► (If exists: Return 409 / Existing Metadata)
              │
              ▼
   [4] Save File to Storage Provider (Date-Partitioned YYYY/MM/DD)
              │
              ▼
   [5] Persist Metadata in Database (Transaction context)
              │
         ┌────┴────┐
         ▼         ▼
      Success   DB Exception
         │         │
         │         └──► Rollback: Delete stored file from disk immediately!
         ▼
  Return 201 Created (UploadResponse)
```

---

## 3. Storage Abstraction Architecture

The storage subsystem strictly decouples business logic from disk interactions via the abstract class `StorageProvider`:

- **`StorageProvider` (Abstract Interface)**:
  - `save(content: bytes, original_filename: str) -> Tuple[stored_filename, rel_path, abs_path]`
  - `get(relative_path: str) -> bytes`
  - `delete(relative_path: str) -> bool`
  - `exists(relative_path: str) -> bool`
  - `validate_path_safety(relative_path: str) -> Path`

- **`LocalStorageProvider` Implementation**:
  - Partitioning Scheme: `storage/uploads/YYYY/MM/DD/`
  - Path Traversal Defense: Verifies canonical paths remain inside base storage root using `os.path.commonpath`.
  - Future Cloud Compatibility: Pluggable interface for AWS S3, Google Cloud Storage, or Azure Blob without changing business logic.

---

## 4. File Validation Pipeline & Magic Bytes Verification

The validation pipeline (`DocumentService.validate_file`) rejects malicious, malformed, or fake files BEFORE saving:

1. **Empty File Check**: Rejects 0-byte uploads.
2. **Size Limits**: Enforces `MAX_UPLOAD_SIZE_MB` (default 10 MB).
3. **Filename Length**: Limits original filename length to 255 characters.
4. **Path Traversal Defense**: Rejects filenames containing `..`, `/`, or `\`.
5. **Dangerous Extension Rejection**: Rejects executable extensions (`.exe`, `.bat`, `.sh`, `.php`, `.js`, `.py`).
6. **Double Extension Rejection**: Detects and rejects double extension attacks (e.g. `invoice.pdf.exe`).
7. **Magic Bytes Signature Inspection**:
   - `PDF`: Header starts with `%PDF-` (`0x25 0x50 0x44 0x46 0x2D`)
   - `PNG`: Header starts with `\x89PNG\r\n\x1a\n` (`0x89 0x50 0x4E 0x47`)
   - `JPEG`: Header starts with `\xff\xd8\xff` (`0xFF 0xD8 0xFF`)
   - `TIFF`: Header starts with `II*\x00` or `MM\x00*`
   - Rejects file if magic bytes fail to match declared extension.

---

## 5. Duplicate Detection Policy

- Every file's binary content is hashed with SHA-256 (`calculate_sha256`).
- Queries database via `doc_repo.get_by_hash(sha256_h, owner_id)`.
- If duplicate file exists for the same user, returns `is_duplicate=True` with existing document metadata, preventing storage inflation and redundant downstream processing.

---

## 6. Transactional Safety & Storage Rollback

To prevent orphaned files or database inconsistencies:
- File saving is executed first.
- Database entity creation occurs within an explicit `try-except` block.
- If database persistence fails, `storage_provider.delete(rel_path)` is called immediately to purge the saved file from disk.

---

## 7. API Endpoints Reference

| Method | Endpoint | Description | Status Code | Auth |
|--------|----------|-------------|-------------|------|
| `POST` | `/api/v1/documents/upload` | Ingest document file with magic byte validation & SHA256 check | 201 Created | Bearer JWT |
| `GET`  | `/api/v1/documents` | List user documents (paginated, with search parameter) | 200 OK | Bearer JWT |
| `GET`  | `/api/v1/documents/{id}` | Retrieve document metadata details | 200 OK | Bearer JWT |
| `DELETE`| `/api/v1/documents/{id}` | Safely delete DB metadata and physical file from disk | 200 OK | Bearer JWT |
