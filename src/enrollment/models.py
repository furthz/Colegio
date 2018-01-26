from django.db import models
from django.urls import reverse
from register.models import Sucursal
from register.models import Alumno
from profiles.models import Profile
from utils.models import ActivoMixin
from utils.models import CreacionModificacionFechaMixin
from utils.models import CreacionModificacionUserMixin
# Create your models here.

class TipoServicio(ActivoMixin, CreacionModificacionFechaMixin, CreacionModificacionUserMixin, models.Model):
    """
    isordinario:        indica si el servicio es ordinario (1er grado, 2do grado, etc.)
                        o extra (curso de verano, danza, etc.)
    nivel:              indica el nivel que el colegio puede dictar (inicial, primaria, secundaria)
    grado:              indica los grados que el colegio puede dictar
    extra:              curso extraordinarios que el colegio dicta
    codigomodular:      numero que identifica al colegio
    """
    id_tipo_servicio = models.AutoField(primary_key=True)
    colegio = models.ForeignKey(Sucursal, models.DO_NOTHING, db_column='id_colegio')
    is_ordinario = models.BooleanField()
    nivel = models.IntegerField(blank=True, null=True)
    grado = models.IntegerField(blank=True, null=True)
    extra = models.CharField(max_length=50, blank=True, null=True)
    codigo_modular = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        """
        Solo retorna informacion de la clase como string
        :return: nombre del servicio
        """
        if self.extra is not None:
            return "{0}".format(self.extra)
        else:
            return "{1} de {0} ".format(self.getTipoNivel, self.getTipoGrado)

    def full_detail(self):
        """
        Da una descripcion detallada de la informacion del Tipo de Servicio
        :return: lista de todos los atributos de la clase
        """
        if self.extra is not None:
            extra = self.extra
            codigo_modular = "--"
        else:
            codigo_modular = self.codigo_modular
            extra = "--"
        user_create = Profile.objects.get(pk=self.usuario_creacion)
        user_update = Profile.objects.get(pk=self.usuario_modificacion)
        detalle_completo = ["Nivel: {0}".format(self.getTipoNivel),
                            "Grado: {0}".format(self.getTipoGrado),
                            "Extra: {0}".format(extra),
                            "Codigo modular: {0}".format(codigo_modular),
                            "Fecha creacion: {0}".format(self.fecha_creacion),
                            "Fecha modificacion: {0}".format(self.fecha_modificacion),
                            "Usuario creacion: {0}".format(user_create.getNombreCompleto),
                            "Usuario modificacion: {0}".format(user_update.getNombreCompleto)
                            ]
        return detalle_completo

    def get_absolute_url(self):
        """
        Redirecciona las views que usan como modelo esta clase
        :return: url de detalles del tipo de servicio
        """
        return reverse('enrollments:tiposervicio_detail', kwargs={'pk': self.pk})
        #return "/servicios/impdates/list/{0}/".format(str(self.pk))

    @property
    def getTipoNivel(self):
        """
        Método que retorna la descripción del tipo de nivel, cruzándolo con el cataloto TipoNivel
        :return: Descripción del catalogo TipoNivel
        """

        from utils.models import TiposNivel

        idtipo = self.nivel
        if idtipo is not None:
            tipodoc = TiposNivel.objects.get(pk=idtipo)
            return tipodoc.descripcion
        else:
            return "--"

    @property
    def getTipoGrado(self):
        """
        Método que retorna la descripción del tipo de grado, cruzándolo con el cataloto TiposGrados
        :return: Descripción del catalogo TiposGrados
        """

        from utils.models import TiposGrados

        idtipo = self.grado
        if idtipo is not None:
            tipodoc = TiposGrados.objects.get(pk=idtipo)
            return tipodoc.descripcion
        else:
            return "--"

    def getServiciosAsociados(self):
        return Servicio.objects.filter(tipo_servicio_id=self.id_tipo_servicio, activo=True)

    class Meta:
        managed = False
        #db_table = 'tipo_servicio'
        permissions = (
            ("Cargar_Tipo_Servicio_Create", "cargar tipo de servicio"),
            ("Tipo_Servicio_Regular_Create","cargar tipo de servicio regular"),
            ("Tipo_Servicio_Extra_Create","cargar tipo de servicio extra"),
            ("Tipo_Servicio_Detail","cargar detalle de tipo de servicio "),
            ("Tipo_Servicio_Regular_End_Update","actualizar tipo de servicio regular end"),
            ("Tipo_Servicio_Extra_End_Update","actualizar tipo de servicio extra end"),
            ("Tipo_Servicio_Regular_Update","actualizar tipo de servicio regular"),
            ("Tipo_Servicio_Extra_Update","actualizar tipo de servicio extra"),
            ("Tipo_Servicio_Delete","borrar tipo de servicio"),
            ("Tipo_Servicio_List","listar tipo de servicio"),
        )

        #unique_together = (('id_tipo_servicio', 'colegio'),)

class Servicio(ActivoMixin, CreacionModificacionFechaMixin, CreacionModificacionUserMixin, models.Model):
    """
    nombre:         nombre del servicio
    precio:         precio del servicio
    isperiodic:     indica si el servicio tiene un costo periodico o no
    fechafacturar:  indica la fecha de facturacion
    cuotas:         indica el numero de cuotas en caso de ser periodico
    """
    id_servicio = models.AutoField(primary_key=True)
    tipo_servicio = models.ForeignKey('TipoServicio', models.DO_NOTHING, db_column='id_tipo_servicio')
    nombre = models.CharField(max_length=100)
    precio = models.FloatField()
    is_periodic = models.BooleanField()
    fecha_facturar = models.DateField()
    cuotas = models.IntegerField()

    def __str__(self):
        """
        Solo retorna informacion de la clase como string
        :return: nombre del servicio
        """
        return  "Servicio:  {0}    ------------------- precio: {1}".format(self.nombre,self.precio)

    def full_detail(self):
        """
        Da una descripcion detallada de la informacion del servicio
        :return: lista de todos los atributos de la clase
        """
        user_create = Profile.objects.get(pk=self.usuario_creacion)
        user_update = Profile.objects.get(pk=self.usuario_modificacion)
        detalle_completo = ["Descripcion: {0}".format(self.nombre),
                            "Precio: {0}".format(self.precio),
                            "Fecha Facturacion: {0}".format(self.fecha_facturar),
                            "Cuotas: {0}".format(self.cuotas),
                            "Fecha creacion: {0}".format(self.fecha_creacion),
                            "Fecha modificacion: {0}".format(self.fecha_modificacion),
                            "Usuario creacion: {0}".format(user_create.getNombreCompleto),
                            "Usuario modificacion: {0}".format(user_update.getNombreCompleto)
                            ]
        return detalle_completo

    def get_absolute_url(self):
        """
        Redirecciona las views que usan como modelo esta clase
        :return: url de la lista de servicios
        """
        return reverse('enrollments:servicio_list', kwargs={'pkts': self.tipo_servicio.pk})
        #return "/servicios/impdates/list/{0}/listservicios".format(str(self.tipo_servicio.id_tipo_servicio))

    class Meta:
        managed = False
        #db_table = 'servicio'
        permissions = (
            ("Servicio_Regular_Create", "crear un servicio regular"),
            ("Servicio_Extra_Create", "crear un servicios extra"),
            ("Servicio_Detail", "ver un detalle de servicio"),
            ("Servicio_Regular_End_Update", "actualizar un servicio regular end"),
            ("Servicio_Extra_End_Update", "actualizar un servicio extra end"),
            ("Servicio_Regular_Update", "actualizar un servicio regular"),
            ("Servicio_Extra_Update", "actualizar un servicio extra"),
            ("Servicio_Delete", "borrar un srvicio"),
            ("Servicio_List", "listar un servicio"),
        )

class Matricula(ActivoMixin, CreacionModificacionUserMixin, CreacionModificacionFechaMixin, models.Model):
    """

    """
    id_matricula = models.AutoField(primary_key=True)
    alumno = models.ForeignKey(Alumno, models.DO_NOTHING, db_column='id_alumno')
    colegio = models.ForeignKey(Sucursal, models.DO_NOTHING, db_column='id_colegio')
    tipo_servicio = models.ForeignKey(TipoServicio, models.DO_NOTHING, db_column='id_tipo_servicio')

    def __str__(self):
        """

        :return:
        """
        return "El alumno {0} registrado en el {1}".format(self.alumno.persona.getNombreCompleto, self.tipo_servicio)

    def get_absolute_url(self):
        """
        Redirecciona las views que usan como modelo esta clase
        :return: url de la lista de servicios
        """
        return reverse('enrollments:matricula_list')



    class Meta:
        managed = False
        #db_table = 'matricula'
        permissions = (
            ("Matricula_Create","crear una matricula"),
            ("Cargar_Matricula_Create","cargar una matricula"),
            ("Matricula_Detail","detalles de matricula"),
            ("Matricula_Update","matricula update"),
            ("Cargar_Matricula_Update","cargar matricula update"),
            ("Matricula_Delete","borrar matricula"),
            ("Matricula_List","listar matricula")
        )

class dCuentasManager(models.Manager):
    fecha_inicio = models.DateField
    fecha_final = models.DateField
    def get_queryset(self):
        return super(dCuentasManager, self).get_queryset()


class Cuentascobrar(ActivoMixin, CreacionModificacionFechaMixin, CreacionModificacionUserMixin, models.Model):
    """

    """
    id_cuentascobrar = models.AutoField(primary_key=True)
    matricula = models.ForeignKey(Matricula, models.DO_NOTHING, db_column='id_matricula')
    servicio = models.ForeignKey(Servicio, models.DO_NOTHING, db_column='id_servicio')
    fecha_ven = models.DateField()
    comentario = models.CharField(max_length=500, blank=True, null=True)
    estado = models.BooleanField()
    precio = models.FloatField()
    deuda = models.FloatField()
    descuento = models.FloatField()
    objects = models.Manager()
    objetos = dCuentasManager()

    class Meta:
        managed = False
        #db_table = 'cuentascobrar'
        permissions = (
            ('control_ingresos_padres', 'Para el control de ingresos de los padres'),
            ('control_ingresos_promotor', 'Para el control de ingresos del promotor'),
            ('control_ingresos_promotor_detalle', 'Para el detalle de control de ingresos del promotor'),
        )


    @property
    def getMonto(self):
        """
        Método que calcula los años de una persona
        :return: La cantidad de años de la persona
        """
        monto = self.precio - self.deuda - self.descuento
        return monto

