# ADR-007: Selección del motor OCR

## Contexto

La canalización de ingesta de documentos extrae texto de archivos PDF mediante PyMuPDF. Sin embargo, los PDF escaneados y los documentos basados en imágenes pueden no contener texto extraíble, ya que su contenido está almacenado como imágenes y no como texto.

Para admitir estos documentos, la canalización de ingesta necesita un motor de reconocimiento óptico de caracteres (OCR) que pueda extraer texto de imágenes de páginas.

## Alternativas consideradas

### 1. Tesseract OCR

Tesseract es un motor OCR de código abierto que puede integrarse con Python mediante `pytesseract`. Las páginas PDF se pueden convertir en imágenes con PyMuPDF y procesarse con Tesseract para extraer el texto.

**Ventajas**
- Gratuito y de código abierto.
- Se ejecuta localmente, sin un servicio externo.
- Admite varios idiomas mediante datos de entrenamiento específicos para cada idioma.
- Se integra con Python y PyMuPDF.
- Ofrece una solución ligera para una canalización local de ingesta de documentos.

**Desventajas**
- Es necesario instalar el ejecutable de Tesseract por separado del envoltorio de Python.
- La precisión del OCR depende de la calidad y resolución de la imagen, del diseño y de la configuración del idioma.
- Los diseños complejos, las tablas, la escritura manuscrita y los escaneos de baja calidad pueden producir resultados imprecisos.
- Las páginas PDF deben convertirse en imágenes antes del procesamiento OCR.

### 2. EasyOCR

EasyOCR es una biblioteca OCR orientada a Python y basada en aprendizaje profundo.

**Ventajas**
- Proporciona una API para Python.
- Admite varios idiomas.
- Puede gestionar algunas tareas complejas de reconocimiento de texto en imágenes.

**Desventajas**
- Añade dependencias de aprendizaje automático.
- Puede requerir más memoria y recursos de computación que Tesseract.
- La inicialización de los modelos y la inferencia pueden aumentar la latencia de ingesta.

### 3. PaddleOCR

PaddleOCR es un marco de OCR que ofrece capacidades de detección y reconocimiento de texto.

**Ventajas**
- Admite diseños de documentos complejos y varios idiomas.
- Ofrece modelos de detección y reconocimiento de texto.
- Puede funcionar bien con imágenes de documentos difíciles.

**Desventajas**
- Añade más dependencias y configuración.
- Requiere tener en cuenta la gestión de modelos y los recursos de computación.
- Puede ser innecesariamente complejo para los requisitos iniciales del proyecto.

### 4. Servicios OCR en la nube

Servicios en la nube como Google Cloud Vision, Azure AI Document Intelligence y Amazon Textract ofrecen capacidades OCR gestionadas.

**Ventajas**
- Reducen la necesidad de gestionar modelos OCR localmente.
- Pueden ofrecer funciones avanzadas de procesamiento de documentos, incluida la extracción de diseños y tablas.
- Proporcionan una infraestructura de procesamiento escalable.

**Desventajas**
- Requieren acceso a la red y credenciales de servicios externos.
- Pueden generar costes según el uso.
- Envían el contenido de los documentos a un proveedor externo, sujeto a sus políticas de tratamiento y conservación de datos.
- Añaden una dependencia de un servicio externo a la canalización de ingesta.

## Decisión

Se seleccionó Tesseract OCR para la implementación inicial.

El proyecto prioriza la ejecución local, un coste operativo bajo y una integración sencilla con la canalización de ingesta de PDF existente, basada en Python. Tesseract satisface estos requisitos sin depender de servicios en la nube ni requerir una pila dedicada de inferencia de aprendizaje profundo.

La implementación usará PyMuPDF para detectar si un PDF contiene texto extraíble y para renderizar las páginas cuando se necesite OCR. A continuación, Tesseract procesará las imágenes de esas páginas con los modelos de idioma correspondientes.

## Referencias

- Tesseract OCR: https://github.com/tesseract-ocr/tesseract
- PyTesseract: https://github.com/madmaze/pytesseract
- EasyOCR: https://github.com/JaidedAI/EasyOCR
- PaddleOCR: https://github.com/PaddlePaddle/PaddleOCR
- Google Cloud Vision: https://cloud.google.com/vision
- Azure AI Document Intelligence: https://azure.microsoft.com/products/ai-services/ai-document-intelligence
- Amazon Textract: https://aws.amazon.com/textract/
