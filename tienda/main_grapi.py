from flask import Flask, render_template, request, redirect, url_for

from tienda import Producto, Tienda, Usuario


app = Flask(__name__)


tienda = Tienda()
tienda.agregar_producto(Producto("EA001", "Laptop", "Laptop básica", 10, 1000000))
tienda.agregar_producto(Producto("WE001", "Manzanas", "Manzanas frescas (Precio por gramo)", 50, 2))
tienda.agregar_producto(Producto("SP001", "Camiseta", "Camiseta promocional", 30, 300000))
tienda.agregar_producto(Producto("SP002", "Auriculares", "Auriculares inalámbricos Bluetooth", 15, 120000))
tienda.agregar_producto(Producto("EA002", "Libro", "Libro de programación en Python", 20, 80000))

usuario = Usuario("Daniela")
tienda.usuarios[usuario.nombre] = usuario

@app.route("/")
def index():
    return render_template("index.html", productos=tienda.productos.values())


@app.route("/carrito")
def ver_carrito():
    return render_template("carrito.html", items=usuario.carrito.items, total=usuario.carrito.calcular_total())


@app.route("/agregar", methods=["POST"])
def agregar_al_carrito():
    sku = request.form["sku"]
    cantidad = int(request.form["cantidad"])
    try:
        tienda.agregar_producto_a_carrito(usuario, sku, cantidad)
        return redirect(url_for("ver_carrito"))
    except Exception as e:
        return render_template("mensaje.html", mensaje=str(e))


@app.route("/borrar/<sku>")
def borrar_item(sku):
    usuario.carrito.borrar_item(sku)
    return redirect(url_for("ver_carrito"))


@app.route("/finalizar")
def finalizar_compra():
    try:
        total = tienda.finalizar_compra(usuario)
        return render_template("mensaje.html", mensaje=f"Compra finalizada. Total pagado: ${total:.2f}")
    except Exception as e:
        return render_template("mensaje.html", mensaje=str(e))


if __name__ == "__main__":
    app.run(debug=True)
