# Smart-document-auditor

Aplicación local basada en **Retrieval-Augmented Generation (RAG)** para analizar documentos PDF y responder preguntas utilizando su contenido.

El sistema extrae el texto de documentos PDF, lo divide en fragmentos (*chunks*), genera embeddings vectoriales, los almacena en PostgreSQL con `pgvector`, recupera los fragmentos semánticamente relevantes y utiliza un LLM local mediante Ollama para generar respuestas fundamentadas con referencias al documento y a la página.

## Quick Start

Sigue estos pasos para ejecutar el proyecto localmente.

### 1. Clonar el repositorio

```bash
git clone https://github.com/Albernio/smart-document-auditor
cd smart-document-auditor
```

### 2. Configurar el entorno Python

El proyecto requiere **Python 3.13**. Puedes gestionar el entorno y las dependencias con `uv` (recomendado) o con `venv` y `pip`.

#### Opción A: Usar uv (recomendado)

Instala `uv` siguiendo las instrucciones de su [documentación oficial](https://docs.astral.sh/uv/getting-started/installation/).

Comprueba que Python 3.13 está disponible o deja que `uv` lo instale si es necesario:

```bash
uv python install 3.13
```

Instala las dependencias del proyecto, incluidas las de desarrollo:

```bash
uv sync --extra test
```

Este comando crea o actualiza el entorno virtual `.venv`, instala las dependencias declaradas en `pyproject.toml` y mantiene el archivo `uv.lock` sincronizado.

Ejecuta los comandos del proyecto mediante `uv run`, por ejemplo:

```bash
uv run pytest -v
```

#### Opción B: Usar venv y pip

Comprueba que Python 3.13 está instalado y crea el entorno virtual:

```bash
python3.13 -m venv .venv
```

Activa el entorno virtual.

**Linux / macOS:**

```bash
source .venv/bin/activate
```

**Windows (PowerShell):**

```powershell
.venv\Scripts\Activate.ps1
```

Instala el proyecto y sus dependencias de desarrollo:

```bash
python -m pip install --upgrade pip
pip install -e ".[test]"
```

### 3. Iniciar PostgreSQL + pgvector

Necesitas tener **Docker instalado y en ejecución**.

```bash
docker compose up -d
```

Esto inicia PostgreSQL con la extensión `pgvector`, según la configuración de `compose.yaml` o `docker-compose.yml` del proyecto.

### 4. Crear el esquema de la base de datos

Si estás utilizando `uv`:

```bash
uv run python -c "from src.schema import create_tables; create_tables()"
```

Si estás utilizando `venv` y `pip`, con el entorno virtual activado:

```bash
python -c "from src.schema import create_tables; create_tables()"
```

Esto crea las tablas necesarias y habilita la extensión `vector`.

Este paso solo es necesario para inicializar el esquema de una base de datos nueva.

### 5. Ejecutar la aplicación

Si estás utilizando `uv`:

```bash
uv run streamlit run app.py
```

Si estás utilizando `venv` y `pip`, con el entorno virtual activado:

```bash
streamlit run app.py
```

Streamlit mostrará la URL local para acceder a la aplicación, normalmente `http://localhost:8501`.

### Notas

- **Python:** el proyecto requiere Python 3.13.
- **uv:** si utilizas este gestor, conserva `uv.lock` en el repositorio para reproducir las versiones de las dependencias.
- **PostgreSQL:** el servicio de base de datos debe estar en ejecución y sus credenciales deben coincidir con la configuración de la aplicación.
- **Ollama:** debes tener Ollama instalado y en ejecución, así como descargar el modelo LLM que utilice el proyecto.
- **Configuración:** revisa las variables de entorno y los archivos de configuración antes de iniciar la aplicación.