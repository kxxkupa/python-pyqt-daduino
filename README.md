# PyQt DADUINO AI CAR
PyQt를 이용하여 아두이노 자동차 제어 프로그램을 구현하였음.

## 🗒 프로그램소개
GUI 프로그램으로 버튼과 키보드 입력을 통해 아두이노 자동차를 조종 가능하게 제작하였음.

## ⏲️ 개발기간
- 2024.11.11 ~ 2024.11.15

## 🧑‍🤝‍🧑 개발자
- 김건우

## 🖥 개발환경
- **Version** : Python 3.10.8
- **IDE** : Visual Studio Code

## ⚙️ 기술스택
- Python
- HTML
- CSS
- JQuery

## 📌 주요기능
1. GUI 프로그램의 버튼과 키보드 입력을 통한 아두이노 자동차의 속도, 방향 제어 가능
2. Haar 버튼을 이용하여 얼굴 검출 기능 ON/OFF
3. LineTracing 버튼을 이용하여 자율주행 기능 ON/OFF
4. YOLO 모델 학습 데이터를 활용한 자율주행 기능 탑재

## ❗사용방법
<img src="https://private-user-images.githubusercontent.com/181185297/386424416-9b9436c3-b8aa-4c47-bd8a-7c5d8a5c6590.jpg?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3MzE2MzUyMTgsIm5iZiI6MTczMTYzNDkxOCwicGF0aCI6Ii8xODExODUyOTcvMzg2NDI0NDE2LTliOTQzNmMzLWI4YWEtNGM0Ny1iZDhhLTdjNWQ4YTVjNjU5MC5qcGc_WC1BbXotQWxnb3JpdGhtPUFXUzQtSE1BQy1TSEEyNTYmWC1BbXotQ3JlZGVudGlhbD1BS0lBVkNPRFlMU0E1M1BRSzRaQSUyRjIwMjQxMTE1JTJGdXMtZWFzdC0xJTJGczMlMkZhd3M0X3JlcXVlc3QmWC1BbXotRGF0ZT0yMDI0MTExNVQwMTQxNThaJlgtQW16LUV4cGlyZXM9MzAwJlgtQW16LVNpZ25hdHVyZT03NDJiZmNlMDY0MGViYmQ2YTUwYjEyYjJlMDZkZTdkYTBkY2FlMDhjODU2NTY4MGE0NmZjNWUwZDk5ZmZiZTk3JlgtQW16LVNpZ25lZEhlYWRlcnM9aG9zdCJ9.im73WqmqddHEvclGyAUaCPNsWWg7F2tYP7l46d3hKVA" alt="daduino_img" style="max-width: 100%;">

1. 자동차에 달린 카메라에서 송출되는 화면
2. 자동차 제어 버튼

**☑ 키보드 제어**
- R : 정지
- W : 전진
- S : 후진
- A : 좌회전
- D : 우회전
- Q : 왼쪽으로 돌기
- E : 오른쪽으로 돌기
- 1 : 속도 40
- 2 : 속도 50
- 3 : 속도 60
- 4 : 속도 80
- 5 : 속도 100
- H : Haar 얼굴 검출 기능 ON/OFF
- L : LineTracing 기능 ON/OFF