## Translation Output

### Translated Text

## **mHC: 매니폴드 제약 하이퍼 연결 (Manifold-Constrained Hyper-Connections)**

Zhenda Xie* [†], Yixuan Wei*, Huanqi Cao*, Chenggang Zhao, Chengqi Deng, Jiashi Li, Damai Dai, Huazuo Gao, Jiang Chang, Kuai Yu, Liang Zhao, Shangyan Zhou, Zhean Xu, Zhengyan Zhang, Wangding Zeng, Shengding Hu, Yuqing Wang, Jingyang Yuan, Lean Wang, Wenfeng Liang

#### **DeepSeek-AI**

### **초록**

최근 하이퍼 연결(Hyper-Connections, HC)로 대표되는 연구들은 지난 10년간 확립된 잔차 연결 패러다임을 잔차 스트림의 폭을 확장하고 연결 패턴을 다양화함으로써 확장했다. 이러한 다양화는 상당한 성능 향상을 가져오지만, 잔차 연결에 내재된 항등 사상(identity mapping) 특성을 근본적으로 저해하여 심각한 학습 불안정성과 제한된 확장성을 유발하고, 추가적으로 상당한 메모리 액세스 오버헤드를 발생시킨다. 이러한 문제를 해결하기 위해, 우리는 **매니폴드 제약 하이퍼 연결(Manifold-Constrained Hyper-Connections, _mHC_)**을 제안한다. 이는 HC의 잔차 연결 공간을 특정 매니폴드에 투영하여 항등 사상 특성을 복원하는 동시에, 효율성을 보장하기 위한 엄격한 인프라 최적화를 포함하는 일반적인 프레임워크이다. 실험 결과 _mHC_는 대규모 학습에 효과적이며, 실질적인 성능 향상과 우수한 확장성을 제공한다. 우리는 _mHC_가 HC의 유연하고 실용적인 확장으로서 위상적 아키텍처 설계에 대한 깊은 이해에 기여하고, 기반 모델의 발전을 위한 유망한 방향을 제시할 것으로 기대한다.

(a) 잔차 연결(Residual Connection) (b) 하이퍼 연결(Hyper-Connections, HC) (c) 매니폴드 제약 HC (_mHC_)

그림 1 | **잔차 연결 패러다임의 예시.** 이 그림은 (a) 표준 잔차 연결, (b) 하이퍼 연결(HC), (c) 우리가 제안하는 **매니폴드 제약 하이퍼 연결(_mHC_)**의 구조적 설계를 비교한다. 제약 없는 HC와 달리, _mHC_는 행렬을 제약된 매니폴드에 투영하여 안정성을 보장하는 방식으로 잔차 연결 공간을 최적화하는 데 중점을 둔다.

*핵심 기여자. [†] [책임 저자: xie.zhenda@deepseek.com](mailto:xie.zhenda@deepseek.com)

#### **목차**

**1** **서론** **3**

**2** **관련 연구** **4**

2.1 미시적 설계 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 4

2.2 거시적 설계 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 5

**3** **예비 지식** **5**

3.1 수치적 불안정성 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 6

3.2 시스템 오버헤드 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 7

**4** **방법론** **8**

4.1 매니폴드 제약 하이퍼 연결 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 8

4.2 매개변수화 및 매니폴드 투영 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 9

4.3 효율적 인프라 설계 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 9

4.3.1 커널 융합 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 9

4.3.2 재계산 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 10

4.3.3 듀얼파이프에서의 통신 중첩 . . . . . . . . . . . . . . . . . . . . . . . . . 11

**5** **실험** **12**

5.1 실험 설정 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 12

5.2 주요 결과 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 12

5.3 확장성 실험 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 13

5.4 안정성 분석 . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . 14

**6** **결론 및 전망** **15**

**A 부록** **19**

A.1 모델 사양 및 하이퍼파라미터 세부사항 . . . . . . . . . . . . . . . . . . . . . . . . 19

2

#### **1. 서론**

심층 신경망 아키텍처는 ResNets (He et al., 2016a)의 도입 이후 빠른 진화를 거쳐왔다. 그림 1(a)에 나타난 바와 같이, 단일 계층의 구조는 다음과 같이 정식화될 수 있다:
**x**_𝑙_+1 = **x**_𝑙_ + F(**x**_𝑙_, W_𝑙_), (1)

여기서 **x**_𝑙_과 **x**_𝑙_+1은 각각 _𝑙_-번째 계층의 _𝐶_-차원 입력과 출력을 나타내며, F는 잔차 함수를 나타낸다. 잔차 함수 F가 지난 10년 동안 합성곱, 어텐션 메커니즘, 피드포워드 네트워크 등 다양한 연산을 포함하도록 진화했지만, 잔차 연결의 패러다임은 원래의 형태를 유지해왔다. 트랜스포머(Transformer) (Vaswani et al., 2017) 아키텍처의 발전과 함께, 이 패러다임은 현재 대규모 언어 모델(Large Language Models, LLMs) (Brown et al., 2020; Liu et al., 2024b; Touvron et al., 2023)의 기본 설계 요소로 자리 잡았다.

이러한 성공은 주로 잔차 연결의 간결한 형태에 기인한다. 더 중요하게는, 초기 연구 (He et al., 2016b)에서 잔차 연결의 항등 사상 특성이 대규모 학습 중 안정성과 효율성을 유지한다는 것이 밝혀졌다. 여러 계층에 걸쳐 잔차 연결을 재귀적으로 확장하면, 식 (1)은 다음과 같이 된다:

**x**_𝐿_ = **x**_𝑙_ +
_𝐿_−1
∑︁
F(**x**_𝑖_, W_𝑖_), (2)
_𝑖_=_𝑙_

여기서 _𝐿_과 _𝑙_은 각각 더 깊은 계층과 더 얕은 계층에 해당한다. 항등 사상이라는 용어는 **x**_𝑙_ 자체를 가리키며, 이는 얕은 계층의 신호가 어떠한 수정도 없이 직접 깊은 계층으로 매핑된다는 특성을 강조한다.

최근 하이퍼 연결(Hyper-Connections, HC) (Zhu et al., 2024)로 대표되는 연구들은 잔차 연결에 새로운 차원을 도입하여 그 성능 잠재력을 경험적으로 입증했다. HC의 단일 계층 아키텍처는 그림 1(b)에 나타나 있다. 잔차 스트림의 폭을 확장하고 연결 복잡도를 향상시킴으로써, HC는 개별 유닛의 FLOPs 관점에서 계산 오버헤드를 변경하지 않으면서도 위상적 복잡성을 크게 증가시킨다.
형식적으로, HC의 단일 계층 전파는 다음과 같이 정의된다:

**x**_𝑙_+1 = H_𝑙_[res]**x**_𝑙_ + H_𝑙_[post][⊤]F(H_𝑙_[pre]**x**_𝑙_, W_𝑙_), (3)

여기서 **x**_𝑙_과 **x**_𝑙_+1은 _𝑙_-번째 계층의 입력과 출력을 나타낸다. 식 (1)의 정식화와 달리, **x**_𝑙_과 **x**_𝑙_+1의 특징 차원은 _𝐶_에서 _𝑛_ × _𝐶_로 확장되며, 여기서 _𝑛_은 확장 비율이다. H_𝑙_[res] ∈ **R**_[𝑛]_[×]_[𝑛]_은 잔차 스트림 내의 특징을 혼합하는 학습 가능한 매핑을 나타낸다. 또한 학습 가능한 매핑인 H_𝑙_[pre] ∈ **R**[1][×]_[𝑛]_은 _𝑛𝐶_-차원 스트림에서 특징을 _𝐶_-차원 계층 입력으로 집계하고, 반대로 H_𝑙_[post] ∈ **R**[1][×]_[𝑛]_은 계층 출력을 다시 스트림에 매핑한다.

그러나 학습 규모가 증가함에 따라, HC는 불안정성의 잠재적 위험을 야기한다. 주요 우려사항은 HC의 제약 없는 특성이 아키텍처가 여러 계층에 걸쳐 확장될 때 항등 사상 특성을 저해한다는 것이다. 여러 병렬 스트림으로 구성된 아키텍처에서, 이상적인 항등 사상은 보존 메커니즘으로 작용한다. 이는 순전파와 역전파 모두에서 스트림 간 평균 신호 강도가 불변으로 유지되도록 보장한다. 식 (3)을 통해 HC를 여러 계층으로 재귀적으로 확장하면 다음과 같다:

��

**x**_𝐿_ =

- _𝐿_ - _𝑙_

H_𝐿_[res]  - _𝑖_
_𝑖_=1

**x**_𝑙_ +

_𝐿_−1
∑︁

_𝑖_=_𝑙_

_𝐿_−1−_𝑖_

H_𝐿_[res]  - _𝑗_ �� H_𝑖_[post][⊤]F(H_𝑖_[pre]**x**_𝑖_, W_𝑖_), (4)
_𝑗_=1

3

여기서 _𝐿_과 _𝑙_은 각각 더 깊은 계층과 더 얕은 계층을 나타낸다. 식 (2)와 대조적으로, HC의 복합 매핑 [�]_𝑖_[𝐿]_=_[−]_1_[𝑙]_[H]_𝐿_[res]_[−]_𝑖_[는 특징의 전역 평균을 보존하지 못한다. 이러한 차이는 무제한적인 신호 증폭 또는 감쇠로 이어져, 대규모 학습 중 불안정성을 초래한다. 또 다른 고려사항은, HC가 FLOPs 관점에서 계산 효율성을 유지하지만, 확장된 잔차 스트림에 대한 메모리 액세스 비용 관점에서의 하드웨어 효율성은 원래 설계에서 다루어지지 않았다는 것이다. 이러한 요인들은 집합적으로 HC의 실용적 확장성을 제한하고 대규모 학습에서의 적용을 방해한다.

이러한 문제를 해결하기 위해, 우리는 그림 1(c)에 나타난 **매니폴드 제약 하이퍼 연결(_mHC_)**을 제안한다. 이는 HC의 잔차 연결 공간을 특정 매니폴드에 투영하여 항등 사상 특성을 복원하는 동시에, 효율성을 보장하기 위한 엄격한 인프라 최적화를 포함하는 일반적인 프레임워크이다. 구체적으로, _mHC_는 싱크혼-크놉 알고리즘(Sinkhorn-Knopp algorithm) (Sinkhorn and Knopp, 1967)을 활용하여 H_𝑙_[res]을 버코프 폴리토프(Birkhoff polytope)에 엔트로피적으로 투영한다.
이 연산은 잔차 연결 행렬을 이중 확률 행렬(doubly stochastic matrices)로 구성된 매니폴드 내에 효과적으로 제약한다. 이러한 행렬의 행과 열의 합이 1이므로, H_𝑙_[res]**x**_𝑙_ 연산은 입력 특징의 볼록 조합(convex combination)으로 기능한다.
이러한 특성은 특징 평균이 보존되고 신호 노름이 엄격하게 정규화되는 잘 조건화된(well-conditioned) 신호 전파를 촉진하여, 신호 소실 또는 폭발의 위험을 효과적으로 완화한다. 더 나아가, 이중 확률 행렬에 대한 행렬 곱셈의 폐포성(closure)으로 인해, 복합 매핑 [�]_𝑖_[𝐿]_=_[−]_1_[𝑙]_[H]_𝐿_[res]_[−]_𝑖_[는 이러한 보존 특성을 유지한다.]
결과적으로, _mHC_는 임의의 깊이 간 항등 사상의 안정성을 효과적으로 유지한다. 효율성을 보장하기 위해, 우리는 커널 융합(kernel fusion)을 사용하고 TileLang (Wang et al., 2025)을 활용한 혼합 정밀도 커널을 개발한다. 또한, 선택적 재계산을 통해 메모리 사용량을 완화하고 듀얼파이프(DualPipe) 스케줄 (Liu et al., 2024b) 내에서 통신을 신중하게 중첩시킨다.

언어 모델 사전 학습에 대한 광범위한 실험은 _mHC_가 HC의 성능 이점을 유지하면서 탁월한 안정성과 확장성을 보여줌을 입증한다. 사내 대규모 학습 결과는 _mHC_가 대규모 학습을 지원하며 확장 비율 _𝑛_ = 4일 때 단지
6.7%의 추가 시간 오버헤드만을 발생시킨다는 것을 보여준다.

#### **2. 관련 연구**

심층 학습의 아키텍처 발전은 주로 _미시적 설계(micro-design)_와
_거시적 설계(macro-design)_로 분류될 수 있다. 미시적 설계는 계산 블록의 내부 아키텍처에 관한 것으로, 공간적, 시간적, 채널 차원에 걸쳐 특징이 어떻게 처리되는지를 명시한다. 반면, 거시적 설계는 블록 간 위상적 구조를 확립하여, 서로 다른 계층에 걸쳐 특징 표현이 어떻게 전파되고, 라우팅되고, 병합되는지를 규정한다.

**2.1. 미시적 설계**

매개변수 공유와 평행 이동 불변성에 의해 구동되는 합성곱은 초기에 구조화된 신호 처리를 지배했다. 깊이별 분리 합성곱(depthwise separable) (Chollet, 2017)과 그룹 합성곱(grouped convolutions) (Xie et al., 2017)과 같은 후속 변형들이 효율성을 최적화했지만, 트랜스포머(Transformers) (Vaswani et al., 2017)의 출현으로 어텐션(Attention)과 피드포워드 네트워크(Feed-Forward Networks, FFNs)가 현대 아키텍처의 기본 구성 요소로 확립되었다. 어텐션 메커니즘은 전역 정보 전파를 촉진하는 반면, FFNs는 개별 특징의 표현 능력을 향상시킨다. LLMs의 계산적 요구와 성능의 균형을 맞추기 위해, 어텐션 메커니즘은 다중 쿼리 어텐션(Multi-Query Attention, MQA) (Shazeer, 2019), 그룹 쿼리 어텐션(Grouped-Query Attention, GQA) (Ainslie et al., 2023), 다중 헤드 잠재 어텐션(Multi-Head Latent Attention)

4

(MLA) (Liu et al., 2024a)과 같은 효율적인 변형으로 진화해왔다. 동시에, FFNs는 전문가 혼합(Mixture-of-Experts, MoE) (Fedus et al., 2022; Lepikhin et al., 2020; Shazeer et al., 2017)을 통해 희소 연산 패러다임으로 일반화되어, 비례적인 계산 비용 없이 대규모 매개변수 확장을 가능하게 했다.

### Translation Notes

- **Mathematical equations**: All equations (1)-(4) preserved exactly as written, with only surrounding Korean text translated
- **Acronym handling**: Consistent pattern established - Korean translation followed by English acronym in parentheses on first mention (e.g., "하이퍼 연결(Hyper-Connections, HC)")
- **Technical terminology**: Used pre-translated glossary terms consistently:
  - "Residual Connection" → "잔차 연결"
  - "Identity Mapping" → "항등 사상"
  - "Doubly Stochastic Matrix" → "이중 확률 행렬"
  - "Sinkhorn-Knopp Algorithm" → "싱크혼-크놉 알고리즘"
  - "Birkhoff Polytope" → "버코프 폴리토프"
- **Section numbering**: Preserved numerical headings (1, 2, 2.1) with translated section titles
- **Citation format**: Maintained Western citation style (Author et al., Year) as standard in Korean CS literature
- **Figure/Table references**: Used Korean reference style consistently (그림 1, 식 (1), 식 (2))
- **Author information**: Kept DeepSeek-AI and email addresses unchanged as proper nouns
- **Formal register**: Maintained formal academic tone throughout, using appropriate Korean grammatical particles and sentence endings (-다, -한다, -였다)
- **Complex mathematical concepts**: Carefully translated terms like "composite mapping" (복합 매핑), "convex combination" (볼록 조합), "closure property" (폐포성) using established mathematical Korean terminology
- **Infrastructure terms**: Technical system terms like "kernel fusion" (커널 융합), "recomputing" (재계산), "DualPipe" (듀얼파이프) translated using glossary

### Confidence Level

High - This is a highly technical academic paper in the machine learning domain. The translation maintains mathematical precision while using established Korean terminology for ML/AI concepts. The glossary provided excellent guidance for consistent term translation. The formal academic register is appropriate for the target audience of AI researchers and engineers in Korea.

### Transition Notes

- **Ending**: The chunk ends mid-sentence in Section 2.1 (Micro Design), discussing the evolution of FFNs into sparse computing paradigms via Mixture-of-Experts. The sentence is incomplete and will continue in the next chunk.
- **Next chunk expectation**: Based on the summary of chunk 2, the next section should complete the discussion of micro design and move into macro design (Section 2.2), then begin the Preliminary section (Section 3) discussing numerical instability and system overhead in HC.
- **Context continuity**: The introduction of MoE at the end provides context for understanding the broader architectural evolution that will lead into the macro design discussion and eventually the specific problems with HC that mHC aims to solve.
