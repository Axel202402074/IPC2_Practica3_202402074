from flask import Flask, jsonify, request
from flask_cors import CORS
from utils.manejador_json import leer_inventario, guardar_inventario, inicializar_inventario, generar_id
from models.producto import Producto
from datetime import datetime

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        'mensaje': 'API de Gestión de Inventario',
        'version': '1.0',
        'endpoints': {
            'GET /api/productos': 'Obtener todos los productos',
            'POST /api/productos': 'Crear un nuevo producto',
            'PUT /api/productos/<id>': 'Actualizar un producto',
            'DELETE /api/productos/<id>': 'Eliminar un producto'
        }
    }), 200


# Obtener todos los productos
@app.route('/api/productos', methods=['GET'])
def obtener_productos():
    productos = leer_inventario()
    return jsonify({'success': True, 'total': len(productos), 'productos': productos}), 200


# Obtener un producto
@app.route('/api/productos/<int:id>', methods=['GET'])
def obtener_producto(id):
    productos = leer_inventario()
    producto = next((p for p in productos if p['id'] == id), None)
    if not producto:
        return jsonify({'success': False, 'error': 'Producto no encontrado'}), 404
    return jsonify({'success': True, 'producto': producto}), 200


# Crear un producto
@app.route('/api/productos', methods=['POST'])
def crear_producto():
    data = request.get_json()
    productos = leer_inventario()

    if not data or not data.get('nombre') or not data.get('categoria'):
        return jsonify({'success': False, 'error': 'Datos incompletos'}), 400

    nuevo = Producto(
        id=generar_id(productos),
        nombre=data['nombre'],
        categoria=data['categoria'],
        descripcion=data.get('descripcion', ''),
        precio=float(data.get('precio', 0)),
        cantidad=int(data.get('cantidad', 0)),
        fecha_vencimiento=data.get('fecha_vencimiento', ''),
        fecha_creacion=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    )

    productos.append(nuevo.to_dict())
    guardar_inventario(productos)
    return jsonify({'success': True, 'mensaje': 'Producto agregado', 'producto': nuevo.to_dict()}), 201


# Actualizar un producto
@app.route('/api/productos/<int:id>', methods=['PUT'])
def actualizar_producto(id):
    productos = leer_inventario()
    producto = next((p for p in productos if p['id'] == id), None)

    if not producto:
        return jsonify({'success': False, 'error': 'Producto no encontrado'}), 404

    data = request.get_json()
    producto.update({
        'nombre': data.get('nombre', producto['nombre']),
        'categoria': data.get('categoria', producto['categoria']),
        'descripcion': data.get('descripcion', producto['descripcion']),
        'precio': float(data.get('precio', producto['precio'])),
        'cantidad': int(data.get('cantidad', producto['cantidad'])),
        'fecha_vencimiento': data.get('fecha_vencimiento', producto['fecha_vencimiento']),
        'fecha_modificacion': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    })

    guardar_inventario(productos)
    return jsonify({'success': True, 'mensaje': 'Producto actualizado', 'producto': producto}), 200


# Eliminar un producto
@app.route('/api/productos/<int:id>', methods=['DELETE'])
def eliminar_producto(id):
    productos = leer_inventario()
    producto = next((p for p in productos if p['id'] == id), None)
    if not producto:
        return jsonify({'success': False, 'error': 'Producto no encontrado'}), 404

    productos = [p for p in productos if p['id'] != id]
    guardar_inventario(productos)
    return jsonify({'success': True, 'mensaje': 'Producto eliminado correctamente'}), 200


if __name__ == '__main__':
    inicializar_inventario()
    app.run(debug=True, port=5000)
