import requests_mock
from apps.services.meldingen import MeldingenService
from rest_framework.test import APITestCase


class MeldingenServiceTest(APITestCase):
    @requests_mock.Mocker()
    def setUp(self, m):
        ...

    def test_verkeerde_basis_url(self):
        service = MeldingenService()
        with self.assertRaises(MeldingenService.BasisUrlFout):
            service.relatieve_url("http://verkeerde_mock_url/api/test/")

    @requests_mock.Mocker()
    def test_url_is_none(self, m):
        service = MeldingenService()
        with self.assertRaises(MeldingenService.BasisUrlFout):
            service.signaal_ophalen(signaal_url=None)

    @requests_mock.Mocker()
    def test_url_is_mock(self, m):
        service = MeldingenService()
        with self.assertRaises(MeldingenService.VerkeerdeUrlVoorMethodeFout):
            service.signaal_ophalen(signaal_url="mock")
