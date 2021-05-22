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
>
> Arduino Uno
> >방식 : 시리얼 통신을 사용하여 서버와 통신 후 결과 값에 따라 난간 제어

> ### 소프트웨어  
> 행동인식 및 행동분석
> >종류
> >객체 인식 : YOLO v4
> >행동 인식 : Openpose   
> >행동 인식 알고리즘 : BOTTOM-UP방식을 사용하여 다수의 사람 인식
>
> 서버
> >사용 서버 : flask   
> >수행 기능 : 행동인식 및 행동분석 알고리즘을 실행하고 APP과 통신, 아두이노(난간) 제어
>
> 데이터베이스
> >Firebase 
>
> APP
> > Android 기반 Application

### 프로세스
> 스트리밍
> > RTSP서버를 할당한 IP CAM을 이용하여 CAM에서 서버 운용 컴퓨터로 영상 데이터 전송
>
> 영상 분석
> > flask 서버에서 CAM으로 부터 받은 데이터를 기반으로 OPENPOSE 동작
> > math 함수를 기반으로 한 자세 추정
>
> 서버-아두이노 통신
> > 시리얼 통신을 이용하여 서버와 아두이노간 통신
> > 낙상의 위험이 없는 경우 0을 전송 낙상의 위험이 있는 경우 1을 전송
> 
> 아두이노 동작
> > 낙상의 위험이 있는 경우(시리얼 통신상 1의 값) 서보모터가 동작하여 난간이 동작
>
> 화면 캡쳐
> > 1분의 간격으로 화면을 캡쳐하고 서버 컴퓨터에 저장
> 
> 안드로이드 APP
> > 안드로이드 어플로 캡쳐된 화면을 확인 할 수 있음
