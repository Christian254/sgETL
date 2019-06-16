#tablas de catalogo
extraer_categoria = ('''
    SELECT nombre from inventario_categoria
''')

extraer_proveedor = ('''
    SELECT razon_social from inventario_proveedor
''')

extraer_inventario = ('''
    SELECT precio_promedio_compra from inventario_inventario
''')

#tablas dependientes
extraer_cliente = ('''
    SELECT nombre, apellido from "SIGPAd_cliente"
''')

extraer_compra = ('''
    SELECT proveedor_id, fecha_hora from inventario_compra
''')

extraer_producto = ('''
    SELECT categoria_id, inventario_id, codigo, nombre from
    inventario_producto
''')

extraer_kardex = ('''
    SELECT producto_id, fecha, "precExistencia", "cantExistencia" from
    inventario_kardex
''')

extraer_detallecompra = ('''
    SELECT producto_id, compra_id from inventario_detallecompra
''')

extraer_venta = ('''
    SELECT cliente_id, fecha_hora from inventario_venta
''')

extraer_detalleventa = ('''
    SELECT producto_id, venta_id, cantidad, precio_unitario, descuento, total
    from inventario_detalleventa
''')

lista_extraccion=[extraer_categoria,extraer_proveedor,extraer_inventario,extraer_cliente,extraer_compra
,extraer_producto,extraer_kardex,extraer_detallecompra,extraer_venta,extraer_detalleventa
]    


