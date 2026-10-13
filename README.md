# Ingestion Pipeline


```text
[ Raw PDF File ] 
       │
       ▼
 1. Validation ──(Invalid)──> [ Raise Error / Reject ]
       │ (Valid)
       ▼
 2. PDF Text Extraction (PyMuPDF)
       │
       ▼
 3. Cryptographic Hashing (SHA-256 in Chunks)
       │
       ▼
 4. Document Assembly ──> [ Structured Document Object ]
```