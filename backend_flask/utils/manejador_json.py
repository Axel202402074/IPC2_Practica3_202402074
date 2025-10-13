import json, os

ARCHIVO = 'backend_flask/inventario.json'

def inicializar_inventario():
    if not os.path.exists(ARCHIVO):
        with open(ARCHIVO, 'w', encoding='utf-8') as f:
            json.dump([], f, indent=4, ensure_ascii=False)

def leer_inventario():
    try:
        with open(ARCHIVO, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return []

def guardar_inventario(productos):
    with open(ARCHIVO, 'w', encoding='utf-8') as f:
        json.dump(productos, f, indent=4, ensure_ascii=False)

def generar_id(productos):
    if not productos:
        return 1
    return max(p['id'] for p in productos) + 1
