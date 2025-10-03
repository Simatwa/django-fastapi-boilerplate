"""Interacts with cloud spaces"""

from urllib.parse import urljoin

import httpx
from django.db import models

from project.settings import env_setting
from project.utils.common import get_event_loop


class CloudStorage:
    httpx_defaults = {
        "User-Agent": f"{env_setting.SITE_NAME} API v{env_setting.API_VERSION}",
        "Accept": "application/json",
        "Authorization": f"Bearer {env_setting.CLOUDSTORAGE_TOKEN}",
    }

    def __init__(self, base_url: str | None = None, **httpx_kwargs: dict):
        # Merge default headers into kwargs
        headers = httpx_kwargs.pop("headers", {})
        headers.update(self.httpx_defaults)

        base_url = base_url or env_setting.CLOUDSTORAGE_URL
        if base_url:
            assert env_setting.CLOUDSTORAGE_TOKEN, (
                "CloudStorage token is missing. "
                "Add CLOUDSTORAGE_TOKEN to your .env file."
            )
            self._upload_file = True
            self.client = httpx.AsyncClient(
                base_url=str(base_url),
                headers=headers,
                **httpx_kwargs,
            )
        else:
            self._upload_file = False
            self.client = None

    async def upload(
        self,
        model_file: models.ImageField | models.FileField,
        delete_local_file: bool = env_setting.DELETE_LOCALFILE,
    ) -> str | None:
        """
        Uploads a Django model FileField or ImageField file to cloud storage.
        Returns the accessible file URL (string).
        """
        if not self._upload_file:
            raise RuntimeError(
                "CloudStorage is disabled (no CLOUDSTORAGE_URL set)."
            )

        if not model_file:
            raise ValueError("No file provided for upload.")

        file_name = getattr(model_file, "name", "uploaded_file")
        file_content = model_file.read()

        files = {"file": (file_name, file_content)}

        resp = await self.client.post(
            "/storage/upload/",
            files=files,
        )
        resp.raise_for_status()

        # Expect API to return {"url": "..."}

        data = resp.json()

        file_path: str = data["url"]

        if delete_local_file:
            pass
            # model_file.
            # TODO: Complete this

        if not file_path.startswith("http"):
            return urljoin(str(env_setting.CLOUDSTORAGE_URL), file_path)

        return file_path

    def upload_sync(self, *args, **kwargs) -> str | None:
        return get_event_loop().run_until_complete(self.upload(*args, **kwargs))

    @classmethod
    def get_best_file_url(cls, local_file, cloud_url, default=None) -> None:
        return (
            cloud_url
            if cloud_url
            else local_file.url
            if local_file
            else default
        )
