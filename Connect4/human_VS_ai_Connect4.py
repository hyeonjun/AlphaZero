# 커넥트4
# 바닥부터 돌이 쌓이는 4단 틱택토인 '커넥트4'를 구현한다.
# 두 플레이어가 교대로 7 * 6의 보드면에 아래부터 돌을 쌓아 올린다.
# 먼저 가로, 세로, 대각선 방향 중 하나로 4개의 돌을 나란히 놓는 편이 승리.
# 커넥트4 UI의 돌을 놓은 열은 클릭으로 지정.
# 또한, 간이화했으므로 사람은 항상 선 수를 둔다.
# 이전 틱택토의 코드와는 약간의 차이가 있다.
# 게임 상태(game.py)와 게임 UI는 게임 자체가 다르므로 모두 업데이트하고,
# 듀얼 네트워크(dual_network.py)는 파라미터만 업데이터하며,
# 학습 사이클 실행(train_cycle.py)는 베스트 플레이어 평가 부분만을 삭제한다.
from game import State
from pv_mcts import pv_mcts_action
from tensorflow.keras.models import load_model
from pathlib import Path
from threading import Thread
import tkinter as tk

# 게임 UI 정의
class GameUI(tk.Frame):
    # 게임 UI 초기화
    def __init__(self, master=None, model=None):
        tk.Frame.__init__(self, master)
        self.master.title('커넥트4')

        # 게임 상태 생성
        self.state = State()

        # PV MCTS를 활용한 행동 선택을 따르는 함수 생성
        self.next_action = pv_mcts_action(model, 0.0)

        # 캔버스 생성
        self.c = tk.Canvas(self, width=280, height=240, highlightthickness=0)
        self.c.bind('<Button-1>', self.turn_of_human)
        self.c.pack()

        # 그림 갱신
        self.on_draw()

    # 사람의 턴
    def turn_of_human(self, event):
        # 게임 종료 시
        if self.state.is_done():
            self.state = State()
            self.on_draw()
            return

        # 선 수가 아닌 경우
        if not self.state.is_first_player():
            return

        # 클릭 위치를 행동을 변환
        x = int(event.x / 40)
        if x < 0 or 6 < x: # 범위 외
            return
        action = x

        # 둘 수 있는 수가 아닌 경우
        if not (action in self.state.legal_actions()):
            return

        # 다음 상태 얻기
        self.state = self.state.next(action)
        self.on_draw()

        # AI의 턴
        self.master.after(1, self.turn_of_ai)

    # AI의 턴
    def turn_of_ai(self):
        # 게임 종료 시
        if self.state.is_done():
            return

        # 행동 얻기
        action = self.next_action(self.state)

        # 다음 상태 얻기
        self.state = self.state.next(action)
        self.on_draw()

    # 돌 그리기 'draw_piece()'
    # 인수인 'index'는 매스 위치, 'first_player'는 선 수 여부 판단
    # 선 수는 빨간 원, 후 후는 검은 원
    def draw_piece(self, index, first_player):
        x = (index % 7) * 40 + 5
        y = int(index / 7) * 40 + 5
        if first_player:
            self.c.create_oval(x, y, x + 30, y + 30, width=1.0, outline='#FF0000')
        else:
            self.c.create_line(x, y, x + 30, y + 30, width=1.0, fill='#FFFF00')

    # 화면 갱신 'on_draw()'
    # 모든 매스와 돌을 다시 그린다.
    def on_draw(self):
        self.c.delete('all')
        self.c.create_rectangle(0, 0, 280, 240, width=0.0, fill='#00A0FF')
        for i in range(42):
            x = (i % 7) * 40 + 5
            y = int(i / 7) * 40 + 5
            self.c.create_oval(x, y, x+30, y+30, width=1.0, fill='#FFFFFF')
        for i in range(42):
            if self.state.pieces[i] == 1:
                self.draw_piece(i, self.state.is_first_player())
            if self.state.enemy_pieces[i] == 1:
                self.draw_piece(i, not self.state.is_first_player())

# 베스트 플레이어 모델 로드
model = load_model('./model/best.h5')
# 게임 UI 실행
f = GameUI(model=model)
f.pack()
f.mainloop()











