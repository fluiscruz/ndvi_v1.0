# Importamos las librerías necesarias
import rasterio
import numpy as np
import matplotlib.pyplot as plt
import zipfile
import os


# Descomprimimos la imagen satelital de .zip a .tif

# Definimos el directorio de trabajo.
work_dir = './test/'

# Buscamos la imagen satelital, la cual sera el archivo con la extension .zip
for file in os.listdir(work_dir):
    if file.endswith('.zip'):
        archivo_zip = file
        ruta_zip = work_dir + archivo_zip

# Verificamos que se haya encontrado el archivo .zip
if not archivo_zip:
    print('No se encontró el archivo .zip')
else:
    print(f'Archivo .zip encontrado: {archivo_zip}')

# Definimos la Ruta de extracción del archivo .zip
ruta_extraccion = work_dir

# Extraemos las bandas del archivo .zip
with zipfile.ZipFile(ruta_zip, 'r') as zip_ref:
    zip_ref.extractall(ruta_extraccion)

# Listamos los archivos extraidos
archivos_extraidos = os.listdir(ruta_extraccion)
print('Archivos extraidos:')
for archivo in archivos_extraidos:
    print(archivo)


# Ubicamos automaticamente las bandas NIR y RED. Esto solo en caso de usar LandSAT8.
nir = [ruta_extraccion + i for i in os.listdir(ruta_extraccion) if 'B5' in i][0]
red = [ruta_extraccion + i for i in os.listdir(ruta_extraccion) if 'B4' in i][0]

# En caso de usar otra imagen satelital, se debe definir manualmente la ruta de las
# bandas NIR y RED. Por ejemplo:
# nir = './ruta_de_la_banda_nir.tif'
# red = './ruta_de_la_banda_red.tif'


# Abrimos las bandas NIR y RED con rasterio y realizamos un analisis exploratorio de
# los metadatos.

with rasterio.open(nir) as src:
    nir_src = src.read(1).astype(np.float32)
    print("------------------------------------------------------")
    print('Metadatos de la Banda NIR:')
    print("Tamaño de la imagen: ", src.width, "x", src.height)
    print("Número de bandas: ", src.count)
    print("Coordenadas de la esquina superior izquierda: ", src.transform * (0, 0))
    print("Resolución espacial: ", src.res)
    print("Sistema de referencia de coordenadas: ", src.crs)
    print("Valor de NoData: ", src.nodata)
    print("Tipo de dato: ", src.dtypes[0])
    print("Rango de valores: ", np.nanmin(src.read(1)), "-", np.nanmax(src.read(1)))
    print("------------------------------------------------------")

with rasterio.open(red) as src:
    red_src = src.read(1).astype(np.float32)
    print('Metadatos de la Banda RED:')
    print("Tamaño de la imagen: ", src.width, "x", src.height)
    print("Número de bandas: ", src.count)
    print("Coordenadas de la esquina superior izquierda: ", src.transform * (0, 0))
    print("Resolución espacial: ", src.res)
    print("Sistema de referencia de coordenadas: ", src.crs)
    print("Valor de NoData: ", src.nodata)
    print("Tipo de dato: ", src.dtypes[0])
    print("Rango de valores: ", np.nanmin(src.read(1)), "-", np.nanmax(src.read(1)))
    print("------------------------------------------------------")


# Definimos los valores de los percentiles 2.5 y 97.5 para las bandas NIR y RED
nir_percentiles = np.percentile(nir_src, [2.5, 97.5])
red_percentiles = np.percentile(red_src, [2.5, 97.5])

# Visualizamos los valores de los percentiles 2.5 y 97.5 para las bandas NIR y RED
print("------------------------------------------------------")
print("Niveles de significancia para la Banda NIR:")
print("Percentil 2.5: ", nir_percentiles[0])
print("Percentil 97.5: ", nir_percentiles[1])
print("------------------------------------------------------")
print("Niveles de significancia para la Banda RED:")
print("Percentil 2.5: ", red_percentiles[0])
print("Percentil 97.5: ", red_percentiles[1])
print("------------------------------------------------------")


# Calculamos el NDVI y su respectivo histograma en el mismo grafico
ndvi = (nir_src - red_src) / (nir_src + red_src)

# En caso deseemos trabajar con las imagenes con los outliers enmascarados, estimamos
# el NDVI con la siguiente expresion
# ndvi = (nir_src_masked - red_src_masked) / (nir_src_masked + red_src_masked)


# Definimos la Ruta de las bandas GREEN y SWIR de la imagen satelital. Solo en caso
# de usar datos LandSAT 8.
green = [ruta_extraccion + i for i in os.listdir(ruta_extraccion) if 'B3' in i][0]
swir = [ruta_extraccion + i for i in os.listdir(ruta_extraccion) if 'B6' in i][0]

# En caso de usar otra imagen satelital, se debe definir manualmente la ruta de las
# bandas GREEN y SWIR. Por ejemplo:
# green = './ruta_de_la_banda_green.tif'
# swir = './ruta_de_la_banda_swir.tif'

# Abrimos las bandas GREEN y SWIR con rasterio
with rasterio.open(swir) as src:
    swir_src = src.read(1).astype(np.float32)

with rasterio.open(green) as src:
    green_src = src.read(1).astype(np.float32)


# Definimos los valores de los percentiles 2.5 y 97.5 para las bandas GREEN y SWIR
green_percentiles = np.percentile(green_src, [2.5, 97.5])
swir_percentiles = np.percentile(swir_src, [2.5, 97.5])

# Visualizamos los valores de los percentiles 2.5 y 97.5 para las bandas GREEN y SWIR
print("------------------------------------------------------")
print("Niveles de significancia para la Banda GREEN:")
print("Percentil 2.5: ", green_percentiles[0])
print("Percentil 97.5: ", green_percentiles[1])
print("------------------------------------------------------")
print("Niveles de significancia para la Banda SWIR:")
print("Percentil 2.5: ", swir_percentiles[0])
print("Percentil 97.5: ", swir_percentiles[1])
print("------------------------------------------------------")


# Enmascaramos los valores atípicos en las bandas GREEN y SWIR, los reemplazamos por NaN
# y los guardamos en una nueva variable.
# green_src_masked = np.where((green_src < green_percentiles[0]) | (green_src > green_percentiles[1]),
#                          np.nan, green_src)
# swir_src_masked = np.where((swir_src < swir_percentiles[0]) | (swir_src > swir_percentiles[1]),
#                          np.nan, swir_src)


# Calculamos el MNDWI y su respectivo histograma en el mismo grafico
mndwi = (green_src - swir_src) / (green_src + swir_src)

# En caso deseemos trabajar con las imagenes con los outliers enmascarados, estimamos
# el MNDWI con la siguiente expresion
# mndwi = (green_src_masked - swir_src_masked) / (green_src_masked + swir_src_masked)


# Definimos el umbral y creamos la mascara binaria para el agua
umbral_agua = 0
mascara_agua = mndwi > umbral_agua


# Ahora, con esta mascara binaria, cortamos la imagen NDVI para mostrar solo los
# pixeles correspondientes a las zonas con agua.

mascara_emb = mascara_agua.astype(bool)
ndvi_emb = ndvi.copy()
ndvi_emb[~mascara_emb] = np.nan

# Estimamos los niveles de significancia (inferior y superior) para un alfa = 0.05 para el
# NDVI estimado. Estos umbrales nos permitirán realzar la imagen.

# Definimos los valores de los percentiles 2.5 y 97.5
ndvi_emb_percentiles = np.percentile(ndvi_emb[~np.isnan(ndvi_emb)], [2.5, 97.5])


# Guardamos el NDVI en el lago en un archivo .tif.
fecha = nir.split('/')[-1].split('.')[0]
ndvi_emb_path = work_dir + f'ndvi_{fecha}_L08.tif'
with rasterio.open(nir) as src:
    profile = src.profile
    profile.update(dtype=rasterio.float32)
    profile.update(count=1)
    profile.update(nodata=None)
    with rasterio.open(ndvi_emb_path, 'w', **profile) as dst:
        dst.write(ndvi_emb.astype(rasterio.float32), 1)
print(f'Guardando el NDVI en el lago en: {ndvi_emb_path}')


# Graficamos el NDVI en el lago ajustando los colores a los umbrales de significancia
# y su histograma con los umbrales de significancia como lineas verticales.
fig, axs = plt.subplots(1, 2, figsize=(14, 7))
im = axs[0].imshow(ndvi_emb, cmap='viridis', vmin=ndvi_emb_percentiles[0],
                     vmax=ndvi_emb_percentiles[1])
axs[0].set_title('NDVI Embalse Los Molinos')
plt.colorbar(im, ax=axs[0], orientation='vertical', label='NDVI')
axs[1].hist(ndvi_emb.ravel(), bins=100, color='g', alpha=0.7)
axs[1].axvline(ndvi_emb_percentiles[0], color='r', linestyle='dashed', linewidth=1)
axs[1].axvline(ndvi_emb_percentiles[1], color='r', linestyle='dashed', linewidth=1)
axs[1].set_title('Histograma')
axs[1].set_xlabel('NDVI')
axs[1].set_ylabel('Frecuencia')
plt.xlim(ndvi_emb_percentiles[0] * 1.5, ndvi_emb_percentiles[1] * 1.5)
plt.legend(['Percentil 2.5', 'Percentil 97.5'], loc='upper right')
plt.show()
