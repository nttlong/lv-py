import docx2pdf
import settings
# docx2pdf.convert(
#     r'\\192.168.18.36\Share\TaiLieu\FilesServices.docx',
#     r'C:\BFS\LVCore2021\lv.Web\python\ocr\tes-result\FilesServices.pdf'
# )
# import module
from pdf2image import convert_from_path


# Store Pdf with convert_from_path function
images = convert_from_path(
    pdf_path=r'\\192.168.18.36\Share\test002.pdf',
    poppler_path= settings.poppler_path

)
images[0].save(r'C:\BFS\LVCore2021\lv.Web\python\ocr\tes-result\test002.png', 'PNG')
# for i in range(len(images)):
#
# 	# Save pages as images in the pdf
# 	images[i].save('page'+ str(i) +'.jpg', 'JPEG')
