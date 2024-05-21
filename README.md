# ndvi_v1.0
# Cálculo del NDVI sobre el Embalse Los Molinos usando datos LandSAT 8
## Introducción
Este repositorio contiene un Notebook para estimar el Índice de Vegetación de Diferencia Normalizada (NDVI) con imágenes LandSAT 8 sobre el Embalse Los Molinos. La Notebook se enfoca en la estima del NDVI utilizando el Índice Modificado de Agua de Diferencia Normalizada (MNDWI) para generar una máscara sobre el Embalse, esto con el fin de visualizar los resultados unicamente sobre el Embalse.
## Instalación
Para su uso deberá ejecutar la Notebook (Python 3.9.13) en el programa de su preferencia. El repositorio contiene los datos LandSAT8 del 10 de Febrero de 2024 sobre el Embalse Los Molinos, puede descargar el repositorio y ejecutar el ejemplo predeterminado.
1. Clonar el repositorio (git clone https://github.com/fluiscruz/ndvi_v1.0.git)
2. Abrir la Notebook en Visual Studio Code, Jupyter Notebook o en el programa de su elección.
3. Ejecutar las celdas. Los comentarios indican que hace cada línea de código.

Librerías utilizadas
- *rasterio*
- *numpy*
- *matplotlib*
- *zipfile*
- *os*
## Ejecución
1. Ubicarse en el directorio de repositorio.
2. Definir un directorio de trabajo, aquí se ubicarán los datos.
3. Ubicar los datos LandSAT8 en formato *.zip en el directorio de trabajo, no es necesario descomprmirlos.
4. Ejecutar la Notebook.
## Autor
Ing. Luis Cruz

ORCID 0000-0003-4176-7497
