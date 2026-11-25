# ADR-001: PyMuPDF for extraction

## Context

The system needs a library to extract the data from the PDF documents.

## Decision

**PyMuPDF** will allow me to extract both text and images from PDF files, as well as the coordinates where these are located on each page, which will be useful to keep the chunks ordered.