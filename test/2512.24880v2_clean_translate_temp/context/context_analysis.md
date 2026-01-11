## Document Context Analysis

### Domain
Primary: Technical/Academic - Machine Learning & Deep Neural Networks
Secondary: Computer Science - Artificial Intelligence, Computational Mathematics
Specialized subdomain: Large Language Model Architecture Design, Residual Networks, Optimization Theory

### Audience
Target readers: AI/ML researchers, deep learning engineers, computer science academics
Technical expertise level: Expert
Expected use: Academic reference, research understanding, implementation guidance, technical evaluation

### Tone and Register
Formality: Formal academic
Voice preference: Passive voice dominant (typical research paper style), with occasional active constructions
Narrative person: Third person exclusively
Emotional tone: Neutral, objective, scientifically rigorous with measured confidence in presenting results

### Key Terminology

| Term | Suggested Approach | Notes |
|------|-------------------|-------|
| Manifold-Constrained Hyper-Connections (mHC) | Keep English acronym, translate descriptor | Core concept - 매니폴드 제약 하이퍼 연결 (mHC) |
| Hyper-Connections (HC) | Keep English acronym, translate descriptor | 하이퍼 연결 (HC) |
| Residual Connection | Translate | 잔차 연결 - standard ML term in Korean |
| Identity Mapping | Translate | 항등 사상 or 항등 매핑 |
| Sinkhorn-Knopp Algorithm | Transliterate + keep original | 싱크혼-크놉 알고리즘 |
| Birkhoff Polytope | Transliterate + keep original | 버코프 폴리토프 |
| Doubly Stochastic Matrix | Translate | 이중 확률 행렬 |
| ResNet | Keep acronym | Standard abbreviation in Korean literature |
| Transformer | Keep English | 트랜스포머 (transliterated) - standard in Korean |
| Attention Mechanism | Translate | 어텐션 메커니즘 or 주목 메커니즘 |
| Feed-Forward Network (FFN) | Keep acronym, translate descriptor | 피드포워드 네트워크 (FFN) |
| Mixture-of-Experts (MoE) | Keep acronym, translate descriptor | 전문가 혼합 (MoE) |
| Large Language Model (LLM) | Keep acronym, translate descriptor | 대규모 언어 모델 (LLM) |
| Pre-training | Translate | 사전 학습 |
| Gradient Explosion/Vanishing | Translate | 기울기 폭발/소실 |
| Forward Pass | Translate | 순전파 |
| Backward Pass/Backpropagation | Translate | 역전파 |
| Kernel Fusion | Translate | 커널 융합 |
| Pipeline Parallelism | Translate | 파이프라인 병렬화 |
| Memory Wall | Keep + translate | 메모리 월 (memory wall) |
| DualPipe | Keep as proper name | 듀얼파이프 |
| RMSNorm | Keep acronym | Root Mean Square Normalization |
| TileLang | Keep as proper name | Framework name |
| FLOPs | Keep acronym | Floating Point Operations |
| DeepSeek-V3 | Keep as proper name | Model name |
| Multi-Query Attention (MQA) | Keep acronym, translate | 다중 쿼리 어텐션 (MQA) |
| Grouped-Query Attention (GQA) | Keep acronym, translate | 그룹 쿼리 어텐션 (GQA) |
| Multi-Head Latent Attention (MLA) | Keep acronym, translate | 다중 헤드 잠재 어텐션 (MLA) |
| Spectral Norm | Translate | 스펙트럼 노름 or 스펙트럴 노름 |
| Convex Hull | Translate | 볼록 껍질 |
| Recomputing | Translate | 재계산 |
| Activation | Translate | 활성화 (값) |
| Checkpoint/Checkpointing | Translate | 체크포인트 (기법) |
| BBH, DROP, GSM8K, HellaSwag, MATH, MMLU, PIQA, TriviaQA | Keep as proper names | Benchmark dataset names |
| Micro Design | Translate | 미시적 설계 or 마이크로 설계 |
| Macro Design | Translate | 거시적 설계 or 매크로 설계 |

### Style Guidelines

- **Sentence structure**: Complex academic sentences with multiple clauses; heavy use of mathematical notation; frequent parenthetical references and citations
- **Mathematical notation**: Extensive use of equations numbered sequentially; variables in italics; matrices in bold; subscripts and superscripts critical to meaning
- **Formatting conventions**:
  - Numbered sections with hierarchical subsections (1.1, 1.2, etc.)
  - Tables with clear headers and alignment
  - Figures with detailed captions
  - Equation numbering on right margin
  - Bold for emphasis on key terms and concepts (e.g., **mHC**, **identity mapping**)
  - Italics for mathematical variables and some technical terms
- **Special patterns**:
  - Citation format: (Author et al., Year)
  - Frequent use of "i.e." and "e.g." for clarification
  - Technical definitions using ≔ symbol
  - Use of bullets and numbered lists for clarity
  - Code-style blocks for algorithmic specifications

### Cultural Adaptation Notes

- **Academic conventions**: Korean academic papers typically maintain formal register throughout; equations should remain unchanged but equation references in text need Korean grammar particles (예: 식 (1)에서)
- **Number and notation formats**: Keep Arabic numerals as-is; mathematical notation universal; percentage signs remain (%)
- **Citation style**: Maintain Western citation format (Author, Year) as standard in Korean CS literature
- **Figure/Table references**: Use Korean particles appropriately (그림 1, 표 1, 식 (2))
- **Abbreviations**: First use should include both Korean translation and English acronym in parentheses; subsequent uses can use acronym only
- **Technical depth**: Korean ML audience expects same level of mathematical rigor; do not simplify
- **Honorifics**: Not applicable (third-person academic writing)
- **Measurement units**: No conversion needed; maintain scientific notation as-is

### Translation Recommendations

1. **Preserve mathematical integrity**: All equations, variables, matrices, and mathematical symbols must remain exactly as written. Only translate surrounding explanatory text.

2. **Maintain technical precision**: This is a highly technical paper with specific mathematical concepts. Terms like "doubly stochastic matrix," "Birkhoff polytope," and "Sinkhorn-Knopp algorithm" have established Korean translations in mathematics literature - use standard academic terminology.

3. **Handle acronyms consistently**: On first mention, provide Korean translation followed by English acronym in parentheses. Example: "매니폴드 제약 하이퍼 연결 (Manifold-Constrained Hyper-Connections, mHC)"

4. **Preserve code and pseudocode**: Lines 460-482 contain code-style specifications with data types and operations. Keep these exactly as-is with only comments translated if present.

5. **Table and figure captions**: Translate caption text but preserve all mathematical notation, variable names, and technical parameters within tables.

6. **Bibliography**: Keep references section entirely in original format - author names, titles, and publication venues should not be translated.

7. **Maintain logical flow markers**: Terms like "Specifically," "Furthermore," "Consequently," "Notably" are important for argument structure - translate to appropriate Korean equivalents (구체적으로, 또한, 결과적으로, 특히)

8. **Handle compound technical terms**: Many terms combine multiple concepts (e.g., "doubly stochastic constraint," "memory access overhead"). Ensure Korean translation preserves the precise relationship between components.

9. **Section numbering**: Keep numerical section headings (1, 2, 3.1, etc.) but translate section titles.

10. **Abstract positioning**: Korean academic papers may place abstract after title/authors or include both Korean and English abstracts. Maintain original abstract, potentially adding Korean translation as requested.

11. **Author affiliations and contact**: Keep institutional names in English (DeepSeek-AI) and email addresses unchanged.

12. **Experimental results**: Numbers, percentages, and statistical measures should remain unchanged. Only translate descriptive text around results.

13. **URL and references**: Keep all URLs, DOIs, and arXiv references exactly as written.

14. **Proper nouns for models and frameworks**: DeepSeek-V3, TileLang, DualPipe are proper names - use transliteration where helpful but preserve original for clarity.

15. **Consistency across document**: Given document length (920+ lines), maintain glossary of translated technical terms to ensure consistency, especially for key concepts repeated throughout.

### Potential Translation Challenges

1. **Mathematical compound constructions**: Terms like "composite mapping," "row/column normalization," "convex combination" require precise mathematical Korean terms.

2. **System-level terminology**: Hardware/system terms (memory bandwidth, kernel launch overhead, GPU memory footprint) require specialized Korean IT terminology.

3. **Ambiguous referents**: Extensive use of pronouns and implicit subjects in English may need explicit subjects in Korean for clarity.

4. **Passive voice density**: Korean academic writing accepts passive constructions but may require rephrasing for natural flow in some instances.

5. **Long noun phrases**: English allows complex noun stacking (e.g., "memory access cost bottleneck") which may require restructuring in Korean using possessive particles or relative clauses.

6. **Figure annotations**: Figures 1-8 contain embedded text that should be translated while preserving visual layout intent.

7. **Nested parentheticals**: Frequent use of nested explanations may require sentence restructuring for Korean readability.
