"""
Package n?y khai b?o c?c h?m x? ly file pdf
V? d? nhu; Chuy?n file docx sang pdf, pdf sang h?nh v? ngu?c l?i
"""

from PIL import Image
import img2pdf
from pdf2image import convert_from_path
#from wand.image import Image
import settings
def convert_image_to_pdf(input_file_path, output_file_path):
    """
    Chuy?n d?i file pdf sang file image png
    """
    assert isinstance(input_file_path, str), 'H?nh nhu sai ki?u d? li?u {} ph?i l? ki?u str'.format(input_file_path)
    assert isinstance(output_file_path, str), 'H?nh nhu sai ki?u d? li?u {} ph?i l? ki?u str'.format(input_file_path)

    image = Image.open(input_file_path)
    pdf_bytes = img2pdf.convert(image.filename)
    file = open(output_file_path, "wb")
    file.write(pdf_bytes)
    image.close()


def convert_pdf_to_image(input_file_path, output_file_path):
    """
    Chuy?n d?i file pdf v? image
    """
    assert isinstance(input_file_path, str), 'H?nh nhu sai ki?u d? li?u {} ph?i l? ki?u str'.format(input_file_path)
    assert isinstance(output_file_path, str), 'H?nh nhu sai ki?u d? li?u {} ph?i l? ki?u str'.format(input_file_path)
    try:
        images = convert_from_path(
            pdf_path=input_file_path,
            poppler_path=settings.poppler_path
        )
        for i, image in enumerate(images):
            image.save(output_file_path, "PNG")
            pass
    except Exception as e:
        print(type(e))

