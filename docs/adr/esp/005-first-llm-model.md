# ADR-005: Primer modelo LLM para generar respuestas

## Contexto

El sistema RAG necesita un modelo de lenguaje generativo que produzca respuestas a partir de los fragmentos de documentos recuperados. El sistema está pensado para admitir documentos y consultas de usuarios en varios idiomas.

## Decisión

Usar qwen3:8b a través de Ollama como modelo local de generación.

## Justificación

- Ejecución local
- Capacidad multilingüe
- Tamaño del modelo: el modelo de 8B ofrece un equilibrio práctico entre la calidad de generación y los recursos locales necesarios.
- Sencillez operativa
