import datetime
import calendar
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import FormView
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.views.generic import TemplateView

from AE_academico.forms import AulaForm, MarcarAsistenciaForm, SubirNotasForm, CursoForm, EventoForm
from AE_academico.forms import CursoDocenteForm
from AE_academico.models import Aula, Asistencia, Notas, AulaCurso, Evento, HorarioAula
from AE_academico.models import CursoDocente
from AE_academico.models import Curso
from enrollment.models import Matricula
from income.models import obtener_mes
from register.models import Docente, Personal, PersonalColegio, Alumno, Colegio
from django.conf import settings
from utils.middleware import validar_roles, get_current_request, get_current_colegio, get_current_user
from django.http import HttpResponseRedirect
from utils.views import MyLoginRequiredMixin
import logging
logger = logging.getLogger("project")

#################################################
#####            CRUD DE AULA               #####
#################################################


class AulaListView(MyLoginRequiredMixin, ListView):
    model = Aula
    template_name = 'aula_list.html'

    def get(self, request, *args, **kwargs):
        roles = ['promotor', 'director', 'administrativo', 'tesorero', 'cajero']
        if validar_roles(roles=roles):
            return super(AulaListView, self).get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(settings.REDIRECT_PERMISOS)

    def get_context_data(self, **kwargs):

            context = super(AulaListView, self).get_context_data(**kwargs)

            request = get_current_request()

            if request.session.get('colegio'):
                id = request.session.get('colegio')
                context['idcolegio'] = id
            return context


class AulaDetailView(UpdateView):
    model = Aula
    form_class = AulaForm
    template_name = 'aula_detail.html'

    def get(self, request, *args, **kwargs):
        roles = ['promotor', 'director', 'administrativo', 'tesorero', 'cajero']
        if validar_roles(roles=roles):
            aula_id = 1
            id_colegio = get_current_colegio()
            matriculadosaula = Matricula.objects.filter(colegio_id=id_colegio, activo=True,
                                                        tipo_servicio=1).order_by('alumno__apellido_pa')
            aula = Aula.objects.get(id_aula=aula_id)
            return render(request, template_name=self.template_name, context={
                'matriculados_aula': matriculadosaula,
                'aula': aula,
            })
        else:
            return HttpResponseRedirect(settings.REDIRECT_PERMISOS)
"""
class AulaDetailView(UpdateView):
    model = Aula
    form_class = AulaForm
    template_name = 'aula_detail.html'

    def get(self, request, *args, **kwargs):
        roles = ['promotor', 'director', 'administrativo', 'tesorero', 'cajero']
        if validar_roles(roles=roles):
            return super(AulaDetailView, self).get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(settings.REDIRECT_PERMISOS)
"""

class AulaCreationView(CreateView):
    model = Aula
    form_class = AulaForm
    success_url = reverse_lazy('academic:aula_list')
    template_name = 'aula_form.html'

    def get(self, request, *args, **kwargs):
        roles = ['promotor', 'director', 'administrativo', 'tesorero']
        if validar_roles(roles=roles):
            return super(AulaCreationView, self).get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(settings.REDIRECT_PERMISOS)


class AulaUpdateView(UpdateView):
    model = Aula
    form_class = AulaForm
    success_url = reverse_lazy('academic:aula_list')
    template_name = 'aula_form.html'


class AulaDeleteView(DeleteView):
    model = Aula
    form_class = AulaForm
    success_url = reverse_lazy('academic:aula_list')
    template_name = 'aula_confirm_delete.html'

    def get(self, request, *args, **kwargs):
        roles = ['promotor', 'director', 'administrativo']
        if validar_roles(roles=roles):
            return super(AulaDeleteView, self).get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(settings.REDIRECT_PERMISOS)


#################################################
#####            CRUD DE CURSO              #####
#################################################


class CursoListView(MyLoginRequiredMixin, ListView):
    model = Curso
    template_name = 'curso_list.html'

    def get(self, request, *args, **kwargs):
        roles = ['promotor', 'director', 'administrativo']
        if validar_roles(roles=roles):
            return super(CursoListView, self).get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(settings.REDIRECT_PERMISOS)

    def get_context_data(self, **kwargs):

        context = super(CursoListView, self).get_context_data(**kwargs)

        request = get_current_request()

        if request.session.get('colegio'):
            id = request.session.get('colegio')
            context['idcolegio'] = id
        return context

class CursoDetailView(UpdateView):
    model = Curso
    form_class = CursoForm
    template_name = 'curso_detail.html'

    def get(self, request, *args, **kwargs):
        roles = ['promotor', 'director', 'administrativo']
        if validar_roles(roles=roles):
            return super(CursoDetailView, self).get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(settings.REDIRECT_PERMISOS)

class CursoCreationView(CreateView):
    model = Curso
    form_class = CursoForm
    success_url = reverse_lazy('academic:curso_list')
    template_name = 'curso_form.html'

    def form_valid(self, form):
        form.instance.colegio = Colegio.objects.get(pk=get_current_colegio())
        return super(CursoCreationView, self).form_valid(form)

    def get(self, request, *args, **kwargs):
        roles = ['promotor', 'director', 'administrativo']
        if validar_roles(roles=roles):
            return super(CursoCreationView, self).get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(settings.REDIRECT_PERMISOS)

class CursoUpdateView(UpdateView):
    model = Curso
    form_class = CursoForm
    success_url = reverse_lazy('academic:curso_list')
    template_name = 'curso_form.html'

class CursoDeleteView(DeleteView):
    model = Curso
    form_class = CursoForm
    success_url = reverse_lazy('academic:aula_list')
    template_name = 'curso_confirm_delete.html'

    def get(self, request, *args, **kwargs):
        roles = ['promotor', 'director', 'administrativo']
        if validar_roles(roles=roles):
            return super(CursoDeleteView, self).get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(settings.REDIRECT_PERMISOS)

#################################################
#####            CRUD DE CURSO DOCENTE      #####
#################################################

class CursoDocenteCreateView(CreateView):
    model = CursoDocente
    form_class = CursoDocenteForm
    success_url = reverse_lazy('academic:aula_list')
    template_name = 'cursodocente_form.html'

    def get(self, request, *args, **kwargs):
        roles = ['promotor', 'director', 'administrativo', 'tesorero']
        if validar_roles(roles=roles):
            personalcolegio = PersonalColegio.objects.filter(colegio_id=get_current_colegio(), activo=True)
            personal = []
            docentes = []
            for personalcol in personalcolegio:
                personal.append(personalcol.personal)
            cursos = AulaCurso.objects.filter(aula__tipo_servicio__colegio_id=get_current_colegio(),
                                              activo=True)
            for persona in personal:
                try:
                    docentes.append(Docente.objects.get(empleado=persona))
                except:
                    logger.info("Persona no es un docente ---- AE_academico")
            return render(request, template_name=self.template_name, context={
                'form': self.form_class,
                'docentes': docentes,
                'cursos': cursos,
            })

        else:
            return HttpResponseRedirect(settings.REDIRECT_PERMISOS)

#################################################
#####            CRUD DE  AULA CURSO        #####
#################################################

class AulaCursoCreateView(TemplateView):
    model = AulaCurso
    success_url = reverse_lazy('academic:aula_list')
    template_name = 'aulacurso_form.html'

    def get(self, request, *args, **kwargs):
        roles = ['promotor', 'director', 'administrativo', 'tesorero']
        if validar_roles(roles=roles):
            aula_actual = Aula.objects.get(id_aula=request.GET['aula'])
            cursos = Curso.objects.filter(colegio_id=get_current_colegio(), activo=True)
            return render(request, template_name=self.template_name, context={
                'aula': aula_actual,
                'cursos': cursos,
            })

        else:
            return HttpResponseRedirect(settings.REDIRECT_PERMISOS)

    def post(self, request, *args, **kwargs):
        print(request.POST)
        cursos = Curso.objects.filter(colegio_id=get_current_colegio(), activo=True)
        aula = Aula.objects.get(id_aula=request.POST['aula'])
        data_form = request.POST
        try:
            for curso in cursos:
                text = "item{0}".format(curso.id_curso)

                if data_form[text]:
                    aulacurso = self.model(
                        aula=aula,
                        curso=curso,
                    )
                    aulacurso.save()
                    print("se creo un registro")
        except:
            print("hay un error")

        return HttpResponseRedirect(reverse('academic:aula_list'))


#################################################
#####          ASISTENCIA ALUMNOS           #####
#################################################

class MarcarAsistenciaView(CreateView):

    model = Asistencia
    template_name = 'marcar_asistencia.html'
    form_class = MarcarAsistenciaForm
    success_url = reverse_lazy('academic:asistencia_ver')

    def get(self, request, *args, **kwargs):
        roles = ['promotor', 'director', 'administrativo']
        if validar_roles(roles=roles):
            # AQUI VA EL ID DE TIPO DE SERVICIO
            id_tipo_servicio = 1
            docente = True
            id_colegio = get_current_colegio()
            matriculadosaula = Matricula.objects.filter(colegio_id=id_colegio, activo=True, tipo_servicio=id_tipo_servicio).order_by('alumno__apellido_pa')
            logger.info("Datos son {0}".format(matriculadosaula))

            alumnos = []
            for matriculado in matriculadosaula:
                alumnos.append(matriculado.alumno)
            return render(request, template_name=self.template_name, context={
                'form': self.form_class,
                'alumnos': alumnos,
                'docente': docente,
            })

        else:
            return HttpResponseRedirect(settings.REDIRECT_PERMISOS)

    def post(self, request, *args, **kwargs):
        logger.info("Estoy en el POST")
        logger.info("Los datos de llegada son {0}".format(request.POST))
        data_post = request.POST

        alumnos_id = data_post.getlist('id')
        estado_asistencias = data_post.getlist('estado_asistencia')
        logger.info("Los estados son {0}".format(estado_asistencias))
        num = len(alumnos_id)

        for n in range(0,num):
            alumno = Alumno.objects.get(id_alumno = alumnos_id[n])
            asistencia = Asistencia(alumno=alumno, fecha=datetime.date.today(), estado_asistencia=estado_asistencias[n])
            asistencia.save()

        contexto = {}
        return redirect('academic:asistencia_ver')


class VisualizarAsistenciaView(TemplateView):

    model = Asistencia
    template_name = "asistencia_ver.html"
    #form_class = CuentasCobrarPromotorDetalleForm

    def VisualizarAsistenciaform(self, request):

        roles = ['promotor', 'director']

        if validar_roles(roles=roles):

            # Cargamos los meses
            meses_todos = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto",
                           "Setiembre", "Octubre", "Noviembre", "Diciembre"]
            num_mes = datetime.date.today().month
            meses = []
            for i in range(0, num_mes + 1):
                meses.append(meses_todos[i])

            id_colegio = get_current_colegio()
            aulas = Aula.objects.filter(tipo_servicio__colegio=id_colegio).order_by('nombre')

            return {'meses': meses_todos, 'aulas': aulas}

        else:
            mensaje_error = "No tienes acceso a esta vista"
            return {'mensaje_error': mensaje_error}  # return context


    def get(self, request, *args, **kwargs):
        super(VisualizarAsistenciaView, self).get(request, *args, **kwargs)

        contexto = self.VisualizarAsistenciaform(request)

        if 'mensaje_error' in contexto.keys():
            return HttpResponseRedirect(settings.REDIRECT_PERMISOS)
        else:
            return render(request, self.template_name, contexto)  # return context


    def post(self, request, *args, **kwargs):

        mes = request.POST["mes"]
        num_mes = obtener_mes(mes)

        meses_dias = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        num_dias = meses_dias[num_mes-1]

        #id_curso =

        asistencias_curso = self.model.objects.filter()

        # Proceso de filtrado según el año
        anio = datetime.date.today().year
        asistencias_curso_anio = asistencias_curso.filter(fecha__year=anio)

        # Proceso de filtrado según el mes
        asistencias_curso_mes = asistencias_curso_anio.filter(fecha__month=num_mes)
        logger.info("La lista de asistencias de mes son {0}".format(asistencias_curso_mes))

        id_tipo_servicio = 1
        id_colegio = get_current_colegio()
        matriculados_aula = Matricula.objects.filter(colegio_id=id_colegio, activo=True, tipo_servicio=id_tipo_servicio).order_by('alumno__apellido_pa')
        alumnos = []
        for matriculado in matriculados_aula:
            alumnos.append(matriculado.alumno)
        len(alumnos)


        fechas = []
        lista_asistencias_dia = []
        for dia in range(0, num_dias):
            asistencias_curso_dia = asistencias_curso_mes.filter(fecha__day=dia+1)
            logger.info("La lista de asistencias del día {0} mes son {1}".format(dia+1, asistencias_curso_dia))
            n = 0
            for asistencias_dias in asistencias_curso_dia:
                lista_asistencias_dia.append(asistencias_dias.estado_asistencia)
                if n == 0:
                    fechas.append(asistencias_dias.fecha)
                n = n + 1
        num_horizontal = len(fechas)
        num_vertical = len(alumnos)

        logger.info("La lista de asistencias de mes son {0}".format(lista_asistencias_dia))
        logger.info("La lista de fechas de mes son {0}".format(fechas))

        contexto = self.VisualizarAsistenciaform(request)

        contexto['asistencias'] = asistencias_curso_mes
        contexto['num_hor'] = num_horizontal
        contexto['num_ver'] = num_vertical
        contexto['fechas'] = fechas
        contexto['alumnos'] = alumnos
        contexto['form'] = VisualizarAsistenciaView
        return render(request, template_name=self.template_name, context=contexto)


#################################################
#####             NOTAS ALUMNOS             #####
#################################################


class SubirNotasView(CreateView):

    model = Notas
    template_name = 'notas_subir.html'
    form_class = SubirNotasForm
    success_url = reverse_lazy('academic:aula_list')

    def get(self, request, *args, **kwargs):
        roles = ['promotor', 'director', 'administrativo']
        if validar_roles(roles=roles):
            # AQUI VA EL ID DE TIPO DE SERVICIO
            id_tipo_servicio = 4
            id_colegio = get_current_colegio()
            matriculadosaula = Matricula.objects.filter(colegio_id=id_colegio, activo=True, tipo_servicio=id_tipo_servicio).order_by('alumno__apellido_pa')
            logger.info("Datos son {0}".format(matriculadosaula))



            alumnos = []
            for matriculado in matriculadosaula:
                alumnos.append(matriculado.alumno)
            return render(request, template_name=self.template_name, context={
                'form': self.form_class,
                'alumnos': alumnos,
            })

        else:
            return HttpResponseRedirect(settings.REDIRECT_PERMISOS)

    def post(self, request, *args, **kwargs):

        logger.info("Estoy en el POST")
        data_post = request.POST
        logger.info("Los datos de llegada son {0}".format(data_post))


        #id_colegio = get_current_colegio()


        contexto = {}
        return render(request, template_name=self.template_name, context=contexto)



#################################################
#####                EVENTOS                #####
#################################################


class EventoCreateView(CreateView):
    model = Evento
    form_class = EventoForm
    template_name = "evento_form.html"
    success_url = reverse_lazy("academics:evento_list")

    def form_valid(self, form):
        form.instance.colegio = Colegio.objects.get(pk=get_current_colegio())
        return super(EventoCreateView, self).form_valid(form)

    def get(self, request, *args, **kwargs):
        roles = ['promotor', 'director', 'administrativo']
        if validar_roles(roles=roles):
            personalcolegio = PersonalColegio.objects.filter(colegio_id=get_current_colegio(), activo=True)
            personal = []
            for personalcol in personalcolegio:
                personal.append(personalcol.personal)
            return render(request, template_name=self.template_name, context={
                'form': self.form_class,
                'empleados': personal,
            })

        else:
            return HttpResponseRedirect(settings.REDIRECT_PERMISOS)


class EventoListView(ListView):
    model = Evento
    form_class = EventoForm
    template_name = "evento_list.html"

    def get(self, request, *args, **kwargs):
        roles = ['promotor', 'director', 'administrativo']
        if validar_roles(roles=roles):
            evento = Evento.objects.filter(colegio_id=get_current_colegio())
            return render(request, template_name=self.template_name, context={
                'eventos':evento,
            })

        else:
            return HttpResponseRedirect(settings.REDIRECT_PERMISOS)

class EventoDetailView(ListView):
    model = Evento
    form_class = EventoForm
    template_name = "evento_detail.html"


    def get(self, request, *args, **kwargs):
        roles = ['promotor', 'director', 'administrativo']
        if validar_roles(roles=roles):
            evento = Evento.objects.get(id_evento=request.GET['evento'])
            return render(request, template_name=self.template_name, context={
                'evento':evento,
            })

        else:
            return HttpResponseRedirect(settings.REDIRECT_PERMISOS)




#################################################
#####               HORARIOS                #####
#################################################


class HorarioCursoCreateView(CreateView):
    model = HorarioAula #Debería ser HorarioCurso, hay que cambiar el nombre
    form_class = CursoDocenteForm
    success_url = reverse_lazy('academic:aula_list')
    template_name = 'cursodocente_form.html'

    def get(self, request, *args, **kwargs):
        roles = ['promotor', 'director', 'administrativo', 'tesorero']
        if validar_roles(roles=roles):
            personalcolegio = PersonalColegio.objects.filter(colegio_id=get_current_colegio(), activo=True)
            personal = []
            docentes = []
            for personalcol in personalcolegio:
                personal.append(personalcol.personal)
            cursos = AulaCurso.objects.filter(aula__tipo_servicio__colegio_id=get_current_colegio(),
                                              activo=True)
            for persona in personal:
                try:
                    docentes.append(Docente.objects.get(empleado=persona))
                except:
                    logger.info("Persona no es un docente ---- AE_academico")
            return render(request, template_name=self.template_name, context={
                'form': self.form_class,
                'docentes': docentes,
                'cursos': cursos,
            })

        else:
            return HttpResponseRedirect(settings.REDIRECT_PERMISOS)








