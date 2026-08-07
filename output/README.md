# 생성 산출물 (Generated Artifacts)

이 폴더에는 `scripts/build_pdfs.py`가 생성하는 PDF가 저장된다.
바이너리 파일은 Git 저장소에 포함하지 않으며, 아래 명령으로 재생성한다.

## 재생성 방법

```bash
pip install reportlab
sudo apt-get install -y fonts-nanum
python3 scripts/build_pdfs.py
```

## 산출물

| 파일명 | 설명 | 예상 크기 |
|---|---|---|
| `교안_고급시스템아키텍처설계.pdf` | 4주 커리큘럼 + 1주차 상세 강의안 (3페이지) | ~110KB |
| `제안서_차세대클라우드협업플랫폼.pdf` | Nexus 플랫폼 사업 제안서 (4페이지) | ~130KB |

## 문서 구성

### 교안
1. 과정 개요
2. 학습 목표
3. 주차별 커리큘럼 (4주)
4. 평가 방식
- 부록 A: 1주차 상세 강의안 (학습 시나리오, 핵심 개념, 실습 과제, 참고 자료)

### 제안서
1. 프로젝트 개요 · 핵심 KPI
2. 기술 아키텍처 (7-레이어 스택)
3. 추진 일정 (3-Phase, 8개월)
4. 예산 구성 (총 18.5억 원)
5. 리스크 관리
6. 기대 효과
7. 제안 마무리 · 서명란

## 한글 폰트

`fonts-nanum` (Nanum Gothic / Nanum Myeongjo) TrueType을 사용한다.
Noto CJK는 PostScript 아웃라인이라 reportlab에서 로드할 수 없어 제외했다.
