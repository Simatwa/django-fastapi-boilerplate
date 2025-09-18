"""Common functions for tests"""

from pydantic import BaseModel


def get_model_example(model: BaseModel) -> dict:
    container: dict = (
        model.config["json_schema_extra"] if hasattr(model, "config") else model.Config.json_schema_extra
    )
    return container.get("example") or container["examples"][0]
