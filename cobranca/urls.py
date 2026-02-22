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
    IndiceViewSet,
    BoletoViewSet,
    ImportBoletosView,
    EscolaViewSet, DividaViewSet, extrato_view, ImportarResponsaveisComBoletos,
)

app_name = "cobranca"

router = routers.DefaultRouter()

router.register("tipocobrancas", TipoCobrancaViewSet, basename="tipocobrancas")
router.register("bancos", BancoViewSet, basename="bancos")
router.register("escritorios", EscritorioViewSet, basename="escritorios")
router.register("posicaocheques", PosicaoChequeViewSet, basename="posicaocheques"),
router.register("entidades", EntidadeViewSet, basename="entidades"),
router.register("escolas", EscolaViewSet, basename="escolas"),
router.register("responsaveis", ResponsavelViewSet, basename="responsaveis"),
router.register("posicaocontratos", PosicaoContratoViewSet, basename="posicaocontratos"),
router.register("lugares", LugarViewSet, basename="lugares"),
router.register("andamentos", AndamentoViewSet, basename="andamentos"),
router.register("alineas", AlineaViewSet, basename="alineas"),
router.register("acordos", AcordoViewSet, basename="acordos"),
router.register("acordoparcelas", AcordoParcelasViewSet, basename="acordoparcelas"),
router.register("boletos", BoletoViewSet, basename="boletos"),
router.register("dividas", DividaViewSet, basename="dividas"),
router.register("indices", IndiceViewSet, basename="indices"),

urlpatterns = router.urls + [
    path("importboletos/", ImportBoletosView.as_view(), name="import-boletos"),
    path("importar-responsaveis-com-boletos/", ImportarResponsaveisComBoletos.as_view(), name="import-resp"),
    path("responsaveis/<uuid:responsavel_id>/extrato/", extrato_view, name="extrato")
]
