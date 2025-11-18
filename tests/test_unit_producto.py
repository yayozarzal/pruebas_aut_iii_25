# tests/test_unit_producto.py
import json
from app import crud


def _setup_temp_db(tmp_path, monkeypatch, initial_data, titulo=""):
    """
    Crea un archivo db.json temporal y hace que crud.DB_FILE apunte ahí.
    Además imprime el estado inicial, como en tus otras pruebas.
    """
    temp_db = tmp_path / "db.json"
    temp_db.write_text(json.dumps(initial_data, ensure_ascii=False, indent=4))

    # Redirigimos el archivo de BD que usa crud
    monkeypatch.setattr(crud, "DB_FILE", str(temp_db))

    print(f"\n[SETUP {titulo}] Base de datos temporal inicial:\n")
    print(json.dumps(initial_data, ensure_ascii=False, indent=4))
    print("--------------------------------------------------- \n")

    return temp_db


def test_create_producto_db_categoria_existente(tmp_path, monkeypatch):
    # 1. Preparamos una BD temporal con una categoría existente
    initial_data = {
        "categorias": [
            {"id": 1, "nombre": "Electrónica"}
        ],
        "productos": []
    }
    temp_db = _setup_temp_db(
        tmp_path,
        monkeypatch,
        initial_data,
        titulo="CATEGORÍA EXISTENTE",
    )

    # 2. Ejecutamos la función que queremos probar (UNITARIA)
    producto = crud.create_producto_db("Smartphone", categoria_id=1)

    print("\n[UNIT] Producto creado por create_producto_db:\n")
    print(json.dumps(producto, ensure_ascii=False, indent=4))
    print("--------------------------------------------------- \n")

    # 3. Aserciones sobre el resultado retornado
    assert producto["nombre"] == "Smartphone"
    assert producto["categoria_id"] == 1
    # new_id arranca desde 100 en tu lógica, así que el primero será 101
    assert producto["id"] == 101

    # 4. Verificamos que realmente se haya guardado en el archivo JSON
    data_final = json.loads(temp_db.read_text())

    print("[UNIT] Estado final de la base de datos temporal:\n")
    print(json.dumps(data_final, ensure_ascii=False, indent=4))
    print("--------------------------------------------------- \n")

    assert len(data_final["productos"]) == 1
    prod_guardado = data_final["productos"][0]
    assert prod_guardado["nombre"] == "Smartphone"
    assert prod_guardado["categoria_id"] == 1
    assert prod_guardado["id"] == 101



