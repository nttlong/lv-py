import os.path
import os
import aspose.words as aw

def convert(in_put, out_put):
    assert isinstance(in_put,str),'in_put must be str'
    assert isinstance(out_put,str),'out_put must be str'
    doc = aw.Document(in_put)

    # set output image format
    options = aw.saving.ImageSaveOptions(aw.SaveFormat.PNG)

    # loop through pages and convert them to PNG images
    for pageNumber in range(doc.page_count):
        options.page_set = aw.saving.PageSet(pageNumber)
        path_to = os.path.join(out_put,str(pageNumber + 1) + "_page.png")
        doc.save(path_to, options)