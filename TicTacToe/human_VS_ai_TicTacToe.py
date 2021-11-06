# 패키지 임포트
from game import State
from pv_mcts import pv_mcts_action
from tensorflow.keras.models import load_model
import tkinter as tk

"""
### 사람의 턴 처리 'turn_of_human()' ###
1. 게임이 종료되는 경우
 - 게임이 종료되는 경우에는 게임 상태를 초기 상태로 되돌림.

2. 선 수가 아닌 경우
 - 선 수가 아닌 경우(AI의 턴일 때) 사람은 조작할 수 없다.

3. 클릭 위치를 행동으로 변환
 - 클릭 위치로부터 행동(매스 번호)으로 변환한다. 

4. 둘 수 있는 수가 아닌 경우
 - 클릭 위치의 XY 좌표로부터 행동으로 변환하고, 그 행동이 둘 수 있는 수가 아닌 경우에는
   처리하지 않도록 한다.

5. 다음 상태 취득
 - 둘 수 있는 수의 경우에는 state.next()로 다음 상태를 취득하고, 화면을 갱신한다.

6. AI 턴으로 변경
 - 사람의 턴이 완료되면 AI의 턴으로 변경한다.
 - 직접 turn_of_ai()를 호출하면 AI 턴이 종료될 때까지 사람의 턴으로 화면 갱신(5.)이
   적용되지 않기 때문에 master.after()로 1밀리초 슬립을 한 뒤 호출한다.
   
### AI의 턴 처리 'turn_of_ai()' ###
1. 게임 종료 시
 - 게임 종료 시에는 아무런 처리를 하지 않는다.

2. 행동 취득
 - 뉴럴 네트워크에서 행동을 취득한다.
 
3. 다음 상태 취득
 - 취득한 행동에 따라 다음 상태를 취득한다. 그리고 화면 갱신
"""

# 게임 UI 정의
class GameUI(tk.Frame):
    # 게임 UI 초기화
    def __init__(self, master=None, model=None):
        tk.Frame.__init__(self, master)
        self.master.title('틱택토')

        # 게임 상태 생성
        self.state = State()

        # PV MCTS를 활용한 행동 선택을 따르는 함수 생성
        self.next_action = pv_mcts_action(model, 0.0)

        # 캔버스 생성
        self.c = tk.Canvas(self, width=240, height=240, highlightthickness=0)
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
        x = int(event.x / 80)
        y = int(event.y / 80)
        if x < 0 or 2 < x or y < 0 or 2 < y: # 범위 외
            return
        action = x + y * 3

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
    # 인수인 'index'는 매스 위치, 'first_player'는 누가 선수를 두는가다.
    # 선 수는 o, 후 수는 x
    def draw_piece(self, index, first_player):
        x = (index % 3) * 80 + 10
        y = int(index / 3) * 80 + 10
        if first_player:
            self.c.create_oval(x, y, x + 60, y + 60, width=2.0, outline='#FFFFFF')
        else:
            self.c.create_line(x, y, x + 60, y + 60, width=2.0, fill='#5D5D5D')
            self.c.create_line(x + 60, y, x, y + 60, width=2.0, fill='#5D5D5D')

    # 화면 갱신 'on_draw()'
    # 모든 매스와 돌을 다시 그린다.
    def on_draw(self):
        self.c.delete('all')
        self.c.create_rectangle(0, 0, 240, 240, width=0.0, fill='#00A0FF')
        self.c.create_line(80, 0, 80, 240, width=2.0, fill='#0077BB')
        self.c.create_line(160, 0, 160, 240, width=2.0, fill='#0077BB')
        self.c.create_line(0, 80, 240, 80, width=2.0, fill='#0077BB')
        self.c.create_line(0, 160, 240, 160, width=2.0, fill='#0077BB')
        for i in range(9):
            if self.state.pieces[i] == 1:
                self.draw_piece(i, self.state.is_first_player())
            if self.state.enemy_pieces[i] == 1:
                self.draw_piece(i, not self.state.is_first_player())





# 베스트 플레이어 모델 로드
model = load_model('model/best.h5')
# 게임 UI 실행
f = GameUI(model=model)
f.pack()
f.mainloop()