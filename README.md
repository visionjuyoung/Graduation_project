# Mic
주제 : 지능형 CCTV를 사용한 요양원 관리  
5 팀 (김민규, 김주영, 박세경)  
트렐로 주소 : https://trello.com/b/DLkKbCis/project  
### 시스템 구성
> ### 하드웨어
> Raspberry Pi 4B 4G
> >사양  
> >프로세서 : Broadcom BCM2711, quad-core Cortex-A72(ARM v8) 64-bit SoC @1.5GHz
> >메모리 : 2GB, 4GB, 8GB LPDDR4  
>
> 라즈베리파이 카메라모듈 V2(RPI 8MP CAMERA BOARD)  
> >사양  
> >이미지 센서 : Sony IMX 219 PQ CMOS image seonsor in a fixed-focus module 
> >방식 : RTSP 서버를 사용하여 IP주소 할당 후 IP카메라 처럼 사용

> ### 소프트웨어  
> 행동인식 및 행동분석
> >종류
> >객체 인식 : YOLO v4
> >행동 인식 : Openpose
> >행동 인식 알고리즘 : BOTTOM-UP방식을 사용하여 다수의 사람 인식
>
> 서버
> >사용 서버 : flask
> >수행 기능 : 행동인식 및 행동분석 알고리즘을 실행하고 APP과 통신
>
> 데이터베이스
> >Firebase 
>
> APP
> > Android 기반 Application
