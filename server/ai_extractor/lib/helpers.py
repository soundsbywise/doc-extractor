"""
Helper functions for the extractor library.
"""
import base64
from io import BytesIO
from django.core.files.uploadedfile import UploadedFile
from pdf2image import convert_from_bytes
import tempfile
from PIL import Image
from openai import OpenAI
import instructor


def convert_pdf_to_image(pdf_file: UploadedFile):
    """
    Converts the passed PDF file to a list of `PIL.Image` objects.

    Note: A single PDF file can have multiple image outputs depending on the number of pages in the PDF.
    """
    file_bytes = pdf_file.file.read()
    with tempfile.TemporaryDirectory() as out_put:
        return convert_from_bytes(
            file_bytes, output_folder=out_put)


def encode_image(image: Image.Image):
    """
    Base64 encode the passed image and return it as a decoded string.
    This method is used to prepare images for sending to the OpenAI API.
    """
    buffered = BytesIO()
    image.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode('utf-8')


def get_client():
    """
    Patches the openAI SDK with Instructor, enabling the OpenAI API to parse
    the extracted data into structured data objects.

    More info on Instructor: https://jxnl.github.io/instructor/
    """
    return instructor.patch(OpenAI())
