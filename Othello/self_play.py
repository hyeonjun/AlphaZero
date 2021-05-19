# 패키지 임포트
from game import State
from pv_mcts import pv_mcts_scores
from dual_network import DN_OUTPUT_SIZE
from datetime import datetime
from tensorflow.keras.models import load_model
from tensorflow.keras import backend as K
from pathlib import Path
import numpy as np
import pickle
import os

# 파라미터 준비
# 'SP_GAME_COUNT'는 셀프 플레이를 수행한 게임 수
# 'SP_TEMPERATURE'는 볼츠만 분포의 온도 파라미터다.
SP_GAME_COUNT = 500 # 오리지널은 25,000
SP_TEMPERATURE = 1.0

# 선 수를 둔 플레이어의 가치
# 'first_play_value(ended_state)'는 최종 국면으로부터 선 수를 둔 플레이어의 가치를
# 계산한다. 선 수를 둔 플레이어가 승리한 경우 1, 패배한 경우 -1, 무승부를 한 경우는 0을 반환.
def first_play_value(ended_state):
    if ended_state.is_lose():
        return -1 if ended_state.is_first_player() else 1
    return 0

# 학습 데이터 저장
def write_data(history):
    now = datetime.now()
    os.makedirs('./data/', exist_ok=True) # 폴더가 없는 경우에는 생성
    path = './data/{:04}{:02}{:02}{:02}{:02}{:02}.history'.format(
        now.year, now.month, now.day, now.hour, now.minute, now.second)
    with open(path, mode='wb') as f:
        # pickle이란 Python 객체를 파일에 보전하고 다시 불러오는데 필요한 패키지.
        # 'with open(path, mode='wb') as f'로 파일을 열고,
        # 'pickle.dump(객체, f)'로 Python 객체를 저장.
        pickle.dump(history, f)

# 게임 실행
def play(model):
    # 학습 데이터
    history = []

    # 상태 생성
    state = State()

    while True:
        # 게임 종료 시
        if state.is_done():
            break

        # 둘 수 있는 수의 확률 분포 얻기
        scores = pv_mcts_scores(model, state, SP_TEMPERATURE)

        # 학습 데이터에 상태와 정책 추가
        policies = [0] * DN_OUTPUT_SIZE
        for action, policy in zip(state.legal_actions(), scores):
            policies[action] = policy
        history.append([[state.pieces, state.enemy_pieces], policies, None])

        # 행동 얻기
        action = np.random.choice(state.legal_actions(), p=scores)

        # 다음 상태 얻기
        state = state.next(action)

    # 학습 데이터에 가치 추가
    value = first_play_value(state)
    for i in range(len(history)):
        history[i][2] = value
        value = -value
    return history

# 셀프 플레이 실행
# 'self_play()'는 셀프 플레이를 실행한다.
# 먼저, 베스트 플레이어 모델을 로드해서 SP_GAME_COUNT의 횟수만큼 게임을 실행.
# 마지막에 수집한 학습 데이터를 저장하고, 모델의 세션과 메모리를 파기한다.
def self_play():
    # 학습 데이터
    history = []

    # 베스트 플레이어 모델 로드
    model = load_model('./model/best.h5')

    # 여러 차례 게임 실행
    for i in range(SP_GAME_COUNT):
        # 게임 실행
        h = play(model)
        history.extend(h)

        # 출력
        print('\rSelfPlay {}/{}'.format(i + 1, SP_GAME_COUNT), end='')
    print('')

    # 학습 데이터 저장
    write_data(history)

    # 모델 삭제
    K.clear_session()
    del model

# 동작 확인 정의
# self_play() 실행만 수행한다.
# 셀프 플레이가 완료되면 data 폴더에 '학습 데이터(*.history)'가 생성된다.
if __name__ == '__main__':
    self_play()
