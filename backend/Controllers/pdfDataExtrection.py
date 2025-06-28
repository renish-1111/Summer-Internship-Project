import os
import logging
import pdfplumber
from pdf2image import convert_from_path
import pytesseract

# Configure logging
logger = logging.getLogger(__name__)

def pdf_to_text(pdf_path):
    """
    Extract text from PDF with comprehensive error handling and fallback options
    """
    text = ""
    
    try:
        # Validate input
        if not pdf_path:
            logger.error("PDF path is empty or None")
            return ""
        
        if not os.path.exists(pdf_path):
            logger.error(f"PDF file does not exist: {pdf_path}")
            return ""
        
        if not os.path.isfile(pdf_path):
            logger.error(f"Path is not a file: {pdf_path}")
            return ""
        
        # Check file size (optional safety check)
        try:
            file_size = os.path.getsize(pdf_path)
            if file_size == 0:
                logger.error(f"PDF file is empty: {pdf_path}")
                return ""
            if file_size > 50 * 1024 * 1024:  # 50MB limit
                logger.warning(f"PDF file is very large ({file_size} bytes): {pdf_path}")
        except Exception as e:
            logger.warning(f"Could not check file size: {e}")
        
        # Try direct text extraction using pdfplumber
        try:
            with pdfplumber.open(pdf_path) as pdf:
                for page_num, page in enumerate(pdf.pages):
                    try:
                        page_text = page.extract_text()
                        if page_text:
                            text += page_text + "\n"
                    except Exception as e:
                        logger.warning(f"Failed to extract text from page {page_num + 1}: {e}")
                        continue

            if text.strip():
                return text.strip()
            else:
                logger.info("Direct text extraction returned empty text, trying OCR fallback")
                
        except Exception as e:
            logger.error(f"Direct text extraction failed: {e}")

        # Fallback to OCR for image-based PDFs
        logger.info("Attempting OCR fallback for image-based PDF")
        try:
            # Check if pdf2image and pytesseract are available
            try:
                images = convert_from_path(pdf_path)
            except Exception as e:
                logger.error(f"PDF to image conversion failed: {e}")
                return text.strip()
            
            for image_num, image in enumerate(images):
                try:
                    page_text = pytesseract.image_to_string(image)
                    if page_text:
                        text += page_text + "\n"
                except Exception as e:
                    logger.warning(f"OCR failed for image {image_num + 1}: {e}")
                    continue
                    
            if text.strip():
                logger.info(f"OCR extraction successful. Extracted {len(text)} characters")
            else:
                logger.warning("OCR extraction returned empty text")
                
        except Exception as e:
            logger.error(f"OCR fallback failed: {e}")

        # Final validation
        result = text.strip()
        if not result:
            logger.error(f"No text could be extracted from PDF: {pdf_path}")
            
        return result
        
    except Exception as e:
        logger.error(f"Unexpected error in pdf_to_text: {e}")
        return ""