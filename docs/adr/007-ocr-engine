# ADR-007: OCR Engine Selection

## Context

The document ingestion pipeline extracts text from PDF files using PyMuPDF. However, scanned PDFs and image-based documents may contain no extractable text because their content is stored as images rather than text.

To support these documents, the ingestion pipeline requires an Optical Character Recognition (OCR) engine that can extract text from page images.

## Alternatives Considered

### 1. Tesseract OCR

Tesseract is an open-source OCR engine that can be integrated into Python using `pytesseract`. PDF pages can be rendered as images using PyMuPDF and passed to Tesseract for text extraction.

**Advantages**
- Free and open source.
- Runs locally without an external service.
- Supports multiple languages through language-specific trained data.
- Integrates with Python and PyMuPDF.
- Offers a lightweight solution for a local document ingestion pipeline.

**Disadvantages**
- Requires installing the Tesseract executable separately from the Python wrapper.
- OCR accuracy depends on image quality, resolution, layout, and language configuration.
- Complex layouts, tables, handwriting, and low-quality scans may produce inaccurate results.
- PDF pages must be rendered as images before OCR processing.

### 2. EasyOCR

EasyOCR is a Python-oriented OCR library based on deep learning.

**Advantages**
- Provides a Python API.
- Supports multiple languages.
- Can handle some challenging image-based text recognition tasks.

**Disadvantages**
- Introduces additional machine-learning dependencies.
- May require more memory and computational resources than Tesseract.
- Model initialization and inference can increase ingestion latency.

### 3. PaddleOCR

PaddleOCR is an OCR framework that provides text detection and recognition capabilities.

**Advantages**
- Supports complex document layouts and multiple languages.
- Offers text detection and recognition models.
- Can perform well on challenging document images.

**Disadvantages**
- Introduces a more substantial dependency and configuration footprint.
- Requires additional consideration of model management and computational resources.
- May be unnecessarily complex for the initial requirements of the project.

### 4. Cloud OCR Services

Cloud services such as Google Cloud Vision, Azure AI Document Intelligence, and Amazon Textract provide managed OCR capabilities.

**Advantages**
- Reduce the need to manage OCR models locally.
- Can provide advanced document processing features, including layout and table extraction.
- Offer scalable processing infrastructure.

**Disadvantages**
- Require network access and external service credentials.
- May introduce usage-based costs.
- Send document content to an external provider, subject to the service's data handling and retention policies.
- Introduce an external service dependency into the ingestion pipeline.

## Decision

Tesseract OCR was selected for the initial implementation.

The project prioritizes local execution, low operational cost, and straightforward integration with the existing Python-based PDF ingestion pipeline. Tesseract satisfies these requirements without introducing a dependency on cloud services or requiring a dedicated deep-learning inference stack.

The implementation will use PyMuPDF to detect whether a PDF contains extractable text and render pages when OCR is required. Tesseract will then process those page images using the appropriate language models.

## References

- Tesseract OCR: https://github.com/tesseract-ocr/tesseract
- PyTesseract: https://github.com/madmaze/pytesseract
- EasyOCR: https://github.com/JaidedAI/EasyOCR
- PaddleOCR: https://github.com/PaddlePaddle/PaddleOCR
- Google Cloud Vision: https://cloud.google.com/vision
- Azure AI Document Intelligence: https://azure.microsoft.com/products/ai-services/ai-document-intelligence
- Amazon Textract: https://aws.amazon.com/textract/