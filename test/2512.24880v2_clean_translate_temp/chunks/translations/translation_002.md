## Translation Output

### Translated Text

**2.2. 거시적 설계**

거시적 설계(Macro-design)는 네트워크의 전역 토폴로지를 관장한다 (Srivastava et al., 2015). ResNet (He et al., 2016a)을 따라, DenseNet (Huang et al., 2017) 및 FractalNet (Larsson et al., 2016)과 같은 아키텍처들은 각각 조밀한 연결성과 다중 경로 구조를 통해 토폴로지 복잡도를 증가시킴으로써 성능 향상을 목표로 하였다. Deep Layer Aggregation (DLA) (Yu et al., 2018)은 다양한 깊이와 해상도에 걸쳐 특징을 재귀적으로 집계함으로써 이 패러다임을 더욱 확장하였다.

보다 최근에는 거시적 설계의 초점이 잔차 스트림(residual stream)의 폭을 확장하는 방향으로 이동하였다 (Chai et al., 2020; Fang et al., 2023; Heddes et al., 2025; Mak and Flanigan, 2025; Menghani et al., 2025; Pagliardini et al., 2024; Xiao et al., 2025; Xie et al., 2023; Zhu et al., 2024). 하이퍼 연결(Hyper-Connections, HC) (Zhu et al., 2024)은 다양한 깊이의 특징들 간의 연결 강도를 조절하기 위해 학습 가능한 행렬을 도입하였으며, Residual Matrix Transformer (RMT) (Mak and Flanigan, 2025)는 특징 저장을 용이하게 하기 위해 표준 잔차 스트림을 외적 메모리 행렬로 대체하였다. 유사하게, MUDDFormer (Xiao et al., 2025)는 계층 간 정보 흐름을 최적화하기 위해 다방향 동적 밀집 연결을 사용한다. 이러한 접근법들의 잠재력에도 불구하고, 이들은 잔차 연결의 고유한 항등 사상(identity mapping) 특성을 훼손하여 불안정성을 야기하고 확장성을 저해한다. 더욱이, 이들은 확장된 특징 폭으로 인해 상당한 메모리 접근 오버헤드를 발생시킨다. HC를 기반으로 구축된 제안된 _m_HC는 잔차 연결 공간을 특정 매니폴드 위로 제한하여 항등 사상 특성을 복원하는 동시에, 효율성을 보장하기 위한 엄격한 인프라 최적화를 통합한다. 이 접근법은 확장된 연결의 토폴로지적 이점을 유지하면서 안정성과 확장성을 향상시킨다.

#### **3. 예비 지식**

먼저 본 연구에서 사용되는 표기법을 확립한다. HC 공식화에서, _𝑙_-번째 층의 입력 **x**_𝑙_ ∈ **R**[1][×]_[𝐶]_는 _𝑛_배로 확장되어 은닉 행렬 **x**_𝑙_ = (**x**[⊤]_𝑙_,0[,] _[. . .]_ [,] **[x]**[⊤]_𝑙_, _𝑛_−1[)][⊤] [∈] **[R]**_[𝑛]_ [×] _[𝐶]_를 구성한다.

이는 _𝑛_-스트림 잔차로 볼 수 있다. 이 연산은 잔차 스트림의 폭을 효과적으로 확장한다. 이 스트림의 읽기, 쓰기 및 업데이트 과정을 관장하기 위해, HC는 세 개의 학습 가능한 선형 사상—H_𝑙_[pre], H_𝑙_[post] ∈ **R**[1][×]_[𝑛]_, 그리고 H_𝑙_[res] ∈ **R**_[𝑛]_ [×] _[𝑛]_—을 도입한다. 이러한 사상들은 식 (1)에 표시된 표준 잔차 연결을 수정하여 식 (3)에 주어진 공식을 생성한다.

HC 공식화에서, 학습 가능한 사상들은 두 부분의 계수로 구성된다: 입력 의존적 계수와 전역 계수이며, 이들은 각각 동적 사상(dynamic mappings)과 정적 사상(static mappings)으로 지칭된다. 형식적으로, HC는 계수를 다음과 같이 계산한다:




**x**˜_𝑙_ = RMSNorm(**x**_𝑙_)
H_𝑙_[pre] = _𝛼_[pre]_𝑙_ - tanh(_𝜃𝑙_[pre] **x**˜[⊤]_𝑙_ [) +] **[b]**[pre]_𝑙_
H_𝑙_[post] = _𝛼_[post]_𝑙_ - tanh(_𝜃𝑙_[post] **x**˜[⊤]_𝑙_ [) +] **[b]**[post]_𝑙_
H_𝑙_[res] = _𝛼_[res]_𝑙_ - tanh(_𝜃𝑙_[res] **x**˜[⊤]_𝑙_ [) +] **[b]**[res]_𝑙_[,]

(5)

여기서 RMSNorm(·) (Zhang and Sennrich, 2019)은 마지막 차원에 적용되며, 스칼라

_𝛼_[pre]_𝑙_, _𝛼_[post]_𝑙_ 그리고 _𝛼_[res]_𝑙_ ∈ **R**는 작은 값으로 초기화되는 학습 가능한 게이팅 인자이다. 동적

5

사상들은 _𝜃𝑙_[pre], _𝜃𝑙_[post] ∈ **R**[1][×]_[𝐶]_ 및 _𝜃𝑙_[res] ∈ **R**_[𝑛]_ [×] _[𝐶]_로 매개변수화된 선형 투영을 통해 유도되며, 정적 사상들은 학습 가능한 편향 **b**[pre]_𝑙_, **b**[post]_𝑙_ ∈ **R**[1][×]_[𝑛]_ 및 **b**[res]_𝑙_ ∈ **R**_[𝑛]_ [×] _[𝑛]_으로 표현된다.

이러한 사상들—H_𝑙_[pre], H_𝑙_[post], 그리고 H_𝑙_[res]—의 도입이 무시할 만한 계산 오버헤드만을 발생시킨다는 점은 주목할 가치가 있다. 전형적인 확장 비율 _𝑛_, 예를 들어 4는, 입력 차원 _𝐶_보다 훨씬 작기 때문이다. 이러한 설계로 인해, HC는 잔차 스트림의 정보 용량을 층의 입력 차원으로부터 효과적으로 분리하는데, 이는 모델의 계산 복잡도(FLOPs)와 강하게 상관되어 있다. 결과적으로, HC는 사전 학습 스케일링 법칙(Hoffmann et al., 2022)에서 논의된 모델 FLOPs 및 학습 데이터 크기의 전통적인 스케일링 차원을 보완하며, 잔차 스트림 폭을 조정함으로써 스케일링을 위한 새로운 방향을 제공한다.

HC는 잔차 스트림과 층 입력 간의 차원 불일치를 관리하기 위해 세 가지 사상을 필요로 하지만, 표 1에 제시된 예비 실험은 잔차 사상 H_𝑙_[res]가 가장 중요한 성능 향상을 제공한다는 것을 나타낸다. 이 발견은 잔차 스트림 내의 효과적인 정보 교환의 중요성을 강조한다.

표 1 | **HC 구성요소의 절제 연구.** 특정 사상(H_𝑙_[pre], H_𝑙_[post], 또는 H_𝑙_[res])이 비활성화될 때, 차원 일관성을 유지하기 위해 고정된 사상을 사용한다: H_𝑙_[pre]에는 1/_𝑛_의 균일 가중치, H_𝑙_[post]에는 1의 균일 가중치, H_𝑙_[res]에는 항등 행렬.

H_𝑙_[res] H_𝑙_[pre] H_𝑙_[post] 절대 손실 차이

0.0
✓         - 0.022
✓ ✓         - 0.025
✓ ✓ ✓         - 0.027

**3.1. 수치적 불안정성**

잔차 사상 H_𝑙_[res]는 성능에 중요하지만, 그것의 순차적 적용은 수치적 안정성에 심각한 위험을 초래한다. 식 (4)에 상세히 설명된 바와 같이, HC가 여러 층에 걸쳐 확장될 때, 층 _𝑙_에서 _𝐿_까지의 효과적인 신호 전파는 합성 사상 [∏]_𝑖_ _[𝐿]_ = [−] 1_[𝑙]_ [H]_𝐿_[res] - _𝑖_에 의해 관장된다. 학습 가능한 사상 H_𝑙_[res]가 제약되지 않기 때문에, 이 합성 사상은 필연적으로 항등 사상에서 벗어난다. 결과적으로, 신호 크기는 순전파와 역전파 모두에서 폭발 또는 소실되기 쉽다. 이 현상은 방해받지 않는 신호 흐름에 의존하는 잔차 학습의 기본 전제를 훼손하여, 더 깊거나 대규모 모델에서 학습 과정을 불안정하게 만든다.

실증적 증거가 이 분석을 뒷받침한다. 우리는 그림 2에 도시된 바와 같이 대규모 실험에서 불안정한 손실 행동을 관찰한다. _m_HC를 기준선으로 하여, HC는 약 12,000 스텝 부근에서 예상치 못한 손실 급등을 보이는데, 이는 기울기 노름의 불안정성과 높은 상관관계가 있다. 더욱이, H_𝑙_[res]에 대한 분석은 이 불안정성의 메커니즘을 검증한다. 합성 사상 [∏]_𝑖_ _[𝐿]_ = [−] 1_[𝑙]_ [H]_𝐿_[res] - _𝑖_가 잔차 스트림을 따라 신호를 증폭하는 방식을 정량화하기 위해, 우리는 두 가지 메트릭을 활용한다. 첫 번째는 합성 사상의 행 합의 최대 절댓값을 기반으로 하여 순전파에서의 최악의 경우 확장을 포착한다. 두 번째는 최대 절대 열 합을 기반으로 하며, 이는 역전파에 해당한다. 우리는 이러한 메트릭을 합성 사상의 _최대 이득 크기(Amax Gain Magnitude)_로 지칭한다. 그림 3 (b)에 도시된 바와 같이, 최대 이득 크기는 3000의 피크를 보이는 극단적인 값을 산출하는데, 이는 1로부터의 현저한 이탈로서 잔차 스트림 폭발의 존재를 확인한다.

6

그림 2 | **하이퍼 연결(HC)의 학습 불안정성.** 이 그림은 (a) _m_HC에 대한 HC의 절대 손실 차이, 그리고 (b) 기울기 노름의 비교를 보여준다. 모든 결과는 27B 모델을 기반으로 한다.

|Hr es Forward Signal Gain<br>l<br>Hr es Backward Gradient<br>l|Gain|
|---|---|
|||
|||
|0<br>10<br>20<br><br>Laye|0<br>10<br>20<br><br>Laye|

|5|Col2|Col3|
|---|---|---|
||Y<br>l<br>i = 1H<br>Y<br>~~61 −l~~<br>i = 1|res<br>l + 1 −i Forward Signal Gain<br>~~res~~<br>61 i~~ Backward Gradient Gain~~|
||Y<br>l<br>i = 1H<br>Y<br>~~61 −l~~<br>i = 1|res<br>l + 1 −i Forward Signal Gain<br>~~res~~<br>61 i~~ Backward Gradient Gain~~|
||<br>|−|
||||
||||
||||
|0<br>10<br>20<br>30<br>Layer In|0<br>10<br>20<br>30<br>Layer In|40<br>50<br>60<br> dexl|

그림 3 | **하이퍼 연결(HC)의 전파 불안정성.** 이 그림은 (a) 단일 층 사상 H_𝑙_[res]과 (b) 합성 사상

- _𝐿_ - _𝑙_
_𝑖_ =1 [H]_𝐿_[res]   - _𝑖_의 전파 동역학을 27B 모델 내에서 보여준다. 층 인덱스 _𝑙_(x-축)은 각 표준 트랜스포머 블록을 두 개의 독립적인 층(어텐션과 FFN)으로 전개한다. 최대 이득 크기(y-축)는 최대 절대 행 합(순전파 신호의 경우)과 열 합(역전파 기울기의 경우)으로 계산되며, 선택된 시퀀스의 모든 토큰에 걸쳐 평균화된다.

**3.2. 시스템 오버헤드**

HC의 계산 복잡도는 추가 사상들의 선형성으로 인해 관리 가능하지만, 시스템 수준의 오버헤드는 무시할 수 없는 문제를 제기한다. 특히, 메모리 접근(I/O) 비용은 흔히 현대 모델 아키텍처에서 주요 병목 중 하나를 구성하며, 이는 널리 "메모리 월(memory wall)"로 지칭된다 (Dao et al., 2022). 이 병목은 아키텍처 설계에서 자주 간과되지만, 런타임 효율성에 결정적인 영향을 미친다.

널리 채택된 사전 정규화 트랜스포머(pre-norm Transformer) (Vaswani et al., 2017) 아키텍처에 초점을 맞춰, 우리는 HC에 내재된 I/O 패턴을 분석한다. 표 2는 _𝑛_-스트림 잔차 설계에 의해 도입된 단일 잔차 층에서의 토큰 당 메모리 접근 오버헤드를 요약한다. 분석 결과, HC는 메모리 접근 비용을 대략 _𝑛_에 비례하는 배수만큼 증가시키는 것으로 나타난다. 이러한 과도한 I/O 요구는 융합된 커널의 완화 없이는 학습 처리량을 크게 저하시킨다. 더욱이, H_𝑙_[pre], H_𝑙_[post], 그리고 H_𝑙_[res]는 학습 가능한 매개변수를 포함하기 때문에, 그들의 중간 활성화가 역전파에 필요하다. 이는 GPU 메모리 사용량의 상당한 증가를 초래하며, 종종 실행 가능한 메모리 사용량을 유지하기 위해 기울기 체크포인팅을 필요로 한다. 게다가, HC는 파이프라인 병렬화(Qi et al., 2024)에서 _𝑛_배 더 많은 통신 비용을 요구하여, 더 큰 버블을 발생시키고 학습 처리량을 감소시킨다.

7

표 2 | **토큰 당 메모리 접근 비용 비교.** 이 분석은 순전파에서 잔차 스트림 유지에 의해 도입된 오버헤드를 설명하며, 층 함수 F의 내부 I/O는 제외한다.

방법 연산 읽기 (요소 수) 쓰기 (요소 수)

잔차
연결

하이퍼연결

#### **4. 방법론**

잔차 병합 2_𝐶_ _𝐶_

**총 I/O** **2C** **C**

H_𝑙_[pre], H_𝑙_[post], H_𝑙_[res] 계산 _𝑛𝐶_ _𝑛_[2] + 2_𝑛_
H_𝑙_[pre] _𝑛𝐶_ + _𝑛_ _𝐶_
H_𝑙_[post] _𝐶_ + _𝑛_ _𝑛𝐶_
H_𝑙_[res] _𝑛𝐶_ + _𝑛_[2] _𝑛𝐶_
잔차 병합 2_𝑛𝐶_ _𝑛𝐶_

**총 I/O** ( **5n** + **1** ) **C** + **n****[2]** + **2n** ( **3n** + **1** ) **C** + **n****[2]** + **2n**

**4.1. 매니폴드 제약 하이퍼 연결**

항등 사상(He et al., 2016b) 원리에서 영감을 받아, _m_HC의 핵심 전제는 잔차 사상 H_𝑙_[res]를 특정 매니폴드 위로 제약하는 것이다. 원래의 항등 사상은 H_𝑙_[res] = **I**를 강제함으로써 안정성을 보장하지만, 이는 근본적으로 잔차 스트림 내의 정보 교환을 배제하며, 이는 다중 스트림 아키텍처의 잠재력을 극대화하는 데 필수적이다. 따라서, 우리는 잔차 사상을 층 간 신호 전파의 안정성을 동시에 유지하고 잔차 스트림들 간의 상호 작용을 촉진하여 모델의 표현력을 보존하는 매니폴드 위로 투영할 것을 제안한다. 이를 위해, 우리는 H_𝑙_[res]를 이중 확률 행렬(doubly stochastic matrix)로 제한하는데, 이는 행과 열이 모두 1로 합산되는 비음수 항목을 갖는다. 형식적으로, M[res]를 이중 확률 행렬의 매니폴드(버코프 폴리토프로도 알려진)라고 하면, 우리는 H_𝑙_[res]를 PMres(H_𝑙_[res])로 제약하며, 다음과 같이 정의된다:

PMres(H_𝑙_[res]) ≔ �H_𝑙_[res] ∈ **R**_[𝑛]_ [×] _[𝑛]_ | H_𝑙_[res] **1**_𝑛_ = **1**_𝑛_, **1**[⊤]_𝑛_ [H]_𝑙_[res] = **1**[⊤]_𝑛_ [,][ H]_𝑙_[res] ⩾ 0�, (6)

여기서 **1**_𝑛_은 _𝑛_-차원의 모든 요소가 1인 벡터를 나타낸다.

_𝑛_ = 1일 때, 이중 확률 조건은 스칼라 1로 퇴화되어 원래의 항등 사상을 복원한다는 점은 주목할 가치가 있다. 이중 확률성의 선택은 대규모 모델 학습에 유익한 몇 가지 엄격한 이론적 특성을 부여한다:

1. **노름 보존:** 이중 확률 행렬의 스펙트럼 노름은 1로 제한된다 (즉, ∥H_𝑙_[res]∥2 ≤ 1). 이는 학습 가능한 사상이 비확장적임을 의미하여, 기울기 폭발 문제를 효과적으로 완화한다.
2. **합성 폐쇄성:** 이중 확률 행렬의 집합은 행렬 곱셈에 대해 폐쇄되어 있다. 이는 여러 층에 걸친 합성 잔차 사상,

- _𝐿_  - _𝑙_
_𝑖_ =1 [H]_𝐿_[res]          - _𝑖_[,][ 가 이중 확률적으로 유지되어, 모델의 전체 깊이에 걸쳐 안정성을 보존함을 보장한다.]
3. **버코프 폴리토프를 통한 기하학적 해석:** 집합 M[res]는 버코프 폴리토프를 형성하며, 이는 순열 행렬 집합의 볼록 껍질이다. 이는 명확한 기하학적 해석을 제공한다: 잔차 사상은 순열의 볼록 조합으로 작용한다. 수학적으로, 이러한 행렬의 반복적 적용은 증가하는 경향이 있다

### Translation Notes

- Maintained all mathematical equations and notation exactly as presented in the source text
- Preserved all citation formats (Author et al., Year) as per Korean academic convention
- Used established glossary terms consistently:
  - "Hyper-Connections" → "하이퍼 연결 (HC)"
  - "Residual Connection" → "잔차 연결"
  - "Identity Mapping" → "항등 사상"
  - "Doubly Stochastic Matrix" → "이중 확률 행렬"
  - "Birkhoff Polytope" → "버코프 폴리토프"
  - "Memory Wall" → "메모리 월"
  - "Numerical Instability" → "수치적 불안정성"
  - "Macro Design" → "거시적 설계"
  - "Residual Stream" → "잔차 스트림"
- Preserved all table and figure structures with only Korean translation of descriptive text
- Maintained technical precision in translating compound terms like "composite mapping" (합성 사상), "signal propagation" (신호 전파), "gradient norm" (기울기 노름)
- Adapted sentence structures for natural Korean flow while preserving academic formality
- Used Korean particles appropriately for figure/equation references (그림 2, 표 1, 식 (5))
- Preserved all proper nouns (ResNet, DenseNet, FractalNet, DLA, RMT, MUDDFormer, RMSNorm, DualPipe)
- The last sentence appears truncated in the source (line 136 ends mid-sentence with "tends to increase"); translated up to that point maintaining the same truncation

### Confidence Level

High - This is a highly technical academic paper with established mathematical terminology. The translation maintains mathematical rigor, uses correct Korean academic register, and follows standard conventions for technical ML literature in Korean. All glossary terms were applied consistently, and the complex mathematical concepts were translated with precision using established Korean mathematical terminology.

### Transition Notes

- Ending: This chunk ends mid-sentence in Section 4.1, specifically discussing the "Geometric Interpretation via the Birkhoff Polytope." The sentence begins explaining that "the repeated application of such matrices tends to increase..." but cuts off before completion. The next chunk (chunk 003) should continue this thought about the mathematical properties of doubly stochastic matrices and likely complete the discussion of the three theoretical properties that benefit large-scale model training. The translator for the next chunk should be aware that they are picking up mid-sentence and should ensure smooth continuation of the geometric interpretation explanation.
