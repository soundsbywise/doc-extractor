from pydantic.main import BaseModel
from PIL import Image
from typing import List, Literal, Union
from ai_extractor.lib.helpers import encode_image


class MessageTextContent(BaseModel):
    """
    OpenAI message content model for type "text".
    """
    type: Literal["text"]
    text: str


class ImageURL(BaseModel):
    """
    OpenAI content member "image_url" model..
    """
    url: str


class MessageImageContent(BaseModel):
    """
    OpenAI message content model for type "image_url".
    """
    type: Literal["image_url"]
    image_url: ImageURL


class GPT4VisionModelMessage(BaseModel):
    """
    OpenAI message model for gpt-4-vision-preview model.
    """
    role: Literal['system', 'user']
    content: List[Union[MessageTextContent, MessageImageContent]]


class GPT4ModelMessage(BaseModel):
    """
    OpenAI message model for gpt-4-preview model.
    """
    role: Literal['system', 'user']
    content: List[MessageTextContent]


def get_image_content_for_message(image: Image.Image):
    """
    Helper function:

    Creates a message content object for the passed image.
    """
    encoded_image = encode_image(image=image)
    image_url = f"data:image/jpeg;base64,{encoded_image}"
    return MessageImageContent(type="image_url", image_url=ImageURL(url=image_url))


def get_messages_from_images(images: List[Image.Image]):
    """
    Helper function:

    Creates a list of message content objects for the passed images.
    """
    return [get_image_content_for_message(
        image) for image in images]
