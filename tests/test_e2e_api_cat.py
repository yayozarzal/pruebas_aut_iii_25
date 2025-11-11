from unittest.mock import patch
from app.crud import create_categoria_db
import json

MOCK_DB_DATA = {
    "categorias": [{"id": 10, "nombre": "Prueba"}],
    "productos" : []
    
}

def test_unit_create_categoria_logic():
    nombre_cat = "categoria unitaria"
    with patch("app.crud._load_db",  return_value= MOCK_DB_DATA.copy()) as mock_load, \
         patch("app.crud._save_db") as mock_save:
         resultado = create_categoria_db(nombre_cat)
         assert resultado["nombre"] == nombre_cat
         assert resultado["id"] == 11  # Siguiente ID disponible
         MOCK_DB_DATA
         
         mock_save.assert_called_once()
         
         datos_guardados = mock_save.call_args[0][0]
         
         print ("\n--- Datos guardados en la base de datos mockeada --- ")
         print (json.dumps(datos_guardados, indent=4))
         print ("--------------------------------------------------- \n")
         
         assert any(cat['nombre'] == nombre_cat for cat in datos_guardados['categorias'])
         
       