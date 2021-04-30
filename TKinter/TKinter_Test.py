# TKinter는 파이썬에서 GUI를 작성하는 패키지이며, Python 3.x.x에 표준으로 표함되어 있다.

# 화면 초기화
# 'Canvas'의 'delete('all')'을 사용.

# 그래픽 그리기
# 'Canvas'의 메소드 사용.

# 이미지 로드
# Image.open()을 사용. 여기에 ImageTK.PhotoImage()를 사용해 'PhotoImage'로 변환.
# 다른 한 장은 Image의 rotate(180)을 사용해 180도 회전시킨다.

# 이벤트 처리
# 이벤트 연결은 'bind(이벤트 정수, 함수)'를 사용한다.
# 이번에는 왼쪽 마우스 버튼을 눌렀을 때 on_click()을 호출한다.
# 마우스 왼쪽 버튼을 눌렀을 때의 이벤트 정의는 <Button-1>이다.
# 알림 대상 함수 event의 event.x에 클릭한 위치의 x 좌표,
# event.y에 클릭한 위치의 y좌표가 전달된다.

import tkinter as tk
from PIL import Image, ImageTk
# UI 생성
class TKinterUI(tk.Frame):
    # 초기화
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)

        # 타이틀 표시
        self.master.title('Graphic')

        # 캔버스 생성
        self.c = tk.Canvas(self, width=240, height=240, highlightthickness=0)
        self.c.bind('<Button-1>', self.on_click)  # 클릭 판정 추가
        self.c.pack()

        # 그림 화면
        # self.on_draw()

        # 이미지 로드
        image = Image.open('sample.png')
        self.images = []
        self.images.append(ImageTk.PhotoImage(image))
        self.images.append(ImageTk.PhotoImage(image.rotate(180)))
        # self.on_image() # 이미지 나타내기

        # 클릭 위치
        self.x = 0
        self.y = 0

        # 이벤트 화면
        self.on_screen()

    # 그림 갱신
    def on_draw(self):
        # 그림 클리어
        self.c.delete('all') # 화면 초기화

        # 라인 그리기
        self.c.create_line(10, 30, 230, 30, width=2.0, fill='#FF0000')

        # 원 그리기
        self.c.create_oval(10, 70, 50, 110, width=2.0, outline='#00FF00')

        # 원 채우기
        self.c.create_oval(70, 70, 110, 110, width=2.0, fill='#00FF00')

        # 직사각형 그리기
        self.c.create_rectangle(10, 130, 50, 170, width=2.0, outline='#00A0FF')

        # 직사각형 채우기기
        self.c.create_rectangle(70, 130, 110, 170, width=2.0, fill='#00A0FF')

        # 문자열 표시
        self.c.create_text(10, 200, text='진이씨', font='courier 20', anchor=tk.NW)

    # 이미지 갱신
    def on_image(self):
        self.c.delete('all')  # 화면 초기화

        # 이미지 그리기
        self.c.create_image(10, 10, image=self.images[0], anchor=tk.NW)

        # 반번 이미지 그리기
        self.c.create_image(10, 100, image=self.images[1], anchor=tk.NW)

    # 좌표 화면 생성
    def on_screen(self):
        # 화면 초기화
        self.c.delete('all')

        # 문자열(좌표) 표시
        str = '클릭 위치 {}, {}'.format(self.x, self.y)
        self.c.create_text(10, 10, text=str, font='courier 16', anchor=tk.NW)

    # 클릭 시 호출
    def on_click(self, event):
        self.x = event.x
        self.y = event.y
        self.on_screen()

# UI실행
f = TKinterUI()
f.pack()
f.mainloop()