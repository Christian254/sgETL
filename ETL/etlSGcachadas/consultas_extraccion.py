#tablas de catalogo
extraer_categoria = ('''
    SELECT id,nombre from inventario_categoria
''')

extraer_proveedor = ('''
    SELECT id,razon_social from inventario_proveedor
''')

extraer_inventario = ('''
    SELECT id, precio_promedio_compra from inventario_inventario
''')

#tablas dependientes
extraer_cliente = ('''
    SELECT id, nombre, apellido from "SIGPAd_cliente"
''')

extraer_compra = ('''
    SELECT id, proveedor_id, fecha_hora from inventario_compra
''')

extraer_producto = ('''
    SELECT id, categoria_id, inventario_id, codigo, nombre from
    inventario_producto
''')

extraer_kardex = ('''
    SELECT id, producto_id, fecha, "precExistencia", "cantExistencia" from
    inventario_kardex
''')

extraer_detallecompra = ('''
    SELECT id, producto_id, compra_id from inventario_detallecompra
''')

extraer_venta = ('''
    SELECT id, cliente_id, fecha_hora from inventario_venta
''')

extraer_detalleventa = ('''
    SELECT id, producto_id, venta_id, cantidad, precio_unitario, descuento, total
    from inventario_detalleventa
''')

lista_extraccion=[extraer_categoria,extraer_proveedor,extraer_inventario,extraer_cliente,extraer_compra
,extraer_producto,extraer_kardex,extraer_detallecompra,extraer_venta,extraer_detalleventa
]    

lista_tablas_transaccional=["inventario_categoria","inventario_proveedor","inventario_inventario",'"SIGPAd_cliente"',
"inventario_compra","inventario_producto","inventario_kardex","inventario_detallecompra","inventario_venta",
"inventario_detalleventa"]

