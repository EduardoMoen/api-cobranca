from django.urls import path
from rest_framework import routers
from cobranca.views import (
    BancoViewSet,
    TipoCobrancaViewSet,
    EscritorioViewSet,
    PosicaoChequeViewSet,
    EntidadeViewSet,
    ResponsavelViewSet,
    PosicaoContratoViewSet,
    LugarViewSet,
    AndamentoViewSet,
    AlineaViewSet,
    AcordoViewSet,
    AcordoParcelasViewSet,
    BoletoViewSet,
    ImportBoletosView,
)

app_name = "cobranca"

router = routers.DefaultRouter()

router.register("tipocobrancas", TipoCobrancaViewSet, basename="tipocobrancas")
router.register("bancos", BancoViewSet, basename="bancos")
router.register("escritorios", EscritorioViewSet, basename="escritorios")
router.register("posicaocheques", PosicaoChequeViewSet, basename="posicaocheques"),
router.register("entidades", EntidadeViewSet, basename="entidades"),
router.register("escolas", EscritorioViewSet, basename="escolas"),
router.register("responsaveis", ResponsavelViewSet, basename="responsaveis"),
router.register("posicaocontratos", PosicaoContratoViewSet, basename="posicaocontratos"),
router.register("lugares", LugarViewSet, basename="lugares"),
router.register("andamentos", AndamentoViewSet, basename="andamentos"),
router.register("alineas", AlineaViewSet, basename="alineas"),
router.register("acordos", AcordoViewSet, basename="acordos"),
router.register("acordoparcelas", AcordoParcelasViewSet, basename="acordoparcelas"),
router.register("boletos", BoletoViewSet, basename="boletos"),

urlpatterns = router.urls + [
    path("importboletos/", ImportBoletosView.as_view(), name="import-boletos"),
]
