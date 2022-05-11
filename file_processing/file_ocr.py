import ocrmypdf
import settings
import subprocess
import os
import shutil
def run_ocrmypdf(in_put, out_put):
    try:
        # ocrmypdf.configure_logging(
        #     verbosity=ocrmypdf.Verbosity(
        #         1
        #     ),
        #
        # )
        ret =ocrmypdf.api.ocr(
            input_file=in_put,
            output_file= out_put,
            use_threads =True,
            language= settings.lang_processing,
            progress_bar= False

        )
        # cmd = ["ocrmypdf", "--deskew", in_put, out_put]
        # settings.logger.info(cmd)
        # proc = subprocess.Popen(
        #     cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        # result = proc.stdout.read()
        # if proc.returncode == 6:
        #     """
        #     Skipped document because it already contained text
        #     """
        #     shutil.move(in_put, out_put)
        #     return None, result
        # elif proc.returncode == 0:
        #     settings.logger.info(result)
        #     return None, result
        # # elif not proc.returncode:
        # #     settings.logger.info(result)
        # #     return Exception(result), None
        # if not os.path.isfile(out_put):
        #     shutil.move(in_put,out_put)
        # return None, result
    except ocrmypdf.PdfMergeFailedError as e:
        return  e,None
    except ocrmypdf.MissingDependencyError as e:
        """
        Lỗi thiếu các phần mềm hỗ trợ
        """
        return  Exception("Missing some program to process {}".format(e.message)),None
    except ocrmypdf.UnsupportedImageFormatError as e:
        """
        Lỗi không xác định đươc ảnh bỏ qua
        """
        return  None,None
    except ocrmypdf.OutputFileAccessError as e:
        """
        Lỗi phân quyền không truy cập được file đầu vào
        """
        return e, None
    except ocrmypdf.PriorOcrFoundError as e:
        """
        File đầu vào đã thực hiện OCR rồi bỏ qua
        """
        return None, None
    except ocrmypdf.InputFileError as e:
        """
        File đều vào bị lỗi bỏ qua
        """
        return None, None
    except ocrmypdf.SubprocessOutputError as e:
        return Exception("Error during file processing {}".format(e.message)),None
    except ocrmypdf.EncryptedPdfError  as e:
        return Exception("Input file '{}' is proctected ".format(in_put)), None
    except ocrmypdf.TesseractConfigError as e:
        """
        Cấu hình Tesseract  không đúng
        """
        return e, None

    except Exception as e:
        return e, None
    """
    PriorOcrFoundError('page already has text! - aborting (use --force-ocr to force OCR;  see also help for the arguments --skip-text and --redo-ocr')
    """
    # ret = ocrmypdf.ocr(
    #     input_file=in_put,
    #     output_file=out_put,
    #     language=settings.lang_processing,
    #     force_ocr= True,
    #     use_threads=True,
    #     tesseract_timeout=2 * 60 * 60,
    #     progress_bar=True,
    #     deskew=True
    # )
    return None, ret