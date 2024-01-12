"""
Configurations for Investment Statement extraction.

Contains data models and helper functions for prompts.

Anything specific to Investment Statement prompts or models should be placed here.
"""

from ai_extractor.lib.prompting import GPT4ModelMessage, GPT4VisionModelMessage, MessageTextContent, get_messages_from_images
from pydantic.main import BaseModel
from typing import List, Optional
from PIL import Image


class Holding(BaseModel):
    """
    A model of a generic holding object that might exist in an investment statement.
    """
    name: str
    cost_basis: Optional[str]
    account: Optional[str]


class InvestmentStatementDetail(BaseModel):
    """
    A model of the data we want to extract from a given investment statement.
    """
    account_owner_name: str
    portfolio_value: str
    holdings: List[Holding]


def get_investment_statement_extraction_prompts(images: List[Image.Image]):
    """
    Helper function:

    Creates an array of message objects, appending the images as image_url type messages.
    """

    user_content = [
        MessageTextContent(
            type="text",
            text="""
                            Understand, in detail, all of the information listed in this statement.
                            Create a list of facts for every piece of data or information contained in this statement.
                            """
        ),
        MessageTextContent(
            type="text",
            text="""
                            What is the name of the listed account owner in this statement?
                            """
        ),
        MessageTextContent(
            type="text",
            text="""
                            What is the total portfolio value in this statement?
                            """
        ),
        MessageTextContent(
            type="text",
            text="""
                            What are all of the holdings and their listed cost basis (whether it has one or not) in this statement?
                            Holdings might exist for multiple accounts.
                            """
        )
    ]

    user_content.extend(get_messages_from_images(images))
    return [
        GPT4VisionModelMessage(
            role="system",
            content=[
                MessageTextContent(
                    type="text",
                    text="""
                            You are going to analyze an investment statement and pull out accurate,
                            detailed information from it. Each image is a page from the investment statement.
                            """
                )
            ]
        ),
        GPT4VisionModelMessage(
            role="user",
            content=user_content
        ),
    ]


def get_investment_statement_structure_prompt(information: str):
    """
    Helper function:

    Returns a system message object with the information string appended to it.
    """

    return GPT4ModelMessage(
        role="user",
        content=[
            MessageTextContent(
                type="text",
                text="""
                    Extract
                    - account owner name (The person the account belongs to)
                    - total portfolio value
                    - all holdings (with the name, cost basis - whether it has one or not, and account number)
                    from the following investment statement information json:
                    """ + information
            )
        ]
    )
