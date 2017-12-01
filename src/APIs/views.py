from django.shortcuts import render

# Create your views here.

from register.models import Profile ,Personal ,PersonalColegio ,Colegio
from .serializers import ColegioSerializer, ProfileSerializer
from rest_framework import generics
from django.views.generic import ListView
from utils.middleware import get_current_request, get_current_user
from authtools.models import User

class UserInfoListView(ListView):
    model = Profile
    template_name = 'UserInfo.html'

    def get_context_data(self, **kwargs):
        context = super(UserInfoListView, self).get_context_data(**kwargs)
        usuario = get_current_user()
        if usuario is not None:
            iduser = usuario.id
        else:
            iduser = -1
        profile_id = Profile.objects.get(user_id=iduser)
        personal_id = Personal.objects.get(persona_id=profile_id)
        #personalcolegio_id = PersonalColegio.objects.values('pk').filter(personal_id=personal_id)[0]['pk']
        context['id_usuario'] = iduser
        context['nombre_usuario'] = User.objects.values('name').filter(id=iduser)[0]['name']
        context['usuario_email'] = User.objects.values('email').filter(id=iduser)[0]['email']
        context['nombre_profile'] = Profile.objects.values('nombre').filter(user_id=iduser)[0]['nombre']
        context['nombre2_profile'] = Profile.objects.values('segundo_nombre').filter(user_id=iduser)[0]['segundo_nombre']
        context['apellido_pa_profile'] = Profile.objects.values('apellido_pa').filter(user_id=iduser)[0]['apellido_pa']
        context['apellido_ma_profile'] = Profile.objects.values('apellido_ma').filter(user_id=iduser)[0]['apellido_ma']
        id_colegio = PersonalColegio.objects.values('colegio_id').filter(personal_id=personal_id)[0]['colegio_id']
        context['id_colegio'] = id_colegio
        context['nombre_colegio'] = Colegio.objects.values('nombre').filter(id_colegio=id_colegio)[0]['nombre']
        return context

class ColegioList(generics.ListCreateAPIView):
    queryset = Colegio.objects.all()
    serializer_class = ColegioSerializer


class ColegioDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Colegio.objects.all()
    serializer_class = ColegioSerializer


class PerfilList(generics.ListCreateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class PerfilDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

