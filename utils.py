"""
Utility functions used by example notebooks
"""
import sys        
sys.path.append('/home/tele/notebook-samples/sentinelhub')
from typing import Any, Optional, Tuple
from sentinelhub import (SHConfig, DataCollection, SentinelHubCatalog, SentinelHubRequest, BBox, bbox_to_dimensions, CRS, MimeType, Geometry)
import numpy as np
import os
import datetime
import matplotlib.pyplot as plt
import pandas as pd
import requests
from creds import *



    
# Import credentials
def get_access_token(username: str, password: str) -> str:
    data = {
        "client_id": "cdse-public",
        "username": username,
        "password": password,
        "grant_type": "password",
        }
    try:
        r = requests.post("https://identity.dataspace.copernicus.eu/auth/realms/CDSE/protocol/openid-connect/token",data=data)
        r.raise_for_status()
    except Exception as e:
        raise Exception(
            f"Access token creation failed. Reponse from the server was: {r.json()}")
    return r.json()["access_token"]
    

def download_Isat(start_date, end_date, north, south, east, west, data_collection, directory_save):
	"""
	Permite descargar imágenes satelitales de Copernicus Data Space Ecosystem.

	Args:
	start_date (str): Fecha de inicio en formato 'YYYY-MM-DD'.
	end_date (str): Fecha de fin en formato 'YYYY-MM-DD'.
	north (float): Coordenada norte del área de interés.
	south (float): Coordenada sur del área de interés.
	east (float): Coordenada este del área de interés.
	west (float): Coordenada oeste del área de interés.
	data_collection (str): Nombre de la colección de datos (e.g., "SENTINEL-2").
	directory_save (str): Directorio donde se guardarán las imágenes descargadas.
	username (str): Nombre de usuario para la autenticación.
	password (str): Contraseña para la autenticación.

	Example:
	download_Isat("2023-04-01", "2023-05-01", -34.81, -34.82, -57.8900, -57.8961, "SENTINEL-2", "/media/tele/Seagate Expansion Drive/S2_timeSeries_2023/", "user", "pass")
	"""
	try:
		# Validación de fechas
		#datetime.strptime(start_date, '%Y-%m-%d')
		#datetime.strptime(end_date, '%Y-%m-%d')

		# Construcción del área de interés (AOI)
		aoi = f"POLYGON(({west} {north}, {east} {north}, {east} {south}, {west} {south}, {west} {north}))"

		# Solicitud para obtener los datos del catálogo
		url = (
		   f"https://catalogue.dataspace.copernicus.eu/odata/v1/Products?"
		   f"$filter=Collection/Name eq '{data_collection}' and OData.CSC.Intersects(area=geography'SRID=4326;{aoi}') "
		   f"and ContentDate/Start gt {start_date}T00:00:00.000Z and ContentDate/Start lt {end_date}T00:00:00.000Z"
		)
		response = requests.get(url)
		response.raise_for_status()
		json_data = response.json()

		# Creación de un DataFrame con los datos obtenidos
		df = pd.DataFrame.from_dict(json_data["value"])

		# Descarga de los productos
		for index, row in df.iterrows():
			if 'L1C' in row['Name']:
				access_token = get_access_token(username, password)
				product_url = f"https://zipper.dataspace.copernicus.eu/odata/v1/Products({row['Id']})/$value"
				headers = {"Authorization": f"Bearer {access_token}"}

				with requests.get(product_url, headers=headers, stream=True) as r:
					r.raise_for_status()
					file_path = f"{directory_save}{row['Name']}.zip"
					with open(file_path, 'wb') as file:
						for chunk in r.iter_content(chunk_size=8192):
							if chunk:
								file.write(chunk)
		print("Descarga completada.")
	except Exception as e:
		print(f"Error: {e}")

	return

