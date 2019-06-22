from django.db import models

class Categoria(models.Model):
    nombre=models.CharField(max_length=25)
    
    def __str__(self):
        return self.nombre

class Inventario(models.Model):
    precio_promedio_compra=models.DecimalField(max_digits=8,decimal_places=2)

    def __str__(self):
        return str(self.precio_promedio_compra)

class Cliente(models.Model):
    nombre=models.CharField(max_length=25)
    apellido=models.CharField(max_length=25)

    def __str__(self):
        return self.nombre+" "+self.apellido

class Proveedor(models.Model):
    razon_social=models.CharField(max_length=256)

    def __str__(self):
        return self.razon_social

class Compra(models.Model):
    idProveedor=models.ForeignKey(Proveedor,on_delete=models.CASCADE,db_column='idProveedor')
    fecha_hora=models.DateTimeField()

    def __str__(self):
        return self.fecha_hora

class Producto(models.Model):
    idCategoria=models.ForeignKey(Categoria,on_delete=models.CASCADE,db_column='idCategoria')
    idInventario=models.ForeignKey(Inventario,on_delete=models.CASCADE,db_column='idInventario')
    codigo=models.CharField(max_length=10)
    nombre=models.CharField(max_length=25)


    def __str__(self):
        return self.codigo

class DetalleCompra(models.Model):
    idCompra=models.ForeignKey(Compra,on_delete=models.CASCADE,db_column='idCompra')
    idProducto=models.ForeignKey(Producto,on_delete=models.CASCADE,db_column='idProducto')

    def __str__(self):
        return "detalle compra: compra: "+str(self.idCompra)+" - producto: "+str(self.idProducto)

class Kardex(models.Model):
    idProducto=models.ForeignKey(Producto,on_delete=models.CASCADE,db_column='idProducto')
    fecha=models.DateField()
    precExistencia=models.DecimalField(max_digits=8,decimal_places=2)
    cantExistencia=models.IntegerField()

    def __str__(self):
        return str(self.fecha)+" "+str(self.idProducto)

class ProductoRetorno(models.Model):
    idCliente=models.ForeignKey(Cliente,on_delete=models.CASCADE,db_column='idCliente')
    idProducto=models.ForeignKey(Producto,on_delete=models.CASCADE,db_column='idProducto')
    idProveedor = models.ForeignKey(Proveedor,on_delete=models.CASCADE,db_column='idProveedor',null=True) #Quitar el null después
    cantidad=models.IntegerField()
    nombre_cliente=models.CharField(max_length=20)
    nombre_producto=models.CharField(max_length=40)
    codigo=models.CharField(max_length=10)
    fecha=models.DateField()

    def __str__(self):
        return self.codigo

class ProductoConsigna(models.Model):
    idCliente=models.ForeignKey(Cliente,on_delete=models.CASCADE,db_column='idCliente')
    idProducto=models.ForeignKey(Producto,on_delete=models.CASCADE,db_column='idProducto')
    cantidad=models.IntegerField()
    fechaInicio=models.DateField()
    fechaFin=models.DateField()

    def __str__(self):
        return "consigna: idcliente: "+str(self.idCliente)+" idproducto: "+str(self.idProducto)

class ProductoPotencial(models.Model):
    idCliente=models.ForeignKey(Cliente,on_delete=models.CASCADE,db_column='idCliente')
    nombre=models.CharField(max_length=25)
    fecha=models.DateField(null=True)
    cantidad=models.IntegerField()

    def __str__(self):
        return self.nombre

class Venta(models.Model):
    idCliente=models.ForeignKey(Cliente,on_delete=models.CASCADE,db_column='idCliente',null=True)
    fecha_hora=models.DateTimeField()

    def __str__(self):
        return str(self.fecha_hora)+" - "+str(self.idCliente)

class DetalleVenta(models.Model):
    idVenta=models.ForeignKey(Venta,on_delete=models.CASCADE,db_column='idVenta',null=True)
    idProducto=models.ForeignKey(Producto,on_delete=models.CASCADE,db_column='idProducto')
    cantidad=models.IntegerField()
    precio_unitario=models.DecimalField(max_digits=8,decimal_places=2)
    descuento=models.DecimalField(max_digits=8,decimal_places=2)
    total=models.DecimalField(max_digits=20,decimal_places=2) 
    
    def __str__(self):
        return str(self.idVenta)+" - "+str(self.idProducto)

class ProductoPotencialHistorico(models.Model):
    idCliente=models.IntegerField(db_column='idCliente')
    nombre=models.CharField(max_length=25)
    fecha=models.DateField(null=True)
    cantidad=models.IntegerField()

class ProductoConsignaHistorico(models.Model):
    idCliente=models.IntegerField(db_column='idCliente')
    idProducto=models.IntegerField(db_column='idProducto')
    cantidad=models.IntegerField()
    fechaInicio=models.DateField()
    fechaFin=models.DateField()

class ProductoRetornoHistorico(models.Model):
    idCliente=models.IntegerField(db_column='idCliente')
    idProducto=models.IntegerField(db_column='idProducto')
    idProveedor = models.IntegerField(db_column='idProveedor') 
    cantidad=models.IntegerField()
    nombre_cliente=models.CharField(max_length=20)
    nombre_producto=models.CharField(max_length=40)
    codigo=models.CharField(max_length=10)
    fecha=models.DateField()


class PermisosSoporte(models.Model):
    class Meta:
        managed=False
        permissions = ( 
            ('resumen_productos_ganancias', 'Presidente Estrategico'),
            ('resumen_productos_potenciales', 'Presidente Estrategico'),  
            ('resumen_ganancias_clientes', 'Presidente Estrategico'),
            ('resumen_productos_vendidos', 'Presidente Estrategico'),
            ('resumen_tardanzas_productos', 'Presidente Estrategico'),
            ('semi_productos_vendidos', 'Director Tactico'),  
            ('semi_productos_ganancias', 'Director Tactico'), 
            ('semi_retornos_equipos', 'Director Tactico'),
            ('semi_productos_consigna', 'Director Tactico'),
            ('semi_ganancias_clientes', 'Director Tactico'),
            ('semi_clientes_frecuentes', 'Director Tactico'),
            ('etl','Administrador'),
            ('gestion_usuarios','Administrador'),
            ('actualizar_admin','Delegado')
        )

