from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from .models import Post,PhotoWakeUp
from django.conf import settings
from .utils import *
import os

# Create your views here.

@csrf_exempt
def upload(request):
    if request.method == "POST":
        post = Post()
        print(request.FILES)
        if request.FILES:
            post.image = request.FILES['uploadFile']
            try:
                post.save()
                print("saved file name : {}".format(post.image))
                return HttpResponse("Sucessfully Uploaded")
            except Exception as e:
                print("Failed to upload")
                return HttpResponse("Failed Error at {}".format(e))

        else:
            return HttpResponse("There is no file to upload")

def recon_3d():
    pwu = PhotoWakeUp()
    print("Seg1 Start")
    pwu.pwu.PoseEstimation()
    print("3D Start")
    pwu.pwu.Reconstruction()
    print("KeyPoints Start")
    pwu.pwu.KeyPoints()
    print("Seg2 Start")
    pwu.pwu.Segmentation()
    print("Complete")


check = Chekcer()


@csrf_exempt
def download(request):
    #if request.method == "POST":
    print("CHECKER :{}".format(check.checker))

    # if 'photowakeup.zip' in os.listdir(settings.BASE_DIR):
    #     if check.success == -1:
    #         os.remove(os.path.join(settings.BASE_DIR,'photowakeup.zip'))
    #     else:
    #         check.flag = 4
    #         return inform(check)

    if check.checker == -1:
        input_dir = os.path.join(settings.BASE_DIR, "input_images")
        print(input_dir)
        check.checker = 1
        try:
            size = len(os.listdir(input_dir))
            print('size : {}'.format(size))
            if size == 0:
                check.flag = 1
            else:
                recon_3d()
                check.flag = 3
        except:
            print("HERE")
            check.flag = 1
    else:
            check.flag = 2

    return inform(check)







