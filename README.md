# NIA2020PhotoWakeUpService
![title](asset/sweetk_photo_wake_up.gif)

## Introduction
한국지능정보사회진흥원(NIA)의 시범서비스 과제로 구축한 Photo wake-up 서비스입니다.

## Git Clone
```sh
git https://github.com/sweetkco/NIA2020PhotoWakeUpService.git
```

## Installation and running
라이브러리 설치
```sh
pip install -r requirements.txt
```
장고 세팅 및 서버 실행
```sh
python manage.py makemigrations
python manage.py migrate
python manage.py runserver 0.0.0.0:{Port} --noreload
```
이미지 업로드
```
http://{ip}:{port}/input_images로 이미지 앞면과 뒷면을 각각 업로드<br>
이미지 형식은 {name}_{front}.jpeg/{name}_{back}.jpeg로 각각 앞면 뒷면을 마킹
```
산출물 다운로드
```
http://{ip}:{port}/photo_wake_up에 접속하면 산출물이 photowakeup.zip으로 다운 받아짐
```

추후 나머지 프로세스 업데이트 예정
```
```
## Inputs
- T포즈에 가까운 1024x1024 이상 사이즈의 고해상도 사람 이미지 앞 뒤(.jpeg)
> 완전히 T포즈의 이미지를 넣을 경우 3d mesh가 불완전하게 형성 될 수 있음.
> 인물 주변에 옷가지들이 들어 있으면 안됨
> 배경은 깨끗할 수록 좋음 

## Outputs
- 3D 인체 mesh(.obj)
- 3d상의 24개 keypoints(.npy)
- 512x512 사이즈의 사람이미지 앞 뒤(.png)

## Citations
```
@article{li2019self,
  title={Self-Correction for Human Parsing},
  author={Li, Peike and Xu, Yunqiu and Wei, Yunchao and Yang, Yi},
  journal={arXiv preprint arXiv:1910.09777},
  year={2019}
}
```
```
@inProceedings{kanazawaHMR18,
  title={End-to-end Recovery of Human Shape and Pose},
  author = {Angjoo Kanazawa
  and Michael J. Black
  and David W. Jacobs
  and Jitendra Malik},
  booktitle={Computer Vision and Pattern Recognition (CVPR)},
  year={2018}
}
```
```
@inproceedings{saito2020pifuhd,
  title={PIFuHD: Multi-Level Pixel-Aligned Implicit Function for High-Resolution 3D Human Digitization},
  author={Saito, Shunsuke and Simon, Tomas and Saragih, Jason and Joo, Hanbyul},
  booktitle={CVPR},
  year={2020}
}
```
```
@inproceedings{osokin2018lightweight_openpose,
    author={Osokin, Daniil},
    title={Real-time 2D Multi-Person Pose Estimation on CPU: Lightweight OpenPose},
    booktitle = {arXiv preprint arXiv:1811.12004},
    year = {2018}
}
```
