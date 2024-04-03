from urllib.parse import urlparse

import requests
from django.conf import settings
from django.core.cache import cache
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from requests import Request, Response


class MeldingenService:
    _api_base_url = None
    _timeout: tuple[int, ...] = (5, 10)
    _v = "v1"
    _api_path: str = f"/api/{_v}"

    class BasisUrlFout(Exception):
        ...

    class NaarJsonFout(Exception):
        ...

    class DataOphalenFout(Exception):
        ...

    class AanvraagFout(Exception):
        ...

    class VerkeerdeUrlVoorMethodeFout(Exception):
        ...

    def __init__(self, *args, **kwargs: dict):
        self._api_base_url = settings.MELDINGEN_URL
        super().__init__(*args, **kwargs)

    def naar_json(self, response):
        try:
            return response.json()
        except Exception:
            raise MeldingenService.NaarJsonFout(
                f"Json antwoord verwacht, antwoord tekst: {response.text}"
            )

    def relatieve_url(self, url: str):
        if not isinstance(url, str):
            raise MeldingenService.BasisUrlFout("Url kan niet None zijn")
        url_o = urlparse(url)
        if not url_o.scheme and not url_o.netloc:
            return url
        if f"{url_o.scheme}://{url_o.netloc}" == self._api_base_url:
            return f"{url_o.path}{url_o.query}"
        raise MeldingenService.BasisUrlFout(
            f"url: {url}, basis_url: {self._api_base_url}"
        )

    def test_url(self, invoer_url: str, url_begint_met: str):
        if self.relatieve_url(invoer_url).startswith(url_begint_met):
            return True
        raise MeldingenService.VerkeerdeUrlVoorMethodeFout(
            f"{invoer_url}(invoer_url) -> {url_begint_met}(url_begint_met)"
        )

    def get_url(self, url):
        return f"{self._api_base_url}{self.relatieve_url(url)}"

    def haal_token(self):
        meldingen_token = cache.get("meldingen_token")
        if not meldingen_token:
            email = settings.MELDINGEN_USERNAME
            try:
                validate_email(email)
            except ValidationError:
                email = f"{settings.MELDINGEN_USERNAME}@forzamor.nl"
            token_response = requests.post(
                settings.MELDINGEN_TOKEN_API,
                json={
                    "username": email,
                    "password": settings.MELDINGEN_PASSWORD,
                },
            )
            if token_response.status_code == 200:
                meldingen_token = token_response.json().get("token")
                cache.set(
                    "meldingen_token", meldingen_token, settings.MELDINGEN_TOKEN_TIMEOUT
                )
            else:
                raise MeldingenService.DataOphalenFout(
                    f"status code: {token_response.status_code}, response text: {token_response.text}"
                )

        return meldingen_token

    def get_headers(self):
        headers = {"Authorization": f"Token {self.haal_token()}"}
        return headers

    def do_request(self, url, method="get", data={}, raw_response=True, stream=False):
        action: Request = getattr(requests, method)
        action_params: dict = {
            "url": self.get_url(url),
            "headers": self.get_headers(),
            "json": data,
            "timeout": self._timeout,
            "stream": stream,
        }
        try:
            response: Response = action(**action_params)
        except Exception as e:
            raise MeldingenService.AanvraagFout(
                f"oorspronkelijke url: {url}, url: '{self.get_url(url)}', fout: {e}"
            )
        if response.status_code >= 400:
            raise MeldingenService.DataOphalenFout(
                f"Verwacht status code < 400, kreeg status code '{response.status_code}', antwoord tekst: {response.text}"
            )
        if raw_response:
            return response
        return self.naar_json(response)

    def signaal_aanmaken(self, data: {}):
        response = self.do_request(
            f"{self._api_path}/signaal/",
            method="post",
            data=data,
        )
        if response.status_code == 201:
            return self.naar_json(response)
        raise MeldingenService.DataOphalenFout(
            f"signaal_aanmaken: Verwacht status code 201, kreeg status code '{response.status_code}'"
        )

    def signaal_ophalen(self, signaal_url: str):
        self.test_url(signaal_url, f"/api/{self._v}/signaal/")
        response = self.do_request(signaal_url)
        if response.status_code == 200:
            return self.naar_json(response)
        raise MeldingenService.DataOphalenFout(
            f"signaal_ophalen: Verwacht status code 200, kreeg status code '{response.status_code}'"
        )

    def melding_ophalen(self, signaal_melding_url: str):
        self.test_url(signaal_melding_url, f"/api/{self._v}/melding/")
        response = self.do_request(signaal_melding_url)
        if response.status_code == 200:
            return self.naar_json(response)
        raise MeldingenService.DataOphalenFout(
            f"melding_ophalen: Verwacht status code 200, kreeg status code '{response.status_code}'"
        )

    def melding_ophalen_met_signaal_url(self, signaal_url: str):
        meldingen_signaal = MeldingenService().signaal_ophalen(signaal_url)
        return MeldingenService().melding_ophalen(
            meldingen_signaal.get("_links", {}).get("melding")
        )

    def afbeelding_ophalen(self, afbeelding_url: str, stream=False):
        return self.do_request(afbeelding_url, stream=stream)
