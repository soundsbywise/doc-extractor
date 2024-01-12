from pydantic.main import BaseModel
from pydantic import create_model, Field
from typing import Type
from ai_extractor.lib.prompting import GPT4ModelMessage
from ai_extractor.lib.helpers import get_client


class DataStructurer:
    """
    Structures the passed information string to the shape of the passed model.
    ```
    """

    def __init__(self, information: str, prompt: GPT4ModelMessage, model: Type[BaseModel]):
        self.__prompt = prompt
        self.__model = model
        self.__client = get_client()
        self.__information: str = information
        self.data = self.__structure_information()

    def __structure_information(self) -> BaseModel:
        """
        Structures the information string extracted by OpenAI in the shape of the passed data model.
        It uses the gpt-4 model for this purpose.
        """

        # Create a model from the passed model class

        dynamic_model_fields = {
            field_name: (field_info, Field(..., alias=field_name))
            for field_name, field_info in self.__model.__annotations__.items()
        }

        dynamic_model = create_model(
            self.__model.__name__,
            **dynamic_model_fields
        )

        details = self.__client.chat.completions.create(
            model="gpt-4",
            response_model=dynamic_model,  # structures the response according to the model
            messages=[self.__prompt.model_dump(mode="json")]
        )

        return details
