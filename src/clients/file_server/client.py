import sentry_sdk
from httpx import AsyncClient, ConnectError, Response

from clients.file_server.exceptions import ServerNotWorkingError, WrongResponseError
from clients.file_server.models import (
    RecognizeVoiceRequestModel,
    RecognizeVoiceResponseModel,
)
from settings import settings


class Client:
    _BASE_DOMAIN: str = settings.file_server_domain
    _API_PREFIX: str = "/api/v1"

    def __init__(self, http_client: AsyncClient):
        self.http_client = http_client

    async def recognize_speech(self, data: RecognizeVoiceRequestModel) -> RecognizeVoiceResponseModel:
        """Asynchronously recognizes speech from voice data.

        This method sends a POST request to the voice recognition service with the given voice data
        and returns the recognized voice response. In case of an unsuccessful request, it captures
        the error message and raises a `ServerNotWorkingError`.

        Parameters
        ----------
        data : RecognizeVoiceRequestModel
            An instance of `RecognizeVoiceRequestModel` containing the voice data to be recognized.

        Returns
        -------
        RecognizeVoiceResponseModel
            An instance of `RecognizeVoiceResponseModel` containing the results of the speech recognition.

        Raises
        -------
        ServerNotWorkingError
            If the server response status code is not 200, indicating a failure in processing the request.
        """

        try:
            response = await self._request("POST", "/voice/recognize", json=data.model_dump())
        except ConnectError as exc:
            sentry_sdk.capture_exception(exc)
            raise ServerNotWorkingError
        if response.status_code != 200:
            sentry_sdk.capture_message(response.text)
            raise WrongResponseError
        return RecognizeVoiceResponseModel.model_validate(response.json())

    async def _request(self, method: str, url: str, **kwargs) -> Response:
        return await self.http_client.request(method, f"{self._BASE_DOMAIN}{self._API_PREFIX}{url}", **kwargs)
