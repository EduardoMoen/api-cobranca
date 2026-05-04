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
    ImportBoletosView,
    EscolaViewSet,
    DividaViewSet,
    extrato_view,
    ImportarResponsaveisComBoletos,
    ImportResponsaveisApi,
    EnviarEmail,
    carta_view,
    ValidarResponsaveis,
    ValidarBoletos,
    ImportCsvView,
    carta_por_entidade_view,
    carta_por_escola_view,
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
router.register("dividas", DividaViewSet, basename="dividas"),
router.register("indices", IndiceViewSet, basename="indices"),

urlpatterns = router.urls + [
    path("importar-boletosApi/", ImportBoletosView.as_view(), name="importar-boletosApi"),
    path("importar-responsaveisApi/", ImportResponsaveisApi.as_view(), name="importar-responsaveisApi"),
    path("importar-responsaveis-com-boletos/", ImportarResponsaveisComBoletos.as_view(), name="import-resp"),
    path("mandar-email/", EnviarEmail.as_view(), name="enviar-email"),
    path("dividas/<uuid:responsavel_id>/extrato/", extrato_view, name="extrato"),
    path("dividas/<uuid:responsavel_id>/carta/", carta_view, name="carta"),
    path("dividas/<uuid:escola_id>/carta-escola/", carta_por_escola_view, name="carta-por-escola"),
    path("dividas/<uuid:entidade_id>/carta-entidade/", carta_por_entidade_view, name="carta-por-entidade"),
    path("validar-responsaveis/", ValidarResponsaveis.as_view(), name="validar-responsaveis"),
    path("validar-boletos/", ValidarBoletos.as_view(), name="validar-boletos"),
    path("importar-csv/", ImportCsvView.as_view(), name="importar-csv"),
]
