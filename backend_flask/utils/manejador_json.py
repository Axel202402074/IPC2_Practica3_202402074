import json
import os

ARCHIVO = 'backend_flask/inventario.json'

def inicializar_inventario():
    try:
        # Crear directorio si no existe
        directorio = os.path.dirname(ARCHIVO)
        if directorio and not os.path.exists(directorio):
            os.makedirs(directorio)
            print(f" Directorio creado: {directorio}")
        
        # Crear archivo si no existe
        if not os.path.exists(ARCHIVO):
            with open(ARCHIVO, 'w', encoding='utf-8') as f:
                json.dump([], f, indent=4, ensure_ascii=False)
            print(f" Archivo de inventario creado: {ARCHIVO}")
        
        return True
    except Exception as e:
        print(f" Error al inicializar inventario: {e}")
        return False


def leer_inventario():
    try:
        # Verificar que el archivo existe
        if not os.path.exists(ARCHIVO):
            print("[WARNING] Archivo no encontrado. Inicializando...")
            inicializar_inventario()
            return []
        
        # Leer el archivo
        with open(ARCHIVO, 'r', encoding='utf-8') as f:
            contenido = f.read().strip()
            
            # Verificar si el archivo está vacío
            if not contenido:
                print("[WARNING] Archivo vacio. Retornando lista vacia.")
                return []
            
            # Intentar parsear el JSON
            productos = json.loads(contenido)
            
            # Verificar que sea una lista
            if not isinstance(productos, list):
                print("[WARNING] El contenido no es una lista. Reinicializando...")
                inicializar_inventario()
                return []
            
            return productos
            
    except json.JSONDecodeError as e:
        print(f"[ERROR] Error al decodificar JSON: {e}")
        print("[WARNING] Archivo JSON corrupto. Creando respaldo y reinicializando...")
        
        # Crear respaldo del archivo corrupto
        try:
            if os.path.exists(ARCHIVO):
                backup = f"{ARCHIVO}.backup"
                os.rename(ARCHIVO, backup)
                print(f"[OK] Respaldo creado: {backup}")
        except Exception as backup_error:
            print(f" Error al crear respaldo: {backup_error}")
        
        # Reinicializar archivo
        inicializar_inventario()
        return []
        
    except FileNotFoundError:
        print(f" Archivo no encontrado: {ARCHIVO}")
        inicializar_inventario()
        return []
        
    except PermissionError:
        print(f" Sin permisos para leer el archivo: {ARCHIVO}")
        return []
        
    except Exception as e:
        print(f" Error inesperado al leer inventario: {e}")
        return []


def guardar_inventario(productos):
    try:
        # Validar que productos sea una lista
        if not isinstance(productos, list):
            print("[ERROR] Error: Se esperaba una lista de productos")
            return False
        
        # Verificar que el directorio existe
        directorio = os.path.dirname(ARCHIVO)
        if directorio and not os.path.exists(directorio):
            os.makedirs(directorio)
        
        # Guardar en archivo temporal primero (para evitar corrupción)
        archivo_temp = f"{ARCHIVO}.tmp"
        with open(archivo_temp, 'w', encoding='utf-8') as f:
            json.dump(productos, f, indent=4, ensure_ascii=False)
        
        # Reemplazar archivo original con el temporal
        if os.path.exists(ARCHIVO):
            os.remove(ARCHIVO)
        os.rename(archivo_temp, ARCHIVO)
        
        return True
        
    except PermissionError:
        print(f"[ERROR] Sin permisos para escribir en: {ARCHIVO}")
        return False
        
    except Exception as e:
        print(f"[ERROR] Error al guardar inventario: {e}")
        # Limpiar archivo temporal si existe
        archivo_temp = f"{ARCHIVO}.tmp"
        if os.path.exists(archivo_temp):
            try:
                os.remove(archivo_temp)
            except:
                pass
        return False


def generar_id(productos):
    try:
        if not productos or not isinstance(productos, list):
            return 1
        
        # Obtener el ID 
        ids = [p.get('id', 0) for p in productos if isinstance(p, dict) and 'id' in p]
        
        if not ids:
            return 1
        
        return max(ids) + 1
        
    except Exception as e:
        print(f"[ERROR] Error al generar ID: {e}")
        return 1


def validar_estructura_producto(producto):
    if not isinstance(producto, dict):
        return False
    
    campos_requeridos = ['id', 'nombre', 'categoria', 'precio', 'cantidad']
    
    for campo in campos_requeridos:
        if campo not in producto:
            return False
    
    return True