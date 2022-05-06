import ocrmypdf
import settings
import subprocess
import os
import shutil
def run_ocrmypdf(in_put, out_put):
    try:
        cmd = ["ocrmypdf", "--deskew", in_put, out_put]
        settings.logger.info(cmd)
        proc = subprocess.Popen(
            cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        result = proc.stdout.read()
        if proc.returncode == 6:
            """
            Skipped document because it already contained text
            """
            shutil.move(in_put, out_put)
            return None, result
        elif proc.returncode == 0:
            settings.logger.info(result)
            return None, result
        # elif not proc.returncode:
        #     settings.logger.info(result)
        #     return Exception(result), None
        if not os.path.isfile(out_put):
            shutil.move(in_put,out_put)
        return None, result
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
    # return None, ret