# KETI모비우스 플렛폼 대회 최종코드(화면 깜박이는거 추가)

import threading
import requests
import tkinter as tk
from tkinter import *
import time

con = "" # con 값 초기화
flag = False #blink_background 함수를 한 번만 작동시키기 위한 flag
blink_finished = threading.Event() #blink_background 작업 완료 여부를 알려주는 이벤트 객체

# 무한 반복으로 실행될 함수
def infinite_loop():
    global con
    #Mobius 서버에서 con 값을 가져오기
    while True:
        url = "http://114.71.220.94:7579/Mobius/Canbus_No.7715/CANBUS-01_23/la"
        payload = {}
        headers = {
            'Accept': 'application/json',
            'X-M2M-RI': '12345',
            'X-M2M-Origin': 'S'
        }
        
        response = requests.request("GET", url, headers=headers, data=payload)
        data = response.json()
        con = data["m2m:cin"]["con"]
        

# 멀티스레드 객체 생성 및 시작
my_thread = threading.Thread(target=infinite_loop)
my_thread.start()

# 메인 스레드에서 동시에 실행할 작업
window = tk.Tk()
window.attributes("-fullscreen", True) #전체화면 크기로 설정
window.geometry("{0}x{1}+0+0".format(window.winfo_screenwidth(), window.winfo_screenheight()))
label = Label(window, font=("Helvetica", 36)) #text font: Helvetica, text size: 36
label.pack(expand=True)
label.place(relx=0.5, rely=0.5, anchor=CENTER) #text 스크린 중앙에 배치

#하차벨을 눌렀을 때, 스크린 background 파란색, 빨간색으로 깜빡임
def blink_background(color1, color2, interval, count):
    label.config(text='하차할게요') #screen에 하차할게요 라고 표시
    window.config(bg=color1)
    if count > 0: #count == 0이 될 때까지 blink_background() 반복
        window.after(interval, lambda: blink_background(color2, color1, interval, count -1))
    else:
        window.config(bg = 'lightgray') #count==0이면, 배경색을 다시 lightgray로 바꿈
        blink_finished.set() #blink_background() 완료를 알림.

def route(): #사용자가 어디서 어디까지 가고 싶어하는지 screen에 표시
    label.config(text=con)

def update_label(): #screen에 표시할 내용 select
    global flag
    global con
    
    #사용자가 하차벨을 눌렀을 때
    if con == 'exit' and not flag:
        blink_finished.clear() #blink_ground() 시작을 알림
        blink_background("blue", "red", 500, 20) #화면 깜빡임
        flag = True #flag를 사용하여 blink_background()가 한 번만 동작
    
    #screen에 하차 알림을 보낸 후    
    elif con == 'exit' and flag:
        if blink_finished.is_set(): #blink_ground()가 끝나면 text를 바꿈
            label.config(text='다음 승객을 기다립니다.')
    elif con == "wait" :
        label.config(text="다음 승객을 기다립니다.")
    
    #screen에 출발지와 도착지 표시
    else:
        flag = False
        route()
    
    window.after(1000, update_label)

update_label()

window.mainloop()