from django.http import HttpResponse
from django.conf import settings
import zipfile
import os

def inform(check):
    print('flag : {}'.format(check.flag))
    if check.flag == 1:
        check.checker = -1
        check.success = -1
        return HttpResponse("<h1>No Contents to Process</h1>")
    elif check.flag == 2:
        check.checker = 1
        check.success = -1
        return HttpResponse("<h1>Modules are in progress. Try it in a minute.</h1>")
    elif check.flag == 3:
        check.checker = -1
        check.success = 1
        input_dir = os.path.join(settings.BASE_DIR, "input_images")
        response = zip(input_dir)
        return response
    elif check.flag == 4:
        check.checker = -1
        check.success = -1
        response = HttpResponse(open(os.path.join(settings.BASE_DIR, 'photowakeup.zip'), 'rb'),
                                content_type='application/zip')
        response['Content-Disposition'] = 'attachment; filename=photowakeup.zip'
        return response
    else:
        return HttpResponse("<h1>Undefined flag</h1>")


def zip(input_dir):
    file_dir = os.path.join(settings.BASE_DIR, "results")
    zip_name = "photowakeup"
    zip_filename = "{}.zip".format(zip_name)
    zf = zipfile.ZipFile(zip_filename, "w")
    for file in os.listdir(file_dir):
        fdir, fname = os.path.split(file)
        file_path = os.path.join(file_dir, fname)
        zip_path = fname
        zf.write(file_path, zip_path)
        os.remove(file_path)
    zf.close()

    response = HttpResponse(open(os.path.join(settings.BASE_DIR, zip_filename), 'rb'),
                            content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename=photowakeup.zip'
    for file in os.listdir(input_dir):
        os.remove(os.path.join(input_dir, file))

    return response

class Chekcer:
    def __init__(self):
        self.checker = -1
        self.success = -1
        self.flag = -1