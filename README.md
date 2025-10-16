# Análisis de Datos de Nombres con Python

Este proyecto es un script de Python diseñado para consolidar, limpiar y analizar datos de nombres de personas a partir de múltiples archivos CSV. El objetivo es extraer insights y generar visualizaciones sobre las tendencias de nombres a lo largo de los años.

## ✨ Características Principales

* **Unificación de Datos:** Combina automáticamente múltiples archivos CSV en un único DataFrame de Pandas.
* **Limpieza de Datos:** Filtra entradas inválidas y normaliza los nombres para un análisis preciso.
* **Análisis Estadístico:** Calcula datos clave como el nombre más popular, el año con más registros y el nombre más largo.
* **Visualización de Datos:** Genera 3 gráficos claros y descriptivos utilizando Matplotlib:
    1.  Distribución porcentual de registros por año.
    2.  Evolución histórica de nombres específicos (ej: Juan y María).
    3.  Nombre más popular para cada año analizado.

## 🚀 Cómo Utilizarlo

Para ejecutar este script en tu máquina local, sigue estos pasos:

1.  **Clona el repositorio:**
    ```bash
    git clone [https://github.com/fabrizionav/python-analisis-de-datos.git](https://github.com/fabrizionav/python-analisis-de-datos.git)
    ```

2.  **Navega a la carpeta del proyecto:**
    ```bash
    cd python-analisis-de-datos
    ```

3.  **Crea un entorno virtual (recomendado):**
    ```bash
    python -m venv venv
    ```
    * Para activarlo en Windows (Git Bash): `source venv/Scripts/activate`
    * Para activarlo en Linux/Mac: `source venv/bin/activate`

4.  **Instala las dependencias necesarias:**
    ```bash
    pip install -r requirements.txt
    ```

5.  **Ejecuta el script:**
    ```bash
    python tu-nombre-de-script.py
    ```
    *(**Nota:** ¡Recuerda cambiar `tu-nombre-de-script.py` por el nombre real de tu archivo Python!)*

## 🛠️ Tecnologías Utilizadas

* **Python 3**
* **Pandas:** Para la manipulación y análisis de datos.
* **Matplotlib:** Para la creación de gráficos y visualizaciones.
