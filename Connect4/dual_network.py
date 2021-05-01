# 패키지 임포트
from tensorflow.keras.layers import Activation, Add, BatchNormalization, Conv2D, Dense, GlobalAveragePooling2D, Input
from tensorflow.keras.models import Model
from tensorflow.keras.regularizers import l2
from tensorflow.keras import backend as K
import os

# dual_network.py(파라미터만 갱신)
# 'dual_network.py'에서는 듀얼 네트워크의 파라미터를 갱신한다. 
# 입력 형태는 (7, 6, 2), 행동 수는 7이다.
DN_FILTERS = 128 # 컨볼루셔널 레이어 커널 수(오리지널 256)
DN_RESIDUL_NUM = 16 # 레지듀얼 블록 수(오리지널 19)
DN_INPUT_SHAPE = (7, 6, 2) # 입력 형태
DN_OUTPUT_SIZE = 7 # 행동 수(배치 수(7))

# 컨볼루셔널 레이어 생성
# conv(filters)로 ResNet의 컨볼루셔널 레이어를 생성한다.
def conv(filters):
    return Conv2D(filters, 3, padding='same', use_bias=False, kernel_initializer='he_normal', kernel_regularizer=l2(0.0005))

# 레지듀얼 블록 생성
# residual_block()으로 ResNet의 레지듀얼 블록을 생성한다.
def residual_block():
    def f(x):
        sc = x
        x = conv(DN_FILTERS)(x)
        x = BatchNormalization()(x)
        x = Activation('relu')(x)
        x = conv(DN_FILTERS)(x)
        x = BatchNormalization()(x)
        x = Add()([x, sc])
        x = Activation('relu')(x)
        return x
    return f

# 듀얼 네트워크 생성
def dual_network():
    # 모델 생성이 완료된 경우 처리하지 않음
    if os.path.exists('./model/best.h5'):
        return

    # 입력 레이어
    input = Input(shape=DN_INPUT_SHAPE)

    # 컨볼루셔널 레이어
    x = conv(DN_FILTERS)(input)
    x = BatchNormalization()(x)
    x = Activation('relu')(x)

    # 레지듀얼 블록 x 16
    for i in range(DN_RESIDUL_NUM):
        x = residual_block()(x)

    # 풀링 레이어
    x = GlobalAveragePooling2D()(x)

    # 정책 출력
    p = Dense(DN_OUTPUT_SIZE, kernel_regularizer=l2(0.0005),
              activation='softmax', name='pi')(x)

    # 가치 출력
    v = Dense(1, kernel_regularizer=l2(0.0005))(x)
    v = Activation('tanh', name='v')(v)

    # 모델 생성
    model = Model(inputs=input, outputs=[p,v])

    # 모델 저장
    os.makedirs('./model/', exist_ok=True) # 폴더가 없는 경우 생성
    model.save('./model/best.h5') # 베스트 플레이어 생성

    # 모델 삭제
    K.clear_session()
    del model

# 동작 학인
# create_dual_network()의 실행만을 수행한다. 이를 통해 model 폴더에 베스트 플레이어 모델(./model/best/h5)이 생성된다.
if __name__ == '__main__':
    dual_network()


























