#tablas de catalogo
carga_categoria = ('''
  INSERT INTO gerencial_categoria(id,nombre) values ( %s ,%s )
''')

carga_proveedor = ('''
  INSERT INTO gerencial_proveedor(id,razon_social) values (%s, %s )
''')

carga_inventario = ('''
  INSERT INTO gerencial_inventario(id,precio_promedio_compra) values (%s, %s )
''')

#tablas dependientes
carga_cliente = ('''
  INSERT INTO gerencial_cliente(id, nombre,apellido) values (%s, %s , %s )
''')

carga_compra = ('''
  INSERT INTO gerencial_compra(id,"idProveedor",fecha_hora) values (%s, %s , %s )
''')

carga_producto = ('''
  INSERT INTO gerencial_producto(id,"idCategoria", "idInventario", codigo, nombre) 
  values ( %s ,%s , %s , %s , %s )
''')

carga_kardex = ('''
  INSERT INTO gerencial_kardex(id, "idProducto", fecha, "precExistencia", "cantExistencia") 
  values (%s, %s ,  %s , %s , %s )
''')

carga_detallecompra = ('''
  INSERT INTO gerencial_detallecompra(id,"idProducto", "idCompra") values ( %s ,%s , %s )
''')

carga_venta = ('''
  INSERT INTO gerencial_venta(id,"idCliente", fecha_hora) values (%s, %s , %s )
''')

carga_detalleventa = ('''
  INSERT INTO gerencial_detalleventa(id,"idProducto", "idVenta", cantidad, precio_unitario, descuento, total) 
  values ( %s , %s , %s,  %s , %s , %s, %s )
''')


lista_carga=[carga_categoria,carga_proveedor,carga_inventario,carga_cliente,carga_compra
,carga_producto,carga_kardex,carga_detallecompra,carga_venta,carga_detalleventa
]    

lista_tablas_gerencial=["gerencial_categoria","gerencial_proveedor","gerencial_inventario","gerencial_cliente",
"gerencial_compra","gerencial_producto","gerencial_kardex","gerencial_detallecompra","gerencial_venta",
"gerencial_detalleventa"]