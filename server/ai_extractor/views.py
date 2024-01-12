from django.http import HttpResponseBadRequest, HttpRequest, JsonResponse, HttpResponseNotAllowed, HttpResponse
from ai_extractor.lib.helpers import convert_pdf_to_image
from ai_extractor.lib.extractor import Extractor
from ai_extractor.lib.configs.investment_statement import get_investment_statement_extraction_prompts, get_investment_statement_structure_prompt, InvestmentStatementDetail
from ai_extractor.lib.data_structurer import DataStructurer


def extractInvestmentStatement(request: HttpRequest):
    """
    HTTP entrypoint for extracting strucutred data from an uploaded investment statement file.

    The request must be a POST and contain a PDF file.
    """
    if request.method == 'POST' and request.FILES['pdf_file']:
        pdf_file = request.FILES['pdf_file']
        # Case: File is not a PDF
        if not pdf_file.name.endswith("pdf"):
            return HttpResponse("Unsupported media type. Please provide a PDF file.", status=415)

        # convert the pdf pages to images
        images = convert_pdf_to_image(pdf_file)

        # extract the information string
        extracted = Extractor(
            images=images,
            prompts=get_investment_statement_extraction_prompts(images=images)
        )
        # format the information string
        structured = DataStructurer(information=extracted.information,
                                    prompt=get_investment_statement_structure_prompt(
                                        extracted.information),
                                    model=InvestmentStatementDetail
                                    )

        return JsonResponse({"data": structured.data.model_dump(mode="json")})

    # Case: No file provided
    if request.method == 'POST' and not request.FILES['pdf_file']:
        return HttpResponseBadRequest("A PDF file is required.")

    # Case: method is not POST
    return HttpResponseNotAllowed(["POST"])
