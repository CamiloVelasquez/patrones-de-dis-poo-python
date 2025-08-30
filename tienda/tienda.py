# modelos.py

from abc import abstractmethod

#implementación de la interfaz ReglaPrecio con sus metodos abstractos
#metodo 1: es aplicable
#metodo 2: calcular total
class ReglaPrecio():
  @abstractmethod
  def es_aplicable(self, sku: str) -> bool:
    pass
  @abstractmethod
  def calcular_total(self, cantidad: int, precio: float) -> float:
    pass

#Regla para productos normales (SKU empieza por 'EA')
#Metodos customizados para cada regla (EA = regla normal -> cantidad x precio unitario)
class ReglaPrecioNormal(ReglaPrecio):
  def es_aplicable(self, sku: str) -> bool:
    return sku.startswith("EA")
  def calcular_total(self, cantidad: int, precio: float) -> float:
    return cantidad * precio

#Regla para productos por peso (SKU empieza por 'WE')
#Metodos customizados para cada regla (WE = regla por peso -> cantidad * 1000 * precio)
class ReglaPrecioPorPeso(ReglaPrecio):
  def es_aplicable(self, sku: str) -> bool:
    return sku.startswith("WE")
  def calcular_total(self, cantidad: int, precio: float) -> float:
    # Se retorna el valor por kilogramo (suponiendo que  la cantidad y el precio están en gramos)
    return (cantidad* 1000 * precio )

#Regla para productos normaEspeciales (SKU empieza por 'SP')
#Metodos customizados para cada regla (SP = regla especial -> cantidad x precio unitario con descuento según cantidad)
class ReglaPrecioEspecial(ReglaPrecio):
  def es_aplicable(self, sku: str) -> bool:
    return sku.startswith("SP")
  def calcular_total(self, cantidad: int, precio: float) -> float:
    # Descuento del 20% por cada 3 unidades, con un máximo del 50%.
    descuento_por_bloque = 0.20
    unidades_por_bloque = 3
    num_bloques = cantidad // unidades_por_bloque
    descuento_total = min(num_bloques * descuento_por_bloque, 0.50)
    precio_base = cantidad * precio
    monto_descuento = precio_base * descuento_total
    return precio_base - monto_descuento

#manejador de reglas, encargado de aplicar la regla de precio correcta para un producto.
class ManejadorReglas:
  def __init__(self):
    self._reglas = [ReglaPrecioNormal(), ReglaPrecioPorPeso(), ReglaPrecioEspecial()]
  def obtener_regla(self, sku: str) -> ReglaPrecio:
    for regla in self._reglas:
      if regla.es_aplicable(sku):
        return regla
    raise ValueError(f"No se encontró una regla de precio aplicable para el SKU: {sku}")

#implementación de la clase producto con sus atributos y métodos, representa un producto en tienda
#metodo 1: se consulta si tiene unidades
#metodo 2: descontar unidades en caso de que tenga suficientes
class Producto:
  def __init__(self, sku: str, nombre: str, descripcion: str, unidades_disponibles: int, precio_unitario: float):
    self.sku = sku
    self.nombre = nombre
    self.descripcion = descripcion
    self.unidades_disponibles = unidades_disponibles
    self.precio_unitario = precio_unitario
  def tiene_unidades(self, cantidad: int) -> bool:
    return self.unidades_disponibles >= cantidad
  def descontar_unidades(self, cantidad: int):
    if self.tiene_unidades(cantidad):
      self.unidades_disponibles -= cantidad
    else:
      raise ValueError("No hay suficientes unidades disponibles.")

#implementación de la clase item en el carrito de compras
#metodo 1: calcular total basado en la regla
class Item:
  _manejador_reglas = ManejadorReglas()
  def __init__(self, producto: Producto, cantidad: int):
    self.producto = producto
    self.cantidad = cantidad
    self.regla_precio = self._manejador_reglas.obtener_regla(producto.sku)
  def calcular_total(self) -> float:
    return self.regla_precio.calcular_total(self.cantidad, self.producto.precio_unitario)

#implementación de la clase Carrito que representa el carrito de compras de un usuario
#metodo 1: agregar item validando las unidades disponibles
#metodo 2: borrar item del carrito validando que si esté en el carrito
#metodo 3: Calcular el total del carrito aplicando las reglas de precio que apliquen
class Carrito:
  def __init__(self):
    self.items = []
  def agregar_item(self, producto: Producto, cantidad: int):
    if not producto.tiene_unidades(cantidad):
      raise ValueError(f"No hay suficientes unidades de '{producto.nombre}'. Disponibles: {producto.unidades_disponibles}")
    # Validar si el producto ya está en el carrito, actualiza la cantidad
    for item in self.items:
      if item.producto.sku == producto.sku:
        item.cantidad += cantidad
        return (f"El producto ya estaba en el carrito, se actualizó la cantidad a {item.cantidad} unidades.")    
    # Si no está , agrega un nuevo item
    nuevo_item = Item(producto, cantidad)
    self.items.append(nuevo_item)

  def borrar_item(self, sku: str):
    self.items = [item for item in self.items if item.producto.sku != sku]

  def calcular_total(self) -> float:
    return sum(item.calcular_total() for item in self.items)

#implementación de la clase Usuario
#metodo 1: agregar item a carrito validando la existencia del producto
#metodo 2: borrar item del carrito
class Usuario:
  def __init__(self, nombre: str):
    self.nombre = nombre
    self.carrito = Carrito()
  def agregar_item_a_carrito(self, producto: Producto, cantidad: int):
    self.carrito.agregar_item(producto, cantidad)
  def borrar_item_de_carrito(self, sku: str):
    self.carrito.borrar_item(sku)

#implementación de la clase Tienda que gestiona la tienda
#metodo 1: agregar producto
#metodo 2: registrar usuario
#metodo 3: agregar producto a carrito
#metodo 4: eliminar item de carrito
#metodo 5: finalizar compra
class Tienda:
    def __init__(self):
        self.productos = {}
        self.usuarios = {}
        self.total_ventas = 0.0
    #se implementa el método agregar_producto a la tienda para administrar los productos
    def agregar_producto(self, producto: Producto):
        self.productos[producto.sku] = producto  
    #se implementa el método obtener_productoo para validar la existencia del producto en la tienda
    def obtener_producto(self, sku: str) -> Producto:
        if sku not in self.productos:
            raise KeyError(f"Producto con SKU '{sku}' no encontrado.")
        return self.productos[sku]
    def agregar_producto_a_carrito(self, usuario: Usuario, sku_producto: str, cantidad: int):
        producto = self.obtener_producto(sku_producto)
        usuario.agregar_item_a_carrito(producto, cantidad)
        # se hace el calculo de los totales para mostrarlos en la consola
        item_recien_agregado = next(item for item in usuario.carrito.items if item.producto.sku == sku_producto)
        total_item = item_recien_agregado.calcular_total()
        total_carrito = usuario.carrito.calcular_total()
        return total_item, total_carrito
    def finalizar_compra(self, usuario: Usuario):
        total_compra = usuario.carrito.calcular_total()
        # descontamos las unidades de cada producto para tener el inventario actualizado
        for item in usuario.carrito.items:
            producto = self.obtener_producto(item.producto.sku)
            producto.descontar_unidades(item.cantidad)           
        # también se acumulan las ventas totales de la tienda
        self.total_ventas += total_compra  
        usuario.carrito.items = []
        return total_compra