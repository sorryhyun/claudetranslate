## Translation Output

### Translated Text

**# Shots** 3-shot 3-shot 8-shot 10-shot 4-shot 5-shot 0-shot 5-shot

표 4는 다양한 벤치마크 세트에서의 다운스트림 성능을 제시한다 (Bisk et al., 2020; Cobbe et al., 2021; Hendrycks et al., 2020, 2021; Joshi et al., 2017; Zellers et al., 2019). _m_ HC는 포괄적인 개선을 달성하여 일관되게 기준선을 능가하고 대부분의 작업에서 HC를 초과한다. 특히, HC와 비교하여 _m_ HC는 모델의 추론 능력을 더욱 향상시켜 BBH (Suzgun et al., 2022)에서 2.1%, DROP (Dua et al., 2019)에서 2.3%의 성능 향상을 제공한다.

**5.3. 확장성 실험**

그림 6 | **기준선과 비교한** _**m**_ **HC의 확장 특성. (a) 연산 확장성 곡선.** 실선은 다양한 연산 예산에 걸친 성능 차이를 나타낸다. 각 점은 3B와 9B에서 27B 파라미터까지 확장되는 모델 크기와 데이터셋 크기의 특정 연산 최적 구성을 나타낸다. **(b) 토큰 확장성 곡선.** 학습 중 3B 모델의 궤적. 각 점은 서로 다른 학습 토큰에서 모델의 성능을 나타낸다. 자세한 아키텍처 및 학습 구성은 부록 A.1에 제공되어 있다.

우리의 접근법의 확장성을 평가하기 위해, 서로 다른 규모에 걸쳐 기준선 대비 _m_ HC의 상대적 손실 개선을 보고한다. 그림 6 (a)에서는 3B, 9B, 27B 파라미터에 걸친 연산 확장성 곡선을 그린다. 궤적은 성능 이점이 더 높은 연산 예산에서도 견고하게 유지되며, 미미한 감쇠만 보인다는 것을 나타낸다. 또한, 그림 6 (b)에서 실행 내 동역학을 조사하며, 이는 3B 모델에 대한 토큰 확장성 곡선을 제시한다. 종합적으로, 이러한 발견은 대규모 시나리오에서 _m_ HC의 효과를 검증한다. 이 결론은 우리의 사내 대규모 학습 실험에 의해 더욱 입증된다.

13

그림 7 | **매니폴드 제약 하이퍼 연결 (** _**m**_ **HC)의 전파 안정성.** 이 그림은 (a) 단일 계층 매핑 PMres (H _𝑙_ [res] )와 (b) 27B 모델 내에서 복합 매핑 [�] _𝑖_ _[𝐿]_ = [−] 1 _[𝑙]_ [P][M][res] [(H] _𝐿_ [res] - _𝑖_ [)]의 전파 동역학을 보여준다. 결과는 _m_ HC가 HC와 비교하여 전파 안정성을 크게 향상시킨다는 것을 보여준다.

그림 8 | **학습 가능한 매핑의 시각화.** 이 그림은 HC (첫 번째 행)와 _m_ HC (두 번째 행)에 대한 대표적인 단일 계층 및 복합 매핑을 표시한다. 각 행렬은 선택된 시퀀스 내의 모든 토큰에 대해 평균을 구하여 계산된다. y축과 x축을 따라 표시된 레이블은 각각 순전파 신호 증폭 (행 합)과 역전파 기울기 증폭 (열 합)을 나타낸다.

**5.4. 안정성 분석**

그림 3과 유사하게, 그림 7은 _m_ HC의 전파 안정성을 보여준다. 이상적으로, 단일 계층 매핑은 이중 확률 제약을 만족하며, 이는 순전파 신호 증폭과 역전파 기울기 증폭이 모두 1이어야 함을 의미한다. 그러나 싱크혼-크놉 알고리즘을 활용하는 실제 구현에서는 연산 효율성을 달성하기 위해 반복 횟수를 제한해야 한다. 우리의 설정에서는 20회 반복을 사용하여 근사 솔루션을 얻는다. 결과적으로, 그림 7(a)에서 보여지듯이 역전파 기울기 증폭이 1에서 약간 벗어난다. 그림 7(b)에 표시된 복합 경우에서는 편차가 증가하지만 제한되어 있으며, 최대값이 약 1.6에 도달한다. 특히, HC의 거의 3000에 달하는 최대 이득 크기와 비교하여 _m_ HC는 이를 3차수 크기로 감소시킨다. 이러한 결과는 _m_ HC가 HC와 비교하여 전파 안정성을 크게 향상시켜 안정적인 순전파 신호 및 역전파 기울기 흐름을 보장한다는 것을 보여준다. 추가로, 그림 8은 대표적인 매핑을 표시한다. 우리는 HC의 경우 최대 이득이 클 때 다른 값들도 크게 나타나는 경향이 있으며, 이는 모든 전파 경로에 걸친 일반적인 불안정성을 나타낸다는 것을 관찰한다. 대조적으로, _m_ HC는 일관되게 안정적인 결과를 산출한다.

14

#### **6. 결론 및 전망**

본 논문에서는 하이퍼 연결 (HC)에서 제안된 바와 같이 잔차 스트림의 폭을 확장하고 연결을 다양화하는 것이 성능 향상을 가져오는 동시에, 이러한 연결의 무제약적 특성이 신호 발산을 유발한다는 것을 밝힌다. 이러한 교란은 계층 간 신호 에너지 보존을 손상시켜 학습 불안정성을 유도하고 심층 네트워크의 확장성을 저해한다. 이러한 과제를 해결하기 위해, 우리는 잔차 연결 공간을 특정 매니폴드에 투영하는 일반화된 프레임워크인 **매니폴드 제약 하이퍼 연결** ( _**m**_ **HC** )을 소개한다. 싱크혼-크놉 알고리즘을 사용하여 잔차 매핑에 이중 확률 제약을 적용함으로써, _m_ HC는 신호 전파를 특징의 볼록 조합으로 변환한다. 실험 결과는 _m_ HC가 효과적으로 항등 사상 특성을 복원하여 기존 HC와 비교하여 우수한 확장성으로 안정적인 대규모 학습을 가능하게 한다는 것을 확인한다. 중요하게도, 효율적인 인프라 수준 최적화를 통해 _m_ HC는 무시할 수 있는 연산 오버헤드로 이러한 개선을 제공한다.

HC 패러다임의 일반화된 확장으로서, _m_ HC는 향후 연구를 위한 여러 유망한 방향을 제시한다. 본 연구는 안정성을 보장하기 위해 이중 확률 행렬을 활용하지만, 프레임워크는 특정 학습 목표에 맞춤화된 다양한 매니폴드 제약의 탐색을 수용한다. 우리는 서로 다른 기하학적 제약에 대한 추가 조사가 가소성과 안정성 간의 균형을 더 잘 최적화하는 새로운 방법을 산출할 수 있을 것으로 기대한다. 또한, _m_ HC가 거시적 아키텍처 설계에 대한 커뮤니티의 관심을 다시 불러일으키기를 바란다. 토폴로지 구조가 최적화 및 표현 학습에 미치는 영향에 대한 이해를 심화함으로써, _m_ HC는 현재의 한계를 해결하고 차세대 기초 아키텍처의 진화를 위한 새로운 경로를 잠재적으로 조명할 것이다.

#### **참고문헌**

J. Ainslie, J. Lee-Thorp, M. De Jong, Y. Zemlyanskiy, F. Lebrón, and S. Sanghai. Gqa: Training generalized multi-query transformer models from multi-head checkpoints. arXiv preprint arXiv:2305.13245, 2023.

Y. Bisk, R. Zellers, R. L. Bras, J. Gao, and Y. Choi. PIQA: reasoning about physical commonsense in natural language. In The Thirty-Fourth AAAI Conference on Artifcial Intelligence, AAAI
2020, The Thirty-Second Innovative Applications of Artifcial Intelligence Conference, IAAI
2020, The Tenth AAAI Symposium on Educational Advances in Artifcial Intelligence, EAAI
2020, New York, NY, USA, February 7-12, 2020, pages 7432–7439. AAAI Press, 2020. doi:
10.1609/aaai.v34i05.6239. URL `https://doi.org/10.1609/aaai.v34i05.6239` .

T. Brown, B. Mann, N. Ryder, M. Subbiah, J. D. Kaplan, P. Dhariwal, A. Neelakantan, P. Shyam, G. Sastry, A. Askell, et al. Language models are few-shot learners. Advances in neural information processing systems, 33:1877–1901, 2020.

Y. Chai, S. Jin, and X. Hou. Highway transformer: Self-gating enhanced self-attentive networks.
In D. Jurafsky, J. Chai, N. Schluter, and J. Tetreault, editors, Proceedings of the 58th Annual
Meeting of the Association for Computational Linguistics, pages 6887–6900, Online, July
2020. Association for Computational Linguistics. doi: 10.18653/v1/2020.acl-main.616. URL
`https://aclanthology.org/2020.acl-main.616/` .

F. Chollet. Xception: Deep learning with depthwise separable convolutions. In Proceedings of

the IEEE conference on computer vision and pattern recognition, pages 1251–1258, 2017.

15

K. Cobbe, V. Kosaraju, M. Bavarian, M. Chen, H. Jun, L. Kaiser, M. Plappert, J. Tworek, J. Hilton, R. Nakano, et al. Training verifiers to solve math word problems. arXiv preprint arXiv:2110.14168, 2021.

T. Dao, D. Y. Fu, S. Ermon, A. Rudra, and C. Ré. FlashAttention: Fast and memory-efficient exact attention with IO-awareness. In Advances in Neural Information Processing Systems (NeurIPS), 2022.

D. Dua, Y. Wang, P. Dasigi, G. Stanovsky, S. Singh, and M. Gardner. DROP: A reading comprehension benchmark requiring discrete reasoning over paragraphs. In J. Burstein, C. Doran, and
T. Solorio, editors, Proceedings of the 2019 Conference of the North American Chapter of the
Association for Computational Linguistics: Human Language Technologies, NAACL-HLT
2019, Minneapolis, MN, USA, June 2-7, 2019, Volume 1 (Long and Short Papers), pages 2368–
2378. Association for Computational Linguistics, 2019. doi: 10.18653/V1/N19-1246. URL
`https://doi.org/10.18653/v1/n19-1246` .

Y. Fang, Y. CAI, J. Chen, J. Zhao, G. Tian, and G. Li. Cross-layer retrospective retrieving via layer attention. In The Eleventh International Conference on Learning Representations, 2023. URL
`https://openreview.net/forum?id=pvgEL1yS3Ql` .

W. Fedus, B. Zoph, and N. Shazeer. Switch transformers: Scaling to trillion parameter models with simple and efficient sparsity. Journal of Machine Learning Research, 23(120):1–39, 2022.

K. He, X. Zhang, S. Ren, and J. Sun. Deep residual learning for image recognition. In Proceedings

of the IEEE conference on computer vision and pattern recognition, pages 770–778, 2016a.

K. He, X. Zhang, S. Ren, and J. Sun. Identity mappings in deep residual networks. In European

conference on computer vision, pages 630–645. Springer, 2016b.

M. Heddes, A. Javanmard, K. Axiotis, G. Fu, M. Bateni, and V. Mirrokni. Deepcrossattention:
Supercharging transformer residual connections. In Forty-second International Conference on Machine Learning, 2025. URL `https://openreview.net/forum?id=j3JBfFnGYh` .

D. Hendrycks, C. Burns, S. Basart, A. Zou, M. Mazeika, D. Song, and J. Steinhardt. Measuring massive multitask language understanding. arXiv preprint arXiv:2009.03300, 2020.

D. Hendrycks, C. Burns, S. Kadavath, A. Arora, S. Basart, E. Tang, D. Song, and J. Steinhardt. Measuring mathematical problem solving with the math dataset. arXiv preprint arXiv:2103.03874, 2021.

J. Hoffmann, S. Borgeaud, A. Mensch, E. Buchatskaya, T. Cai, E. Rutherford, D. de Las Casas, L. A. Hendricks, J. Welbl, A. Clark, T. Hennigan, E. Noland, K. Millican, G. van den Driessche, B. Damoc, A. Guy, S. Osindero, K. Simonyan, E. Elsen, O. Vinyals, J. Rae, and L. Sifre.
An empirical analysis of compute-optimal large language model training. In S. Koyejo, S. Mohamed, A. Agarwal, D. Belgrave, K. Cho, and A. Oh, editors, Advances in Neural
Information Processing Systems, volume 35, pages 30016–30030. Curran Associates, Inc., 2022.
URL `https://proceedings.neurips.cc/paper_files/paper/2022/file/c1e2faff6f588870935f114ebe04a3e5-Paper-Conference.pdf` .

G. Huang, Z. Liu, L. Van Der Maaten, and K. Q. Weinberger. Densely connected convolutional networks. In Proceedings of the IEEE conference on computer vision and pattern recognition, pages 4700–4708, 2017.

16

M. Joshi, E. Choi, D. Weld, and L. Zettlemoyer. TriviaQA: A large scale distantly supervised challenge dataset for reading comprehension. In R. Barzilay and M.-Y. Kan, editors, Proceedings of the 55th Annual Meeting of the Association for Computational Linguistics (Volume 1: Long
Papers), pages 1601–1611, Vancouver, Canada, July 2017. Association for Computational
Linguistics. doi: 10.18653/v1/P17-1147. URL `https://aclanthology.org/P17-1147` .

G. Larsson, M. Maire, and G. Shakhnarovich. Fractalnet: Ultra-deep neural networks without residuals. arXiv preprint arXiv:1605.07648, 2016.

D. Lepikhin, H. Lee, Y. Xu, D. Chen, O. Firat, Y. Huang, M. Krikun, N. Shazeer, and Z. Chen.
Gshard: Scaling giant models with conditional computation and automatic sharding. arXiv preprint arXiv:2006.16668, 2020.

A. Liu, B. Feng, B. Wang, B. Wang, B. Liu, C. Zhao, C. Dengr, C. Ruan, D. Dai, D. Guo, et al.
Deepseek-v2: A strong, economical, and efficient mixture-of-experts language model. arXiv preprint arXiv:2405.04434, 2024a.

A. Liu, B. Feng, B. Xue, B. Wang, B. Wu, C. Lu, C. Zhao, C. Deng, C. Zhang, C. Ruan, et al.
Deepseek-v3 technical report. arXiv preprint arXiv:2412.19437, 2024b.

I. Loshchilov and F. Hutter. Decoupled weight decay regularization. arXiv preprint arXiv:1711.05101, 2017.

B. Mak and J. Flanigan. Residual matrix transformers: Scaling the size of the residual stream.

arXiv preprint arXiv:2506.22696, 2025.

G. Menghani, R. Kumar, and S. Kumar. LAurel: Learned augmented residual layer. In
Forty-second International Conference on Machine Learning, 2025. URL `https://openreview.net/forum?id=rUDRWP9WvZ` .

M. Pagliardini, A. Mohtashami, F. Fleuret, and M. Jaggi. Denseformer: Enhancing information flow in transformers via depth weighted averaging. In The Thirty-eighth Annual Conference on Neural Information Processing Systems, 2024. URL `https://openreview.net/forum?id=kMnoh7CXrq` .

P. Qi, X. Wan, G. Huang, and M. Lin. Zero bubble (almost) pipeline parallelism. In The Twelfth

International Conference on Learning Representations, 2024. URL `https://openreview.net/forum?id=tuzTN0eIO5` .

N. Shazeer. Fast transformer decoding: One write-head is all you need. arXiv preprint arXiv:1911.02150, 2019.

N. Shazeer, A. Mirhoseini, K. Maziarz, A. Davis, Q. Le, G. Hinton, and J. Dean. Outrageously large neural networks: The sparsely-gated mixture-of-experts layer. arXiv preprint arXiv:1701.06538, 2017.

R. Sinkhorn and P. Knopp. Concerning nonnegative matrices and doubly stochastic matrices.

Pacifc Journal of Mathematics, 21(2):343–348, 1967.

R. K. Srivastava, K. Greff, and J. Schmidhuber. Training very deep networks. In C. Cortes, N. Lawrence, D. Lee, M. Sugiyama, and R. Garnett, editors, Advances in Neural Information
Processing Systems, volume 28. Curran Associates, Inc., 2015. URL `https://proceedings.neurips.cc/paper_files/paper/2015/file/215a71a12769b056c3c32e7299f1c5ed-Paper.pdf` .

17

J. Su, M. Ahmed, Y. Lu, S. Pan, W. Bo, and Y. Liu. Roformer: Enhanced transformer with rotary position embedding. Neurocomputing, 568:127063, 2024.

M. Suzgun, N. Scales, N. Schärli, S. Gehrmann, Y. Tay, H. W. Chung, A. Chowdhery, Q. V. Le, E. H. Chi, D. Zhou, et al. Challenging big-bench tasks and whether chain-of-thought can solve them. arXiv preprint arXiv:2210.09261, 2022.

H. Touvron, T. Lavril, G. Izacard, X. Martinet, M.-A. Lachaux, T. Lacroix, B. Rozière, N. Goyal, E. Hambro, F. Azhar, et al. Llama: Open and efficient foundation language models. arXiv preprint arXiv:2302.13971, 2023.

A. Vaswani, N. Shazeer, N. Parmar, J. Uszkoreit, L. Jones, A. N. Gomez, Ł. Kaiser, and I. Polosukhin. Attention is all you need. Advances in neural information processing systems, 30, 2017.

### Translation Notes

- 참고문헌 섹션은 학술 관례에 따라 원문 형식을 유지했습니다 (저자명, 제목, 출판 정보, URL 등 모두 영문 원문 그대로 유지)
- 벤치마크 데이터셋 이름들 (BBH, DROP, PIQA, TriviaQA, MMLU, MATH, HellaSwag, GSM8K)은 고유명사로 원문 유지
- 모델명 및 프레임워크 이름 (DeepSeek-V3, HC, mHC)은 일관성 있게 처리
- 수치 데이터 (2.1%, 2.3%, 3B, 9B, 27B 등)는 원문 그대로 유지
- 그림 및 표 참조는 한국어 조사를 적절히 사용 (그림 6, 그림 7, 그림 8, 표 4)
- 기술 용어는 glossary에 따라 일관되게 번역 (전파 안정성, 순전파 신호 증폭, 역전파 기울기 증폭 등)
- 결론 부분은 논문의 핵심 기여를 요약하는 중요한 섹션으로, 이전 섹션에서 사용된 용어와의 일관성을 유지하며 번역
- 수학적 표기 (PMres, H_l, 등)는 원문 그대로 유지

### Confidence Level

High - 이 청크는 실험 결과, 확장성 분석, 안정성 검증, 결론 및 참고문헌을 포함하고 있습니다. 기술 용어는 glossary를 일관되게 적용했으며, 학술 논문의 결론 부분에 적합한 형식적인 어조를 유지했습니다. 참고문헌은 학술 관례에 따라 원문을 그대로 유지했습니다.

### Transition Notes

- Ending: 이 청크는 참고문헌 섹션의 일부로 종료됩니다 (아직 전체 참고문헌 목록이 완료되지 않음). 다음 청크(chunk 5)는 나머지 참고문헌과 부록 A.1의 모델 사양을 포함할 것으로 예상됩니다.
