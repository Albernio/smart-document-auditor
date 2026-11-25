# Cómo funciona Smart Document Auditor

La aplicación permite cargar un PDF, indexar su contenido y hacer preguntas
utilizando los fragmentos más relevantes como contexto para un modelo local.
La interfaz está implementada con Streamlit; PostgreSQL y `pgvector` almacenan
los fragmentos y sus vectores.

## Flujo general

```mermaid
flowchart TD
    U[Usuario] --> UI[Interfaz Streamlit]

    subgraph INGESTA["Carga e indexación del PDF"]
        PDF[PDF cargado] --> VALIDAR[Validar archivo PDF]
        VALIDAR --> HASH[Calcular hash SHA-256]
        HASH --> EXTRAER[Extraer texto por página]
        EXTRAER --> TIPO{Tipo de contenido}
        TIPO -->|Texto| TEXTO[Extraer con PyMuPDF]
        TIPO -->|Escaneado| OCR[OCR con Tesseract]
        TIPO -->|Mixto| MIXTO[PyMuPDF y OCR de imágenes]
        TEXTO --> PAGINAS[Texto asociado a páginas]
        OCR --> PAGINAS
        MIXTO --> PAGINAS
        PAGINAS --> CHUNK[Dividir en fragmentos<br/>1000 caracteres, 200 de solapamiento]
        CHUNK --> EMB[Crear embeddings multilingües]
        EMB --> GUARDAR[Guardar documento, fragmentos y vectores]
    end

    UI -->|Subir y pulsar Ingest document| PDF
    GUARDAR --> DB[(PostgreSQL + pgvector)]

    subgraph PREGUNTAS["Búsqueda y generación de respuesta"]
        P[Pregunta del usuario] --> QEMB[Crear embedding de la pregunta]
        QEMB --> BUSCAR[Buscar los 5 fragmentos más similares]
        BUSCAR --> CONTEXTO[Construir contexto]
        CONTEXTO --> PROMPT[Preparar prompt con pregunta y contexto]
        P --> PROMPT
        PROMPT --> LLM[Ollama: qwen3:8b]
        LLM --> RESP[Respuesta y referencias]
    end

    UI -->|Escribir pregunta y pulsar Ask| P
    DB -->|Fragmentos ordenados por distancia vectorial| BUSCAR
    RESP --> UI
```

## Qué ocurre en cada etapa

1. **Carga:** Streamlit recibe el PDF y, al iniciar la ingesta, valida el
   archivo y calcula su hash SHA-256.
2. **Extracción:** PyMuPDF lee el texto nativo. Para páginas escaneadas o
   imágenes, Tesseract realiza OCR en inglés y español; los PDF mixtos
   combinan ambos métodos.
3. **Indexación:** el texto conserva el número de página, se divide en
   fragmentos solapados y el modelo
   `paraphrase-multilingual-MiniLM-L12-v2` genera sus embeddings.
4. **Persistencia:** se guardan los metadatos del documento y los fragmentos
   con sus vectores en PostgreSQL. `pgvector` permite compararlos con una
   pregunta.
5. **Búsqueda:** la pregunta se convierte en un embedding y se consultan los
   cinco fragmentos más similares.
6. **Respuesta:** el sistema reúne los fragmentos en el contexto del prompt y
   Ollama genera la respuesta. La interfaz muestra el texto y las referencias
   recuperadas, incluidos documento, página y distancia.

## Componentes principales

| Componente | Función |
| --- | --- |
| Streamlit (`app.py`) | Interfaz para cargar documentos y preguntar |
| PyMuPDF | Extraer texto y procesar páginas PDF |
| Tesseract | Reconocer texto en páginas escaneadas e imágenes |
| Sentence Transformers | Generar embeddings multilingües |
| PostgreSQL + `pgvector` | Guardar documentos, fragmentos y vectores; buscar similitud |
| Ollama | Ejecutar localmente el modelo de generación de respuestas |
