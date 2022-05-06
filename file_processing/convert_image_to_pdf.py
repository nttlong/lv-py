from PIL import Image
import img2pdf
from pdf2image import convert_from_path
#from wand.image import Image
import settings
def convert_image_to_pdf(input_file_path, output_file_path):
    """
    Chuyển đổi file image sang pdf
    """
    try:
        assert isinstance(input_file_path, str), 'H?nh nhu sai ki?u d? li?u {} ph?i l? ki?u str'.format(input_file_path)
        assert isinstance(output_file_path, str), 'H?nh nhu sai ki?u d? li?u {} ph?i l? ki?u str'.format(input_file_path)

        image = Image.open(input_file_path)
        pdf_bytes = img2pdf.convert(image.filename)
        file = open(output_file_path, "wb")
        file.write(pdf_bytes)
        image.close()
        return None, output_file_path
    except Exception as e:
        return e,None