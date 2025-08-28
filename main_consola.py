# main_consola.py

from Trabajo.tienda import Tienda, Producto, Usuario

def mostrar_menu():
    """Imprime el menú principal de opciones en la consola."""
    print("\n" + "="*10 + " MENÚ DE LA TIENDA " + "="*10)
    print("1. Ver productos disponibles")
    print("2. Agregar producto al carrito")
    print("3. Ver carrito de compras")
    print("4. Eliminar ítem del carrito")
    print("5. Finalizar compra")
    print("6. Salir")
    print("="*39)

def ver_productos(tienda: Tienda):
    """Muestra todos los productos de la tienda."""
    print("\n--- Productos Disponibles ---")
    for sku, prod in tienda.productos.items():
        tipo = "Normal"
        if sku.startswith("WE"): tipo = "Por Peso (precio/gr)"
        if sku.startswith("SP"): tipo = "Especial"
        
        print(f"[{sku}] {prod.nombre:<20} | ${prod.precio_unitario:9,.2f} | Stock: {prod.unidades_disponibles:<5} | Tipo: {tipo}")
    print("-" * 29)

def agregar_a_carrito(tienda: Tienda, usuario: Usuario):
    """Solicita al usuario un SKU y cantidad para agregar al carrito."""
    try:
        sku = input("Ingrese el SKU del producto a agregar: ").upper()
        cantidad_str = input(f"Ingrese la cantidad (para productos por peso, son gramos): ")
        cantidad = int(cantidad_str)

        if cantidad <= 0:
            print("❌ Error: La cantidad debe ser un número positivo.")
            return

        tienda.agregar_producto_a_carrito(usuario, sku, cantidad)
        print(f"✅ ¡Producto '{sku}' agregado al carrito exitosamente!")

    except KeyError as e:
        print(f"❌ Error: {e}")
    except ValueError as e:
        print(f"❌ Error: {e}")
    except Exception:
        print("❌ Error: La cantidad debe ser un número entero.")


def ver_carrito(usuario: Usuario):
    """Muestra el contenido actual del carrito de compras."""
    print("\n--- Carrito de Compras ---")
    if not usuario.carrito.items:
        print("El carrito está vacío.")
    else:
        for item in usuario.carrito.items:
            print(f"- SKU: {item.producto.sku:<7} | Producto: {item.producto.nombre:<20} | Cant: {item.cantidad:<5} | Subtotal: ${item.calcular_total():>12,.2f}")
        print("-" * 30)
        print(f"TOTAL DEL CARRITO: ${usuario.carrito.calcular_total():>19,.2f}")
    print("-" * 26)

def eliminar_de_carrito(usuario: Usuario):
    """Solicita el SKU de un producto para eliminarlo del carrito."""
    if not usuario.carrito.items:
        print("❌ El carrito ya está vacío.")
        return
    try:
        sku = input("Ingrese el SKU del producto a eliminar: ").upper()
        usuario.borrar_item_de_carrito(sku)
        print(f"✅ Producto '{sku}' eliminado del carrito.")
    except ValueError as e:
        print(f"❌ Error: {e}")

def finalizar_compra(tienda: Tienda, usuario: Usuario):
    """Procesa la compra, actualiza el stock y las ventas totales."""
    try:
        total_pagado = tienda.finalizar_compra(usuario)
        print("\n" + "*"*30)
        print("🎉 ¡Compra finalizada con éxito! 🎉")
        print(f"Total pagado: ${total_pagado:,.2f}")
        print("Gracias por su compra.")
        print("*"*30)
    except ValueError as e:
        print(f"❌ Error al finalizar la compra: {e}")


def main():
    """Función principal que ejecuta el bucle de la aplicación."""
    # 1. Configuración inicial
    tienda = Tienda()
    tienda.agregar_producto(Producto("EA001", "Teclado Mecánico", "Teclado RGB", 10, 150000.0))
    tienda.agregar_producto(Producto("EA002", "Mouse Gamer", "Mouse con 6 botones", 20, 80000.0))
    tienda.agregar_producto(Producto("WE001", "Manzanas", "Manzana Royal Gala por gramo", 5000, 5.0))
    tienda.agregar_producto(Producto("SP001", "Gaseosa 1.5L", "Pack de gaseosas", 30, 4000.0))

    usuario = Usuario("Cliente Consola")

    print(f"¡Bienvenido a la Tienda, {usuario.nombre}!")

    # 2. Bucle principal de la aplicación
    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ")

        if opcion == '1':
            ver_productos(tienda)
        elif opcion == '2':
            agregar_a_carrito(tienda, usuario)
        elif opcion == '3':
            ver_carrito(usuario)
        elif opcion == '4':
            eliminar_de_carrito(usuario)
        elif opcion == '5':
            finalizar_compra(tienda, usuario)
        elif opcion == '6':
            print("Saliendo de la aplicación. ¡Hasta pronto!")
            break
        else:
            print("Opción no válida. Por favor, intente de nuevo.")

if __name__ == "__main__":
    main()