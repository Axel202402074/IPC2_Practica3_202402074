class Producto:
    def __init__(self, id, nombre, categoria, descripcion, precio, cantidad, fecha_vencimiento="", fecha_creacion=""):
        self.id = id
        self.nombre = nombre
        self.categoria = categoria
        self.descripcion = descripcion
        self.precio = precio
        self.cantidad = cantidad
        self.fecha_vencimiento = fecha_vencimiento
        self.fecha_creacion = fecha_creacion

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "categoria": self.categoria,
            "descripcion": self.descripcion,
            "precio": self.precio,
            "cantidad": self.cantidad,
            "fecha_vencimiento": self.fecha_vencimiento,
            "fecha_creacion": self.fecha_creacion
        }
