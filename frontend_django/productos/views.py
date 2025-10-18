import requests
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages

API_URL = "http://127.0.0.1:5000/api/productos"


def lista_productos(request):
    # Obtiene y muestra todos los productos del inventario
    
    try:
        response = requests.get(API_URL, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            productos = data.get("productos", [])
            return render(request, "lista.html", {
                "productos": productos,
                "total": len(productos)
            })
        else:
            messages.error(request, "Error al obtener los productos")
            return render(request, "lista.html", {"productos": []})
            
    except requests.exceptions.ConnectionError:
        messages.error(request, "No se pudo conectar con el servidor Flask. Asegúrate de que esté corriendo en http://127.0.0.1:5000")
        return render(request, "lista.html", {"productos": []})
    except requests.exceptions.Timeout:
        messages.error(request, "El servidor tardó demasiado en responder")
        return render(request, "lista.html", {"productos": []})
    except Exception as e:
        messages.error(request, f"Error inesperado: {str(e)}")
        return render(request, "lista.html", {"productos": []})


def detalle_producto(request, id):
    #Muestra los detalles de un producto específico
    
    try:
        response = requests.get(f"{API_URL}/{id}", timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            producto = data.get("producto")
            if producto:
                return render(request, "detalle.html", {"producto": producto})
        elif response.status_code == 404:
            messages.error(request, "Producto no encontrado")
            return redirect(reverse("lista_productos"))
        else:
            messages.error(request, "Error al obtener el producto")
            return redirect(reverse("lista_productos"))
            
    except requests.exceptions.ConnectionError:
        messages.error(request, "No se pudo conectar con el servidor")
        return redirect(reverse("lista_productos"))
    except Exception as e:
        messages.error(request, f"Error inesperado: {str(e)}")
        return redirect(reverse("lista_productos"))


def crear_producto(request):
    #Crea un nuevo producto en el inventario
    
    if request.method == "POST":
        try:
            # Validar campos requeridos
            nombre = request.POST.get("nombre", "").strip()
            categoria = request.POST.get("categoria", "").strip()
            
            if not nombre or not categoria:
                messages.error(request, "El nombre y la categoría son obligatorios")
                return render(request, "formulario.html", {"datos": request.POST})
            
            # Preparar datos
            data = {
                "nombre": nombre,
                "categoria": categoria,
                "descripcion": request.POST.get("descripcion", "").strip(),
                "precio": request.POST.get("precio", 0),
                "cantidad": request.POST.get("cantidad", 0),
                "fecha_vencimiento": request.POST.get("fecha_vencimiento", "").strip()
            }
            
            # Enviar petición a la API
            response = requests.post(API_URL, json=data, timeout=5)
            
            if response.status_code == 201:
                messages.success(request, "Producto creado exitosamente")
                return redirect(reverse("lista_productos"))
            else:
                error_data = response.json()
                error_msg = error_data.get("error", "Error al crear el producto")
                messages.error(request, error_msg)
                return render(request, "formulario.html", {"datos": request.POST})
                
        except requests.exceptions.ConnectionError:
            messages.error(request, "No se pudo conectar con el servidor")
            return render(request, "formulario.html", {"datos": request.POST})
        except Exception as e:
            messages.error(request, f"Error inesperado: {str(e)}")
            return render(request, "formulario.html", {"datos": request.POST})
    
    return render(request, "formulario.html")


def actualizar_producto(request, id):
    # Actualiza un producto existente
    
    if request.method == "POST":
        try:
            # Validar campos requeridos
            nombre = request.POST.get("nombre", "").strip()
            categoria = request.POST.get("categoria", "").strip()
            
            if not nombre or not categoria:
                messages.error(request, "El nombre y la categoría son obligatorios")
                producto = requests.get(f"{API_URL}/{id}").json().get("producto", {})
                return render(request, "formulario.html", {"producto": producto})
            
            # Preparar datos
            data = {
                "nombre": nombre,
                "categoria": categoria,
                "descripcion": request.POST.get("descripcion", "").strip(),
                "precio": request.POST.get("precio", 0),
                "cantidad": request.POST.get("cantidad", 0),
                "fecha_vencimiento": request.POST.get("fecha_vencimiento", "").strip()
            }
            
            # Enviar petición a la API
            response = requests.put(f"{API_URL}/{id}", json=data, timeout=5)
            
            if response.status_code == 200:
                messages.success(request, "Producto actualizado exitosamente")
                return redirect(reverse("lista_productos"))
            elif response.status_code == 404:
                messages.error(request, "Producto no encontrado")
                return redirect(reverse("lista_productos"))
            else:
                error_data = response.json()
                error_msg = error_data.get("error", "Error al actualizar el producto")
                messages.error(request, error_msg)
                producto = requests.get(f"{API_URL}/{id}").json().get("producto", {})
                return render(request, "formulario.html", {"producto": producto})
                
        except requests.exceptions.ConnectionError:
            messages.error(request, "No se pudo conectar con el servidor")
            return redirect(reverse("lista_productos"))
        except Exception as e:
            messages.error(request, f"Error inesperado: {str(e)}")
            return redirect(reverse("lista_productos"))
    
    # GET request - mostrar formulario con datos del producto
    try:
        response = requests.get(f"{API_URL}/{id}", timeout=5)
        if response.status_code == 200:
            data = response.json()
            producto = data.get("producto", {})
            return render(request, "formulario.html", {"producto": producto})
        else:
            messages.error(request, "Producto no encontrado")
            return redirect(reverse("lista_productos"))
    except Exception as e:
        messages.error(request, f"Error al cargar el producto: {str(e)}")
        return redirect(reverse("lista_productos"))


def eliminar_producto(request, id):
    """
    Elimina un producto del inventario
    """
    if request.method == "POST":
        try:
            response = requests.delete(f"{API_URL}/{id}", timeout=5)
            
            if response.status_code == 200:
                messages.success(request, "Producto eliminado exitosamente")
                return redirect(reverse("lista_productos"))
            elif response.status_code == 404:
                messages.error(request, "Producto no encontrado")
                return redirect(reverse("lista_productos"))
            else:
                messages.error(request, "Error al eliminar el producto")
                return redirect(reverse("lista_productos"))
                
        except requests.exceptions.ConnectionError:
            messages.error(request, "No se pudo conectar con el servidor")
            return redirect(reverse("lista_productos"))
        except Exception as e:
            messages.error(request, f"Error inesperado: {str(e)}")
            return redirect(reverse("lista_productos"))
    
    # GET request - mostrar confirmación
    try:
        response = requests.get(f"{API_URL}/{id}", timeout=5)
        if response.status_code == 200:
            data = response.json()
            producto = data.get("producto", {})
            return render(request, "eliminar.html", {"producto": producto})
        else:
            messages.error(request, "Producto no encontrado")
            return redirect(reverse("lista_productos"))
    except Exception as e:
        messages.error(request, f"Error al cargar el producto: {str(e)}")
        return redirect(reverse("lista_productos"))