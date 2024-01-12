from PIL import Image
from typing import List

from ai_extractor.lib.prompting import GPT4VisionModelMessage
from ai_extractor.lib.helpers import get_client


class Extractor:
    """
    Extracts data from the passed array of images into a string.
    """

    def __init__(self, images: list[Image.Image], prompts: List[GPT4VisionModelMessage]):
        self.__prompts = prompts
        self.__client = get_client()
        self.images: list[Image.Image] = images
        self.information: str = self.__extract_information()

    def __extract_information(self) -> str:
        """
        Calls the OpenAI API to extract information from the passed images.
        """
        messages = [prompt.model_dump(mode="json")
                    for prompt in self.__prompts]
        response = self.__client.chat.completions.create(
            model="gpt-4-vision-preview",
            messages=messages,
            max_tokens=2000,
        )

        return response.choices[0].message.content
