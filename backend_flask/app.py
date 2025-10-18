from flask import Flask, jsonify, request
from flask_cors import CORS
from utils.manejador_json import leer_inventario, guardar_inventario, inicializar_inventario, generar_id
from models.producto import Producto
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Manejo de errores globales
@app.errorhandler(404)
def not_found(error):
    return jsonify({'success': False, 'error': 'Endpoint no encontrado'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'success': False, 'error': 'Error interno del servidor'}), 500

@app.errorhandler(400)
def bad_request(error):
    return jsonify({'success': False, 'error': 'Solicitud incorrecta'}), 400


@app.route('/', methods=['GET'])
def home():
    return jsonify({
        'mensaje': 'API de Gestión de Inventario',
        'version': '1.0',
        'endpoints': {
            'GET /api/productos': 'Obtener todos los productos',
            'GET /api/productos/<id>': 'Obtener un producto específico',
            'POST /api/productos': 'Crear un nuevo producto',
            'PUT /api/productos/<id>': 'Actualizar un producto',
            'DELETE /api/productos/<id>': 'Eliminar un producto'
        }
    }), 200


# Obtener todos los productos
@app.route('/api/productos', methods=['GET'])
def obtener_productos():
    try:
        productos = leer_inventario()
        return jsonify({
            'success': True, 
            'total': len(productos), 
            'productos': productos
        }), 200
    except Exception as e:
        return jsonify({
            'success': False, 
            'error': f'Error al obtener productos: {str(e)}'
        }), 500


# Obtener un producto específico
@app.route('/api/productos/<int:id>', methods=['GET'])
def obtener_producto(id):
    try:
        productos = leer_inventario()
        producto = next((p for p in productos if p['id'] == id), None)
        
        if not producto:
            return jsonify({
                'success': False, 
                'error': 'Producto no encontrado'
            }), 404
        
        return jsonify({
            'success': True, 
            'producto': producto
        }), 200
    except Exception as e:
        return jsonify({
            'success': False, 
            'error': f'Error al obtener el producto: {str(e)}'
        }), 500


# Crear un producto
@app.route('/api/productos', methods=['POST'])
def crear_producto():
    try:
        data = request.get_json()
        
        # Validar que se recibieron datos
        if not data:
            return jsonify({
                'success': False, 
                'error': 'No se recibieron datos'
            }), 400
        
        # Validar nombre (obligatorio)
        if not data.get('nombre') or not data.get('nombre').strip():
            return jsonify({
                'success': False, 
                'error': 'El nombre es obligatorio'
            }), 400
        
        # Validar categoría (obligatoria)
        if not data.get('categoria') or not data.get('categoria').strip():
            return jsonify({
                'success': False, 
                'error': 'La categoría es obligatoria'
            }), 400
        
        # Validar precio
        try:
            precio = float(data.get('precio', 0))
            if precio < 0:
                return jsonify({
                    'success': False, 
                    'error': 'El precio no puede ser negativo'
                }), 400
        except (ValueError, TypeError):
            return jsonify({
                'success': False, 
                'error': 'El precio debe ser un número válido'
            }), 400
        
        # Validar cantidad
        try:
            cantidad = int(data.get('cantidad', 0))
            if cantidad < 0:
                return jsonify({
                    'success': False, 
                    'error': 'La cantidad no puede ser negativa'
                }), 400
        except (ValueError, TypeError):
            return jsonify({
                'success': False, 
                'error': 'La cantidad debe ser un número entero válido'
            }), 400
        
        # Leer inventario actual
        productos = leer_inventario()
        
        # Crear nuevo producto
        nuevo = Producto(
            id=generar_id(productos),
            nombre=data['nombre'].strip(),
            categoria=data['categoria'].strip(),
            descripcion=data.get('descripcion', '').strip(),
            precio=precio,
            cantidad=cantidad,
            fecha_vencimiento=data.get('fecha_vencimiento', '').strip(),
            fecha_creacion=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        )
        
        productos.append(nuevo.to_dict())
        guardar_inventario(productos)
        
        return jsonify({
            'success': True, 
            'mensaje': 'Producto creado exitosamente', 
            'producto': nuevo.to_dict()
        }), 201
        
    except Exception as e:
        return jsonify({
            'success': False, 
            'error': f'Error al crear el producto: {str(e)}'
        }), 500


# Actualizar un producto
@app.route('/api/productos/<int:id>', methods=['PUT'])
def actualizar_producto(id):
    try:
        data = request.get_json()
        
        # Validar que se recibieron datos
        if not data:
            return jsonify({
                'success': False, 
                'error': 'No se recibieron datos para actualizar'
            }), 400
        
        productos = leer_inventario()
        producto = next((p for p in productos if p['id'] == id), None)
        
        if not producto:
            return jsonify({
                'success': False, 
                'error': 'Producto no encontrado'
            }), 404
        
        # Validar nombre si se proporciona
        if 'nombre' in data:
            if not data['nombre'] or not data['nombre'].strip():
                return jsonify({
                    'success': False, 
                    'error': 'El nombre no puede estar vacío'
                }), 400
            producto['nombre'] = data['nombre'].strip()
        
        # Validar categoría si se proporciona
        if 'categoria' in data:
            if not data['categoria'] or not data['categoria'].strip():
                return jsonify({
                    'success': False, 
                    'error': 'La categoría no puede estar vacía'
                }), 400
            producto['categoria'] = data['categoria'].strip()
        
        # Validar precio si se proporciona
        if 'precio' in data:
            try:
                precio = float(data['precio'])
                if precio < 0:
                    return jsonify({
                        'success': False, 
                        'error': 'El precio no puede ser negativo'
                    }), 400
                producto['precio'] = precio
            except (ValueError, TypeError):
                return jsonify({
                    'success': False, 
                    'error': 'El precio debe ser un número válido'
                }), 400
        
        # Validar cantidad si se proporciona
        if 'cantidad' in data:
            try:
                cantidad = int(data['cantidad'])
                if cantidad < 0:
                    return jsonify({
                        'success': False, 
                        'error': 'La cantidad no puede ser negativa'
                    }), 400
                producto['cantidad'] = cantidad
            except (ValueError, TypeError):
                return jsonify({
                    'success': False, 
                    'error': 'La cantidad debe ser un número entero válido'
                }), 400
        
        # Actualizar descripción y fecha de vencimiento si se proporcionan
        if 'descripcion' in data:
            producto['descripcion'] = data['descripcion'].strip()
        
        if 'fecha_vencimiento' in data:
            producto['fecha_vencimiento'] = data['fecha_vencimiento'].strip()
        
        # Agregar fecha de modificación
        producto['fecha_modificacion'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        guardar_inventario(productos)
        
        return jsonify({
            'success': True, 
            'mensaje': 'Producto actualizado exitosamente', 
            'producto': producto
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False, 
            'error': f'Error al actualizar el producto: {str(e)}'
        }), 500


# Eliminar un producto
@app.route('/api/productos/<int:id>', methods=['DELETE'])
def eliminar_producto(id):
    try:
        productos = leer_inventario()
        producto = next((p for p in productos if p['id'] == id), None)
        
        if not producto:
            return jsonify({
                'success': False, 
                'error': 'Producto no encontrado'
            }), 404
        
        productos = [p for p in productos if p['id'] != id]
        guardar_inventario(productos)
        
        return jsonify({
            'success': True, 
            'mensaje': 'Producto eliminado exitosamente'
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False, 
            'error': f'Error al eliminar el producto: {str(e)}'
        }), 500


if __name__ == '__main__':
    try:
        inicializar_inventario()
        print("[OK] Inventario inicializado correctamente")
        print("[OK] Servidor Flask corriendo en http://localhost:5000")
        app.run(debug=True, port=5000)
    except Exception as e:
        print(f"[ERROR] Error al iniciar el servidor: {e}")