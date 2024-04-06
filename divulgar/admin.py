from django.contrib import admin
from .models import Raca, Tag, Pet
from adotar.models import PedidoAdocao

# Register your models here.
admin.site.register(Raca)
admin.site.register(Tag)
admin.site.register(Pet)
admin.site.register(PedidoAdocao)