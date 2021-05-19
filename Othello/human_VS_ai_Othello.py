# 패키지 임포트
from game import State
from pv_mcts import pv_mcts_action
from tensorflow.keras.models import load_model
from pathlib import Path
from threading import Thread
import tkinter as tk

# 베스트 플레이어 모델 로드
model = load_model('./model/best.h5')

# 게임 UI 정의
class GameUI(tk.Frame):
    # 초기화
    def __init__(self, master=None, model=None):
        # 게임 상태와 PV MCTS로 행동 선택을 수행하는 함수와 캔버스를 준비
        # 마지막으로 화면을 갱신해 초기 화면을 표시한다.
        tk.Frame.__init__(self, master)
        self.master.title('오셀로')

        # 게임 상태 생성
        self.state = State()

        # PV MCTS를 활용한 행동을 선택하는 함수 생성
        self.next_action = pv_mcts_action(model, 0.0)

        # 캔버스 생성
        self.c = tk.Canvas(self, width=240, height=240, highlightthickness=0)
        self.c.bind('<Button-1>', self.turn_of_human)
        self.c.pack()

        # 화면 갱신
        self.on_draw()

    # 사람의 턴
    def turn_of_human(self, event):
        # 게임 종료 시 게임 초기 상태로 되돌림
        if self.state.is_done():
            self.state = State()
            self.on_draw()
            return

        # 선 수가 아닌 경우에는 조작 불가로 처리
        if not self.state.is_first_player():
            return

        # 클릭 위치를 행동으로 변환
        # 클릭 위치에서 행동(매스 번호)으로 변환한다.
        # 둘 수 있는 수가 패스 밖에 없는 경우에는 패스(36)를 지정한다.
        x = int(event.x / 40)
        y = int(event.y / 40)
        if x < 0 or 5 < x or y < 0 or 5 < y: # 범위 외
            return
        action = x + y * 6

        # 합법적인 수가 아닌 경우
        legal_actions = self.state.legal_actions()
        if legal_actions == [36]:
            action = 36 # 패스
        # 클릭 위치에서 반환한 행동이 둘 수 있는 수가 아닌 경우 아무 처리도 하지 않음
        if action != 36 and not (action in legal_actions):
            return

        # 다음 상태 얻기
        self.state = self.state.next(action)
        self.on_draw()

        # AI의 턴
        self.master.after(1, self.turn_of_ai)

    # AI의 턴
    def turn_of_ai(self):
        # 게임 종료 시 게임 상태를 초기 상태로 되돌린다.
        if self.state.is_done():
            return

        # 듀얼 네트워크로 행동을 취득
        action = self.next_action(self.state)

        # 취득한 행동에 따라 다음 상태를 취득하고, 화면을 갱신한다.
        self.state = self.state.next(action)
        self.on_draw()

    # 돌 그리기
    def draw_piece(self, index, first_player):
        x = (index % 6) * 40 + 5
        y = index // 6 * 40 + 5
        if first_player:
            self.c.create_oval(x, y, x+30, y+30, width=1.0, outline='#000000', fill='#C2272D')
        else:
            self.c.create_oval(x, y, x+30, y+30, width=1.0, outline='#000000', fill='#FFFFFF')

    # 화면 갱신
    def on_draw(self):
        self.c.delete('all')
        self.c.create_rectangle(0,0,240,240,width=0.0, fill='#C69C6C')
        for i in range(1, 8):
            self.c.create_line(0,i*40,240,i*40, width=1.0, fill='#000000')
            self.c.create_line(i*40,0,i*40,240, width=1.0, fill='#000000')
        for i in range(36):
            if self.state.pieces[i] == 1:
                self.draw_piece(i, self.state.is_first_player())
            if self.state.enemy_pieces[i] == 1:
                self.draw_piece(i, not self.state.is_first_player())

# 게임 UI 실행
f = GameUI(model=model)
f.pack()
f.mainloop()