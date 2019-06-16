#tablas de catalogo
carga_categoria = ('''
  INSERT INTO gerencial_categoria(nombre) values ( %s )
''')

carga_proveedor = ('''
  INSERT INTO gerencial_proveedor(razon_social) values ( %s )
''')

carga_inventario = ('''
  INSERT INTO gerencial_inventario(precio_promedio_compra) values ( %s )
''')

#tablas dependientes
carga_cliente = ('''
  INSERT INTO gerencial_cliente(nombre,apellido) values ( %s , %s )
''')

carga_compra = ('''
  INSERT INTO gerencial_compra("idProveedor",fecha_hora) values ( %s , %s )
''')

carga_producto = ('''
  INSERT INTO gerencial_producto("idCategoria", "idInventario", codigo, nombre) 
  values ( %s , %s , %s , %s )
''')

carga_kardex = ('''
  INSERT INTO gerencial_kardex("idProducto", fecha, "precExistencia", "cantExistencia") 
  values ( %s ,  %s , %s , %s )
''')

carga_detallecompra = ('''
  INSERT INTO gerencial_detallecompra("idProducto", "idCompra") values ( %s , %s )
''')

carga_venta = ('''
  INSERT INTO gerencial_venta("idCliente", fecha_hora) values ( %s , %s )
''')

carga_detalleventa = ('''
  INSERT INTO gerencial_detalleventa("idProducto", "idVenta", cantidad, precio_unitario, descuento, total) 
  values ( %s , %s , %s,  %s , %s , %s )
''')


lista_carga=[carga_categoria,carga_proveedor,carga_inventario,carga_cliente,carga_compra
,carga_producto,carga_kardex,carga_detallecompra,carga_venta,carga_detalleventa
]    

lista_tablas_gerencial=["gerencial_categoria","gerencial_proveedor","gerencial_inventario","gerencial_cliente",
"gerencial_compra","gerencial_producto","gerencial_kardex","gerencial_detallecompra","gerencial_venta",
"gerencial_detalleventa"]