import os
from dotenv import load_dotenv
from crewai_tools import tool

import pdfplumber
from PIL import Image
import pytesseract

load_dotenv()

@tool("Read Financial PDF")
def read_pdf_tool(file_path: str = "data/sample.pdf") -> str:
    """
    Extracts text from a financial PDF document. Uses direct text extraction first,
    and falls back to OCR if no readable text is found.
    """
    try:
        with pdfplumber.open(file_path) as pdf:
            text = "\n".join(
                page.extract_text() for page in pdf.pages if page.extract_text()
            )
        if text.strip():
            return text
        else:
            ocr_text = ""
            for page in pdf.pages:
                image = page.to_image(resolution=300).original
                ocr_text += pytesseract.image_to_string(image)
            return ocr_text if ocr_text.strip() else "No readable text found in the PDF."
    except Exception as e:
        return f"Error reading PDF: {str(e)}"


@tool("Analyze Investment Data")
def analyze_investment_tool(financial_document_data: str) -> str:
    """
    Cleans and prepares financial document data for investment analysis.
    Placeholder for actual logic.
    """
    try:
        processed_data = financial_document_data
        i = 0
        while i < len(processed_data):
            if processed_data[i:i+2] == "  ":
                processed_data = processed_data[:i] + processed_data[i+1:]
            else:
                i += 1
        # TODO: Implement actual investment analysis logic
        return "Investment analysis functionality to be implemented"
    except Exception as e:
        return f"Error during investment analysis: {str(e)}"


@tool("Create Risk Assessment")
def create_risk_assessment_tool(financial_document_data: str) -> str:
    """
    Placeholder for risk assessment logic based on financial document data.
    """
    try:
        # TODO: Implement actual risk assessment logic
        return "Risk assessment functionality to be implemented"
    except Exception as e:
        return f"Error during risk assessment: {str(e)}"
