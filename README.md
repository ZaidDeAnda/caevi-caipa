# Diagnóstico CAEVI / CAIPA

Aplicación desarrollada en **Streamlit** para capturar, almacenar y visualizar información de diagnóstico de centros CAEVI y CAIPA.

## Descripción

Este proyecto contiene formularios interactivos para levantar información sobre recursos humanos, servicios brindados, servicios disponibles en instalaciones y condiciones de mantenimiento de centros CAEVI y CAIPA.

La información capturada se almacena en una base de datos **MongoDB**, lo que permite posteriormente consultar y visualizar los resultados mediante paneles interactivos.

## Funcionalidades principales

- Captura de cuestionario para centros CAEVI.
- Captura de cuestionario para centros CAIPA.
- Registro de información sobre recursos humanos.
- Registro de servicios brindados durante el último año.
- Registro de servicios disponibles en las instalaciones.
- Registro de condiciones de mantenimiento.
- Almacenamiento de respuestas en MongoDB.
- Visualización de resultados del cuestionario CAIPA.
- Gráficas interactivas con Plotly.
- Conexión configurable mediante archivo `config.yaml`.

## Archivos principales

```text
.
├── CAEVI.py
├── CAIPA.py
├── CAIPA_vis.py
├── caevi_nb.ipynb
├── caipa_vis.ipynb
└── utils
    ├── caipa_graphs.py
    ├── config.py
    ├── database.py
    └── dict_utils.py
```

### `CAEVI.py`

Aplicación principal para capturar el cuestionario de diagnóstico correspondiente a centros CAEVI.

El formulario registra información relacionada con:

- Recursos humanos.
- Manuales de organización y procedimientos.
- Subsidios.
- Servicios brindados.
- Ubicación y dirección del centro.
- Presupuesto.
- Servicios básicos.
- Condiciones de mantenimiento.

Los registros se almacenan en la base de datos `caevi`, dentro de la colección `registry`.

### `CAIPA.py`

Aplicación principal para capturar el cuestionario de diagnóstico correspondiente a centros CAIPA.

El formulario registra información relacionada con:

- Recursos humanos.
- Manual de organización.
- Personal subsidiado.
- Personal capacitado en el modelo CAIPA 2.0.
- Acciones del centro dentro del plan municipal.
- Subsidios.
- Servicios brindados.
- Ubicación y dirección del centro.
- Adscripción administrativa.
- Servicios básicos.
- Condiciones de mantenimiento.

Los registros se almacenan en la base de datos `caipa`, dentro de la colección `registry`.

### `CAIPA_vis.py`

Panel de visualización para analizar los resultados del cuestionario CAIPA.

Incluye visualizaciones sobre:

- Recursos humanos.
- Conteo de servicios ofertados.
- Servicios disponibles.
- Mantenimiento de instalaciones.

### `utils/config.py`

Contiene la clase `Config`, encargada de leer el archivo `config.yaml` con las credenciales de conexión a MongoDB.

### `utils/database.py`

Contiene funciones auxiliares para:

- Crear el cliente de conexión a MongoDB.
- Convertir cursores de MongoDB en DataFrames de Pandas.
- Consultar información de centros.
- Actualizar direcciones.
- Cargar imágenes.
- Completar registros de centros.

### `utils/dict_utils.py`

Contiene diccionarios utilizados para mapear los campos técnicos del formulario a etiquetas legibles para el usuario.

Incluye diccionarios para:

- Recursos humanos CAEVI.
- Recursos humanos CAIPA.
- Servicios CAEVI.
- Servicios CAIPA.
- Servicios básicos.
- Mantenimiento.

### `utils/caipa_graphs.py`

Contiene funciones para transformar los registros de MongoDB en DataFrames útiles para generar gráficas de CAIPA con Plotly.

## Requisitos

Para ejecutar el proyecto se recomienda contar con Python 3.8 o superior.

Instala las dependencias principales con:

```bash
pip install streamlit pandas plotly pymongo pyyaml pillow
```

## Configuración requerida

Para que el proyecto funcione correctamente, es necesario crear un archivo llamado `config.yaml` en la raíz del repositorio.

Este archivo debe contener las credenciales de conexión a MongoDB con el siguiente formato:

```yaml
db_mongo:
  user: "TU_USUARIO_MONGO"
  password: "TU_PASSWORD_MONGO"
  cluster: "TU_CLUSTER_MONGO"
```

Ejemplo:

```yaml
db_mongo:
  user: "usuario_demo"
  password: "password_demo"
  cluster: "cluster0.xxxxx.mongodb.net"
```

El proyecto utiliza estos valores para construir la conexión a MongoDB con el siguiente formato:

```python
mongodb+srv://{user}:{password}@{cluster}/?retryWrites=true&w=majority
```

## Ejecución

Para ejecutar el formulario CAEVI:

```bash
streamlit run CAEVI.py
```

Para ejecutar el formulario CAIPA:

```bash
streamlit run CAIPA.py
```

Para ejecutar el panel de visualización CAIPA:

```bash
streamlit run CAIPA_vis.py
```

Después de ejecutar cualquiera de los comandos, Streamlit abrirá la aplicación en el navegador.

## Uso esperado

1. Crear el archivo `config.yaml` con las credenciales de MongoDB.
2. Instalar las dependencias del proyecto.
3. Ejecutar el formulario correspondiente con Streamlit.
4. Completar la información solicitada.
5. Presionar el botón **Enviar**.
6. Confirmar que la información fue almacenada en MongoDB.
7. Consultar los resultados desde el panel de visualización.

## Bases de datos utilizadas

El proyecto espera trabajar con dos bases de datos principales en MongoDB:

```text
caevi
└── registry

caipa
└── registry
```

La base `caevi` almacena los registros del formulario CAEVI.

La base `caipa` almacena los registros del formulario CAIPA y es utilizada por el panel `CAIPA_vis.py` para generar visualizaciones.

## Tecnologías utilizadas

- Python
- Streamlit
- Pandas
- Plotly
- MongoDB
- PyMongo
- YAML
- Pillow

## Consideraciones importantes

El archivo `config.yaml` contiene credenciales sensibles, por lo que no debe subirse al repositorio público.

Se recomienda agregarlo al archivo `.gitignore`:

```text
config.yaml
```

También se recomienda crear un archivo de ejemplo sin credenciales reales:

```text
config.example.yaml
```

Ejemplo de `config.example.yaml`:

```yaml
db_mongo:
  user: "TU_USUARIO_MONGO"
  password: "TU_PASSWORD_MONGO"
  cluster: "TU_CLUSTER_MONGO"
```

## Objetivo del proyecto

Facilitar la captura estructurada y el análisis de información operativa sobre centros CAEVI y CAIPA, permitiendo almacenar los resultados en MongoDB y visualizar indicadores relevantes para seguimiento institucional.

## Estado del proyecto

Proyecto en desarrollo para uso interno en actividades de diagnóstico, seguimiento y visualización de información relacionada con centros CAEVI y CAIPA.