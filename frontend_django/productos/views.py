import requests
from django.shortcuts import render, redirect
from django.urls import reverse

API_URL = "http://127.0.0.1:5000/api/productos"  # 👈 Flask debe estar corriendo

def lista_productos(request):
    response = requests.get(API_URL)
    data = response.json() if response.status_code == 200 else {}
    productos = data.get("productos", [])
    return render(request, "lista.html", {"productos": productos})


def detalle_producto(request, id):
    response = requests.get(f"{API_URL}/{id}")
    data = response.json()
    producto = data.get("producto") if data.get("success") else None
    return render(request, "detalle.html", {"producto": producto})


def crear_producto(request):
    if request.method == "POST":
        data = {
            "nombre": request.POST["nombre"],
            "categoria": request.POST["categoria"],
            "descripcion": request.POST.get("descripcion", ""),
            "precio": request.POST["precio"],
            "cantidad": request.POST["cantidad"],
            "fecha_vencimiento": request.POST.get("fecha_vencimiento", "")
        }
        requests.post(API_URL, json=data)
        return redirect(reverse("lista_productos"))
    return render(request, "formulario.html")


def actualizar_producto(request, id):
    if request.method == "POST":
        data = {
            "nombre": request.POST["nombre"],
            "categoria": request.POST["categoria"],
            "descripcion": request.POST.get("descripcion", ""),
            "precio": request.POST["precio"],
            "cantidad": request.POST["cantidad"],
            "fecha_vencimiento": request.POST.get("fecha_vencimiento", "")
        }
        requests.put(f"{API_URL}/{id}", json=data)
        return redirect(reverse("lista_productos"))
    producto = requests.get(f"{API_URL}/{id}").json().get("producto", {})
    return render(request, "formulario.html", {"producto": producto})


def eliminar_producto(request, id):
    if request.method == "POST":
        requests.delete(f"{API_URL}/{id}")
        return redirect(reverse("lista_productos"))
    producto = requests.get(f"{API_URL}/{id}").json().get("producto", {})
    return render(request, "eliminar.html", {"producto": producto})
