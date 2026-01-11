## Translation Output

### Translated Text

L. Wang, H. Gao, C. Zhao, X. Sun, and D. Dai. Auxiliary-loss-free load balancing strategy for mixture-of-experts. arXiv preprint arXiv:2408.15664, 2024.

L. Wang, Y. Cheng, Y. Shi, Z. Tang, Z. Mo, W. Xie, L. Ma, Y. Xia, J. Xue, F. Yang, et al. Tilelang: A composable tiled programming model for ai systems. arXiv preprint arXiv:2504.17577, 2025.

D. Xiao, Q. Meng, S. Li, and X. Yuan. Muddformer: Breaking residual bottlenecks in transformers via multiway dynamic dense connections. arXiv preprint arXiv:2502.12170, 2025.

S. Xie, R. Girshick, P. Dollár, Z. Tu, and K. He. Aggregated residual transformations for deep neural networks. In Proceedings of the IEEE conference on computer vision and pattern recognition, pages 1492–1500, 2017.

S. Xie, H. Zhang, J. Guo, X. Tan, J. Bian, H. H. Awadalla, A. Menezes, T. Qin, and R. Yan. Residual:
Transformer with dual residual connections, 2023. URL `[https://arxiv.org/abs/2304.1](https://arxiv.org/abs/2304.14802)`
`[4802](https://arxiv.org/abs/2304.14802)` .

F. Yu, D. Wang, E. Shelhamer, and T. Darrell. Deep layer aggregation. In Proceedings of the

IEEE conference on computer vision and pattern recognition, pages 2403–2412, 2018.

R. Zellers, A. Holtzman, Y. Bisk, A. Farhadi, and Y. Choi. HellaSwag: Can a machine really finish your sentence? In A. Korhonen, D. R. Traum, and L. Màrquez, editors, Proceedings of the 57th
Conference of the Association for Computational Linguistics, ACL 2019, Florence, Italy, July
28- August 2, 2019, Volume 1: Long Papers, pages 4791–4800. Association for Computational
Linguistics, 2019. doi: 10.18653/v1/p19-1472. URL `[https://doi.org/10.18653/v1/p1](https://doi.org/10.18653/v1/p19-1472)`
`[9-1472](https://doi.org/10.18653/v1/p19-1472)` .

B. Zhang and R. Sennrich. Root mean square layer normalization. Advances in neural information processing systems, 32, 2019.

D. Zhu, H. Huang, Z. Huang, Y. Zeng, Y. Mao, B. Wu, Q. Min, and X. Zhou. Hyper-connections.

arXiv preprint arXiv:2409.19606, 2024.

18

#### **A. 부록**

**A.1. 상세 모델 명세 및 하이퍼파라미터.**

표 5 | **상세 모델 명세 및 하이퍼파라미터.** 이 표는 DeepSeek-V3 (Liu et al., 2024b) 아키텍처를 기반으로 한 3B, 9B, 27B 모델의 아키텍처 구성을 제시한다. 이는 실험에서 사용된 최적화 및 학습 프로토콜과 함께, 잔차 스트림 확장 및 싱크혼-크놉 설정을 포함한 _m_ HC 및 HC의 구체적인 하이퍼파라미터를 설명한다.

**속성** | 3B | 9B | 27B | 3B 1T 토큰

어휘 파라미터 | 331M | 496M | 662M | 331M
활성 파라미터 | 612M | 1.66B | 4.14B | 612M
전체 파라미터 | 2.97B | 9.18B | 27.0B | 2.97B

계층 수 | 12 | 18 | 30 | 12
선행 밀집 계층 | 1 | 1 | 1 | 1
라우팅 전문가 | 64 | 64 | 72 | 64
활성 전문가 | 6 | 6 | 6 | 6
공유 전문가 | 2 | 2 | 2 | 2
차원 | 1280 | 1920 | 2560 | 1280
FFN 차원 | 896 | 1280 | 1536 | 896
부하 분산 방법 | Loss-Free (Wang et al., 2024) | Loss-Free (Wang et al., 2024) | Loss-Free (Wang et al., 2024) | Loss-Free
어텐션 헤드 | 16 | 24 | 32 | 16
어텐션 차원 | 128 | 128 | 128 | 128
어텐션 변형 | MLA (Liu et al., 2024a) | MLA (Liu et al., 2024a) | MLA (Liu et al., 2024a) | MLA
KV 순위 | 512 | 512 | 512 | 512
위치 임베딩 | RoPE (Su et al., 2024) | RoPE (Su et al., 2024) | RoPE (Su et al., 2024) | RoPE
RoPE 차원 | 64 | 64 | 64 | 64
RoPE _𝜃_ | 10000 | 10000 | 10000 | 10000
계층 정규화 유형 | RMSNorm (Zhang and Sennrich, 2019) | RMSNorm (Zhang and Sennrich, 2019) | RMSNorm (Zhang and Sennrich, 2019) | RMSNorm
계층 정규화 _𝜀_ | 1e-20 | 1e-20 | 1e-20 | 1e-20

_m_ HC/HC 확장 비율 _𝑛_ | 4 | 4 | 4 | 4
_m_ HC/HC 게이팅 인자 초기값 _𝛼_ | 0.01 | 0.01 | 0.01 | 0.01
_m_ HC 싱크혼-크놉 _𝑡_ max | 20 | 20 | 20 | 20

시퀀스 길이 | 4096 | 4096 | 4096 | 4096
어휘 크기 | 129280 | 129280 | 129280 | 129280
배치 크기 | 320 | 512 | 1280 | 2560
학습 스텝 | 30000 | 50000 | 50000 | 100000
학습 토큰 | 39.3B | 105B | 262B | 1.05T
워밍업 스텝 | 2000 | 2000 | 2000 | 2000
최적화기 | AdamW (Loshchilov and Hutter, 2017) | AdamW (Loshchilov and Hutter, 2017) | AdamW (Loshchilov and Hutter, 2017) | AdamW
AdamW 베타 | (0.9, 0.95) | (0.9, 0.95) | (0.9, 0.95) | (0.9, 0.95)
AdamW _𝜀_ | 1e-20 | 1e-20 | 1e-20 | 1e-20
기본 학습률 | 8.6e-4 | 5.9e-4 | 4.0e-4 | 9.0e-4
학습률 스케줄러 | Step | Step | Step | Step
학습률 감소 스텝 비율 | [0.8 ×, 0.9 ×] | [0.8 ×, 0.9 ×] | [0.8 ×, 0.9 ×] | [0.8 ×, 0.9 ×]
학습률 감소율 | [0.316, 0.1] | [0.316, 0.1] | [0.316, 0.1] | [0.316, 0.1]
가중치 감쇠 | 0.1 | 0.1 | 0.1 | 0.1

19

<!-- Extraction Warnings:
  - Detected potential broken math subscripts/superscripts. PDF may use custom fonts for mathematical notation.
  - Found 39 characters from Unicode Private Use Area. These may be custom glyphs that didn't convert properly.
  - Document appears to contain mathematical equations. Consider using OCR-based tools for better equation extraction.
-->

### Translation Notes

- **Bibliography preservation**: All reference entries have been kept in their original English format, following Korean academic conventions for citing Western literature. Author names, publication titles, venues, URLs, and DOIs remain unchanged.

- **Table structure**: Table 5 has been translated with Korean column headers and descriptions while preserving all technical parameters, numerical values, and model names. Mathematical notation (_𝜃_, _𝜀_, _𝑛_, _𝛼_) remains unchanged.

- **Appendix heading**: "A. Appendix" translated to "A. 부록" following standard Korean academic format for appendix sections.

- **Technical parameters**: All hyperparameter values (e.g., 1e-20, 10000, 0.9, 0.95) and model size designations (3B, 9B, 27B) preserved exactly as written.

- **Acronyms and proper names**: Model names (DeepSeek-V3), methods (MLA, RoPE, RMSNorm, AdamW, Loss-Free), and framework names (TileLang) kept in original form with Korean descriptors where appropriate.

- **Citation format**: Reference citations in Table 5 caption maintain standard academic format "(Liu et al., 2024b)" as is standard in Korean ML literature.

- **Table caption**: Translated to Korean while preserving all technical terminology and mathematical notation, explaining the purpose and content of the detailed specifications.

- **Extraction warnings**: The HTML comment containing extraction warnings has been preserved in original English as it represents metadata about document processing, not academic content.

### Confidence Level

High - This final chunk consists primarily of a bibliography (which should remain in English per academic convention) and a technical specifications table with clearly defined parameters. The translation maintains appropriate balance between Korean accessibility for descriptive text and preservation of technical/numerical precision. Terminology is consistent with the glossary and previous chunks' translations.

### Transition Notes

- Ending: This is the final chunk of the document, concluding with Appendix A.1's detailed model specifications table and extraction warnings. The document is complete with this chunk, providing all necessary technical details for model reproducibility alongside the full reference list.
