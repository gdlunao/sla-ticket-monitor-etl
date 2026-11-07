# 🔴 SLA Ticket Monitor ETL Pipeline

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Pandas](https://img.shields.io/badge/Pandas-2.2-150458.svg)](https://pandas.pydata.org/)
[![Google Cloud](https://img.shields.io/badge/Google%20Cloud-GCP%20API-4285F4.svg)](https://cloud.google.com/)
[![Security](https://img.shields.io/badge/Security-TLS%20587-green.svg)](#estrategia-de-ciberseguridad-y-manejo-de-secretos)

Este es un proyecto de ingeniería de datos y automatización que desarrollé para optimizar la supervisión de Acuerdos de Nivel de Servicio (SLA) en entornos operativos. Para su publicación en este repositorio, adapté el flujo utilizando registros simulados de atención al cliente alojados en Google Sheets.

El sistema se ejecuta como un **pipeline ETL in-memory** estructurado en Python. Su objetivo es conectarse a fuentes de datos operativas en la nube, transformar la información en tiempo real para detectar tickets que han superado su tiempo límite de atención, y despachar automáticamente un reporte analítico formateado en HTML hacia la gerencia mediante el protocolo seguro SMTP.

## ¿Qué se puede hacer en este proyecto?

* **Extracción automatizada (Extract):** Conectar de forma segura a la API de Google Drive y Google Sheets mediante Cuentas de Servicio (GCP) para leer matrices de datos operativas.
* **Procesamiento de datos (Transform):** Filtrar registros mediante la librería `pandas` utilizando reglas de negocio dinámicas (por ejemplo, extraer solo aquellos tickets con estado diferente a 'Cerrado' y con días SLA superiores al umbral permitido).
* **Generación de artefactos de auditoría:** Sobrescribir archivos `.json` locales en cada ejecución que funcionan como un *log* estructurado. Esto permite auditar la volumetría de los datos procesados sin afectar ni modificar la fuente original.
* **Notificación ejecutiva (Load/Notify):** Construir dinámicamente tablas HTML estilizadas y despacharlas por correo electrónico, evitando la dependencia de herramientas de visualización costosas o servidores dedicados.

## Elección de Tecnologías y Arquitectura

Para la realización de este proyecto elegí **Python** junto con su ecosistema de análisis de datos y redes. 

### ¿Por qué Python y Pandas sobre otras herramientas?
1. **Velocidad y Procesamiento In-Memory:** A diferencia de descargar archivos locales o escribir en discos repetidamente, `pandas` carga toda la matriz de Google Sheets directamente en la memoria RAM. Esto permite aplicar filtros complejos en fracciones de segundo.
2. **Desacoplamiento de Servicios:** Utilizar las librerías estándar de Python (`smtplib`, `email`) permite despachar alertas críticas de forma gratuita, aislando el envío a un puerto de red seguro (TLS 587).
3. **Escalabilidad Modular:** El proyecto sigue el **Principio de Responsabilidad Única (SRP)**. El código no es un script gigante, sino que está dividido lógicamente en `core/` (configuraciones), `modules/` (servicios aislados) y un orquestador principal (`main.py`).

### Arquitectura del Sistema (Monolito Modular)

```text
               +-----------------------+
               |  Google Sheets API    |
               +-----------+-----------+
                           |
                           v  [EXTRACT]
               +-----------------------+
               |  data_mock_extract    |  --> (artifacts/data_mock_extract.json)
               +-----------+-----------+
                           |
                           v  [TRANSFORM]
               +-----------------------+
               | data_mock_transformed |  --> (artifacts/data_mock_transformed.json)
               +-----------+-----------+
                           |
                           v  [LOAD / NOTIFY]
               +-----------------------+
               |   SMTP Email Alert    |  --> (Generación de Vista HTML)
               +-----------------------+
```

## Estrategia de Ciberseguridad

### Gestión de Secretos (.env y .gitignore)
En la industria profesional, exponer credenciales en repositorios públicos es un riesgo crítico. En este proyecto implementé la librería `python-dotenv` para mantener las llaves privadas de Google y las contraseñas de aplicación SMTP estrictamente en un archivo `.env` local. Este archivo, junto con la carpeta de auditoría `artifacts/`, están declarados en el `.gitignore` para asegurar que el repositorio de GitHub se mantenga 100% esterilizado.

### Conexiones de Salida Seguras (Outbound-Only)
Desde la perspectiva de seguridad de red, el script es inofensivo para la computadora que lo ejecuta. Al momento de notificar, realiza una petición de salida cifrada por el puerto **587 (TLS)** hacia los servidores de Google y cierra la conexión inmediatamente, garantizando que no se dejen puertos abiertos (*inbound*) que puedan ser vulnerados.

## Vista Previa de la Notificación (HTML Email)

A continuación, se muestra cómo el sistema renderiza la tabla de datos procesados directamente en la bandeja de entrada del destinatario, utilizando colores para resaltar la severidad del retraso:

<p align="center">
  <img src="docs/assets/email_preview.png" alt="Vista Previa de Alerta SLA" width="600"/>
</p>

## Estructura del repositorio

```text
sla-ticket-monitor-etl/
├── artifacts/                           # (Ignorado en Git) Archivos JSON generados en ejecución
├── core/
│   ├── config.py                        # Centralización de variables de entorno
│   └── logger.py                        # Configuración de telemetría para la consola
├── docs/
│   └── assets/
│       └── email_preview.png            # Captura de pantalla de la salida HTML
├── modules/
│   ├── google_sheets/
│   │   ├── client.py                    # Autenticación y token con Google Cloud
│   │   └── service.py                   # Lógica central de extracción y transformación
│   └── notifications/
│       ├── formatter.py                 # Maquetación de la vista HTML
│       └── email_service.py             # Transporte y despacho vía SMTP
├── .env                                 # (Ignorado en Git) Credenciales de sistema
├── .gitignore                           # Reglas de exclusión de seguridad
├── main.py                              # Script orquestador
├── requirements.txt                     # Dependencias instalables
└── README.md                            # Documentación principal
```

## Cómo ejecutarlo en entorno local

### Requisitos previos
* Tener instalado **Python 3.10** o superior.
* Contar con un archivo JSON de credenciales de una Cuenta de Servicio de Google Cloud (GCP) habilitada para Google Sheets.

### Secuencia de ejecución paso a paso

1. **Clonar el repositorio:**
   ```bash
   git clone https://github.com/gdlunao/sla-ticket-monitor-etl.git
   cd sla-ticket-monitor-etl
   ```

2. **Crear y activar un entorno virtual:**
   ```bash
   python -m venv venv
   # En Windows:
   venv\Scripts\activate
   # En Linux/macOS:
   source venv/bin/activate
   ```

3. **Instalar las dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar las credenciales (Archivo `.env`):**
   Crea un archivo llamado `.env` en la raíz del proyecto y agrega los siguientes parámetros (sin comillas):
   ```env
   SPREADSHEET_NAME=Nombre_De_Tu_Google_Sheet
   
   GCP_PROJECT_ID=tu-proyecto-gcp
   GCP_PRIVATE_KEY_ID=tu-key-id
   GCP_PRIVATE_KEY="-----BEGIN PRIVATE KEY-----\ntu-key-aqui\n-----END PRIVATE KEY-----\n"
   GCP_CLIENT_EMAIL=tu-service-account@proyecto.iam.gserviceaccount.com
   GCP_CLIENT_ID=123456789
   
   SENDER_EMAIL=tu_correo_emisor@gmail.com
   SENDER_PASSWORD=contraseña_de_aplicacion_16_letras
   RECEIVER_EMAIL=correo_destino@gmail.com
   ```

5. **Ejecutar el pipeline:**
   ```bash
   python main.py
   ```
   *Nota: La consola solo mostrará los metadatos (cantidad de filas procesadas, éxito de la conexión), manteniendo completamente oculta cualquier información sensible de los tickets.*

## ¿Qué he comprobado hasta ahora?

Durante el desarrollo de esta versión validé los siguientes puntos:
* Conexión ininterrumpida a la API de Drive y Sheets gestionando permisos *OAuth2*.
* Sanitización de logs: Verifiqué que el módulo `logger.py` suprima la impresión de datos en crudo, protegiendo así la privacidad (PII) de los usuarios y empleados.
* Desacoplamiento de vistas: Separación total de la lógica de red (SMTP) del diseño visual (HTML) aplicando el patrón SRP.
* Comportamiento idempotente: El sistema genera los artefactos JSON (`data_mock_transformed.json`) sobrescribiendo los anteriores en cada ejecución para no generar basura digital.

## Sobre este proyecto

Este repositorio nace de mi interés por integrar la **ingeniería de datos, automatización de procesos y los principios de ciberseguridad**.

Me apoyé en herramientas de inteligencia artificial como asistente de código para explorar la configuración óptima de Cuentas de Servicio en GCP, refinar la estructura de la arquitectura modular y optimizar la redacción técnica de este documento. Comparto este trabajo como muestra de mi capacidad de análisis y desarrollo de soluciones orientadas a la toma de decisiones.

**Perfil de GitHub:** [`@gdlunao`](https://github.com/gdlunao)

## Glosario - Librerías de Python

Este cuadro explica de forma sencilla las librerías utilizadas en el archivo `requirements.txt` y en el código base:

| Librería | Propósito en el proyecto |
| :--- | :--- |
| **`pandas`** | Herramienta principal de procesamiento de datos. Permite cargar la información en estructuras llamadas `DataFrames` para filtrar y calcular métricas en memoria. |
| **`gspread`** | Cliente API que facilita la lectura y manipulación directa de documentos de Google Sheets desde Python. |
| **`oauth2client`** | Maneja la seguridad de Google. Traduce las credenciales estáticas de GCP en un token temporal autorizado para consumir la API. |
| **`python-dotenv`** | Librería de seguridad que toma las claves secretas guardadas en el archivo `.env` y las inyecta temporalmente en el entorno del sistema operativo. |
| **`smtplib` / `email`** | (Nativas) Bibliotecas que estructuran el correo electrónico (asunto, cuerpo HTML) y establecen la conexión con el servidor de Gmail. |
| **`json` / `os`** | (Nativas) Módulos utilizados para la gestión de directorios y la exportación de los resultados procesados como artefactos auditables. |

## Glosario Técnico de Arquitectura

| Término | Qué significa en la industria |
| :--- | :--- |
| **ETL (Extract, Transform, Load)** | Pipeline (tubería de datos) que **Extrae** la información bruta, la **Transforma** aplicando reglas de negocio y la **Carga** (o envía) a un destino. |
| **Monolito Modular** | Arquitectura donde todo el código vive en un solo lugar fácil de ejecutar, pero organizado rígidamente por responsabilidades lógicas separadas. |
| **Procesamiento In-Memory** | Trabajar con grandes volúmenes de datos directamente en la memoria RAM para maximizar la velocidad, en lugar de interactuar lentamente con discos duros. |
| **Artefactos (Artifacts)** | Archivos (como JSON, CSV o Logs) generados colateralmente por el código para dejar una huella auditable de lo que procesó el sistema. |
| **SRP (Single Responsibility Principle)** | Principio de buen diseño de software. Dicta que un archivo debe ocuparse de una sola cosa (ej. separar el diseño HTML del envío de red SMTP). |
| **Service Account (Cuenta de Servicio)** | Una cuenta especial de Google Cloud creada para que sistemas automáticos puedan acceder a servicios de Google sin intervención humana. |
| **SMTP / TLS 587** | Protocolo para enviar correos. Al usar TLS por el puerto 587, el mensaje viaja por internet en un túnel encriptado. |
| **CI / CD (Integración / Despliegue Continuo)** | Práctica que permite llevar este script local a la nube (ej. GitHub Actions) para que se ejecute solo, todos los días a una hora programada. |