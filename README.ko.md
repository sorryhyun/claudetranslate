# Claude Translate 플러그인

**한 번의 명령으로 완성되는 고품질 대용량 문서 번역**

Claude Translate는 Claude Code를 위한 다단계 문서 번역 플러그인입니다. 단 한 줄의 명령어로 수만 단어에 달하는 대용량 문서도 전문 번역가 수준의 품질로 번역할 수 있습니다.

```bash
/translate document.md --target korean
```

이것이 전부입니다. 나머지는 Claude가 알아서 처리합니다.

## 주요 특징

- **원클릭 번역**: 복잡한 설정 없이 한 줄 명령으로 전체 번역 파이프라인 실행
- **대용량 문서 지원**: 책 한 권 분량의 문서도 일관성 있게 번역
- **맥락 인식 번역**: 문서의 도메인, 어조, 전문 용어를 분석하여 번역에 반영
- **용어 일관성 보장**: 전문 용어를 자동 추출하고 문서 전체에 일관되게 적용
- **품질 검증**: 번역 품질을 자동으로 검토하고 개선점 제안
- **19개 언어 지원**: 한국어, 일본어, 중국어, 영어 등 주요 언어 모두 지원

## 왜 Claude Translate인가?

### 기존 AI 번역의 한계

일반적인 AI 번역 도구는 컨텍스트 길이 제한으로 인해 긴 문서를 제대로 처리하지 못합니다. 문서를 단순 분할하면 앞뒤 맥락이 단절되어 번역 품질이 급격히 저하됩니다.

### Claude Translate의 해결책

Claude Translate는 **6단계 파이프라인**을 통해 이 문제를 해결합니다:

| 단계 | 설명 |
|------|------|
| **1. 문맥 분석** | 문서의 도메인, 어조, 전문 용어를 파악 |
| **2. 텍스트 분할** | 문단 경계를 존중하며 적절한 크기로 분할 |
| **3. 요약 및 용어 추출** | 각 청크의 맥락 요약 및 전문 용어 추출 |
| **4. 용어집 번역** | 전문 용어의 일관된 번역 보장 |
| **5. 번역 실행** | 맥락과 용어집을 참조한 고품질 번역 |
| **6. 품질 검증** | 번역 품질 검토 및 개선점 제안 (선택사항) |

각 청크를 번역할 때 이전 청크의 요약과 통합 용어집을 함께 전달하여 **문서 전체의 일관성**을 유지합니다.

## 설치

```bash
# Claude Code에 플러그인 설치
/plugin install ./claudetranslate
```

PDF 파일 번역이 필요한 경우:
```bash
pip install pymupdf
```

## 사용법

### 기본 사용법

```bash
# 문서를 한국어로 번역
/translate report.md --target korean

# 언어 코드 사용
/translate report.md --target ko
```

### 옵션 사용

```bash
# 출력 파일명 지정
/translate docs/guide.txt --target japanese --output docs/guide_ja.txt

# 검증 단계 생략 (더 빠른 처리)
/translate article.md --target spanish --skip-verify
```

### PDF 문서 번역

```bash
# PDF를 한국어로 번역
/translate paper.pdf --target korean
```

## 지원 언어

| 언어 | 코드 | 원어 표기 |
|------|------|-----------|
| 한국어 | ko | 한국어 |
| 일본어 | ja | 日本語 |
| 중국어 (간체) | zh | 中文 |
| 중국어 (번체) | zh-tw | 繁體中文 |
| 영어 | en | English |
| 스페인어 | es | Español |
| 프랑스어 | fr | Français |
| 독일어 | de | Deutsch |
| 포르투갈어 | pt | Português |
| 러시아어 | ru | Русский |
| 아랍어 | ar | العربية |
| 힌디어 | hi | हिन्दी |
| 베트남어 | vi | Tiếng Việt |
| 태국어 | th | ไทย |
| 인도네시아어 | id | Bahasa Indonesia |
| 이탈리아어 | it | Italiano |
| 네덜란드어 | nl | Nederlands |
| 폴란드어 | pl | Polski |
| 터키어 | tr | Türkçe |

## 출력 파일

번역이 완료되면 다음 파일이 생성됩니다:

- **번역본**: `{파일명}_{언어코드}.{확장자}` (예: `report_ko.md`)
- **품질 보고서**: `{파일명}_{언어코드}_report.md` - 용어집, 검증 결과, 품질 지표 포함

## 플러그인 구조

```
claudetranslate/
├── commands/
│   └── translate.md             # /translate 명령어 정의
├── agents/
│   ├── context-analyzer.md      # 문맥 분석 에이전트
│   ├── summarizer.md            # 요약 에이전트
│   ├── glossary-translator.md   # 용어집 번역 에이전트
│   ├── translator.md            # 번역 에이전트
│   └── verifier.md              # 검증 에이전트
├── styles/
│   └── *.md                     # 19개 언어별 스타일 파일
├── mcp/
│   └── ...                      # MCP 서버 (텍스트 분할, 워크스페이스 관리)
└── scripts/
    └── ...                      # 훅 스크립트
```

## 활용 팁

- **대용량 문서**: 50,000단어 이상의 문서는 처리 시간이 오래 걸릴 수 있습니다
- **기술 문서**: 문맥 분석기가 기술 도메인을 자동 인식하여 정확한 번역을 수행합니다
- **중요 문서**: 중요한 문서는 검증 단계를 생략하지 마세요
- **작업 중단 시**: `/compact` 명령 후 재시작하면 이어서 진행됩니다

## 라이선스

MIT License
