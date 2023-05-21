# API PRUEBA TECNICA SPOT

La API es un backend que permite administrar datos de cámaras. Proporciona endpoints para recuperar, crear, eliminar y cargar datos de cámaras en Azure Blob Storage.

## configuracion 
### crear un entorno virtual 
    windows:

    crear entorno: py -m venv venv 
    activar entorno:  .\venv\scripts\activate

    Linux o macOs:

    crear entorno: python3 -m venv venv   
    activar entorno : source venv/bin/activate


Se requiere un archivo `.env` en la carpeta `app` que contenga la siguiente configuración:
    El archivo `.env` debe contener la clave secreta (`SECRET_KEY`) necesaria para la aplicación y la cadena de conexión (`CONNECTION_STRING`) para acceder a la cuenta de Azure Blob Storage. 
    Este archivo `.env` se utilizará para cargar la configuración de la aplicación durante la ejecución.
    esto se enviara por correo.

## Instalación de dependencias

Para ejecutar la API, se requiere instalar las dependencias especificadas en el archivo `requirements.txt`. Puedes hacerlo ejecutando el siguiente comando:

    pip install -r requirements.txt
    

## configuracion del servidor
Desde la línea de comandos, navega hasta la raíz del proyecto y ejecuta el siguiente comando:

    uvicorn main:app --reload 

## Pruebas con pytest

Las pruebas unitarias y de integración se realizaron utilizando el framework de pruebas pytest.
A continuación se explica cómo ejecutar las pruebas y obtener resultados detallados.

**Ejecución de las pruebas:**

Para ejecutar las pruebas, se debe utilizar el siguiente comando:

    pytest -v


## Funcionalidad

- Listar datos de cámaras: Permite obtener una lista paginada de datos de cámaras desde la base de datos.
- Obtener datos de cámara por ID: Recupera un registro específico de datos de cámara mediante su ID.
- Crear datos de cámara: Crea un nuevo registro de datos de cámara en la base de datos y carga la imagen correspondiente en Azure Blob Storage.
- Eliminar datos de cámara: Elimina un registro de datos de cámara de la base de datos.
- Cargar datos de cámara por lotes: Permite cargar múltiples registros de datos de cámaras en la base de datos y Azure Blob Storage de manera eficiente.

## Arquitectura y tecnologías utilizadas

- Framework: FastAPI
- Base de datos: SQLAlchemy
- Almacenamiento de imágenes: Azure Blob Storage

## Detalle del funcionamiento.


### Listar datos de cámaras

Recupera una lista paginada de datos de cámaras desde la base de datos.

Endpoint: `GET /cameras`

Parámetros de consulta:
- `page` (opcional): Número de página (por defecto: 1).
- `page_size` (opcional): Tamaño de la página (por defecto: 10, máximo: 100).

### Obtener datos de cámara por ID

Recupera un registro específico de datos de cámara mediante su ID.

Endpoint: `GET /cameras/{id}`

Parámetros de ruta:
- `id`: ID del registro de datos de cámara.

### Crear datos de cámara

Crea un nuevo registro de datos de cámara en la base de datos y carga la imagen correspondiente en Azure Blob Storage.

Endpoint: `POST /cameras`

Parámetros de solicitud:
- `data`: Objeto JSON con los datos de la cámara.

### Eliminar datos de cámara

Elimina un registro de datos de cámara de la base de datos.

Endpoint: `DELETE /cameras/{id}`

Parámetros de ruta:
- `id`: ID del registro de datos de cámara a eliminar.

### Cargar datos de cámara por lotes

Carga múltiples registros de datos de cámaras en la base de datos y Azure Blob Storage de manera eficiente.

Endpoint: `POST /cameras/upload_list`

Parámetros de solicitud:
- `list_data`: Lista de objetos JSON con los datos de las cámaras a cargar.


## Autor

Este proyecto ha sido desarrollado por Daniel Eduardo Rubiano Meneses


