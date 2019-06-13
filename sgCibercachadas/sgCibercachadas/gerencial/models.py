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
    idProveedor=models.ForeignKey(Proveedor,on_delete=models.CASCADE)
    fechaHora=models.DateTimeField()

    def __str__(self):
        return self.fechaHora

class Producto(models.Model):
    idCategoria=models.ForeignKey(Categoria,on_delete=models.CASCADE)
    idInventario=models.ForeignKey(Inventario,on_delete=models.CASCADE)
    codigo=models.CharField(max_length=10)
    nombre=models.CharField(max_length=25)


    def __str__(self):
        return self.codigo

class DetalleCompra(models.Model):
    idCompra=models.ForeignKey(Compra,on_delete=models.CASCADE)
    idProducto=models.ForeignKey(Producto,on_delete=models.CASCADE)

    def __str__(self):
        return "detalle compra: compra: "+str(self.idCompra)+" - producto: "+str(self.idProducto)

class Kardex(models.Model):
    idProducto=models.ForeignKey(Producto,on_delete=models.CASCADE)
    fecha=models.DateField()
    precExistencia=models.DecimalField(max_digits=8,decimal_places=2)
    cantExistencias=models.IntegerField()

    def __str__(self):
        return str(self.fecha)+" "+str(self.idProducto)

class ProductoRetorno(models.Model):
    idCliente=models.ForeignKey(Cliente,on_delete=models.CASCADE)
    idProducto=models.ForeignKey(Producto,on_delete=models.CASCADE)
    cantidad=models.IntegerField()
    nombre_cliente=models.CharField(max_length=20)
    nombre_producto=models.CharField(max_length=40)
    codigo=models.CharField(max_length=10)
    fecha=models.DateField()

    def __str__(self):
        return self.codigo

class ProductoConsigna(models.Model):
    idCliente=models.ForeignKey(Cliente,on_delete=models.CASCADE)
    idProducto=models.ForeignKey(Producto,on_delete=models.CASCADE)
    cantidad=models.IntegerField()
    fechaInicio=models.DateField()
    fechaFin=models.DateField()

    def __str__(self):
        return "consigna: idcliente: "+str(self.idCliente)+" idproducto: "+str(self.idProducto)

class ProductoPotencial(models.Model):
    idCliente=models.ForeignKey(Cliente,on_delete=models.CASCADE)
    nombre=models.CharField(max_length=25)
    cantidad=models.IntegerField()

    def __str__(self):
        return self.nombre

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
            ('etl','administrador'),
            ('gestion_usuarios','administrador'),
        )



