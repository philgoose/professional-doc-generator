"""
교안(강의 커리큘럼) 및 제안서(프로젝트 제안서) PDF 생성 스크립트
professional-doc-generator 프로젝트의 템플릿을 기반으로 A4 PDF를 출력한다.

사용법:
    pip install reportlab
    sudo apt-get install -y fonts-nanum
    python3 scripts/build_pdfs.py

결과물은 output/ 디렉터리에 두 개의 PDF로 저장된다.
    - 교안_고급시스템아키텍처설계.pdf
    - 제안서_차세대클라우드협업플랫폼.pdf
"""
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor, black, white
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import registerFontFamily
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, HRFlowable, ListFlowable, ListItem
)
from datetime import date

FONT_DIR = '/usr/share/fonts/truetype/nanum'
pdfmetrics.registerFont(TTFont('NotoKR',        f'{FONT_DIR}/NanumGothic.ttf'))
pdfmetrics.registerFont(TTFont('NotoKR-Bold',   f'{FONT_DIR}/NanumGothicBold.ttf'))
pdfmetrics.registerFont(TTFont('NotoKR-Serif',      f'{FONT_DIR}/NanumMyeongjo.ttf'))
pdfmetrics.registerFont(TTFont('NotoKR-Serif-Bold', f'{FONT_DIR}/NanumMyeongjoBold.ttf'))
registerFontFamily('NotoKR', normal='NotoKR', bold='NotoKR-Bold', italic='NotoKR', boldItalic='NotoKR-Bold')
registerFontFamily('NotoKR-Serif', normal='NotoKR-Serif', bold='NotoKR-Serif-Bold', italic='NotoKR-Serif', boldItalic='NotoKR-Serif-Bold')

PRIMARY = HexColor('#0f172a')
ACCENT = HexColor('#0891b2')
SUB_ACCENT = HexColor('#8b5cf6')
MUTED = HexColor('#64748b')
LIGHT = HexColor('#f1f5f9')
BORDER = HexColor('#cbd5e1')


def styles():
    return {
        'title':   ParagraphStyle('title', fontName='NotoKR-Bold', fontSize=26, leading=32, textColor=PRIMARY, alignment=TA_LEFT, spaceAfter=6),
        'h1':      ParagraphStyle('h1', fontName='NotoKR-Bold', fontSize=16, leading=22, textColor=PRIMARY, spaceBefore=18, spaceAfter=8),
        'h2':      ParagraphStyle('h2', fontName='NotoKR-Bold', fontSize=13, leading=18, textColor=ACCENT, spaceBefore=12, spaceAfter=6),
        'body':    ParagraphStyle('body', fontName='NotoKR', fontSize=10.5, leading=17, textColor=HexColor('#1f2937'), alignment=TA_LEFT, spaceAfter=6),
        'meta':    ParagraphStyle('meta', fontName='NotoKR', fontSize=9, leading=13, textColor=MUTED),
        'meta_b':  ParagraphStyle('meta_b', fontName='NotoKR-Bold', fontSize=9, leading=13, textColor=PRIMARY),
    }


def cover_header(title_text, kicker, meta_rows, S):
    story = []
    bar = Table([['']], colWidths=[170*mm], rowHeights=[6])
    bar.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,-1), ACCENT)]))
    story.append(bar)
    story.append(Spacer(1, 14))
    story.append(Paragraph(f"<font color='#0891b2'>{kicker}</font>", S['meta_b']))
    story.append(Spacer(1, 4))
    story.append(Paragraph(title_text, S['title']))
    story.append(HRFlowable(width='100%', thickness=0.6, color=BORDER, spaceBefore=8, spaceAfter=10))
    meta_table = Table(meta_rows, colWidths=[28*mm, 60*mm, 28*mm, 54*mm])
    meta_table.setStyle(TableStyle([
        ('FONT', (0,0), (-1,-1), 'NotoKR', 9),
        ('TEXTCOLOR', (0,0), (0,-1), MUTED),
        ('TEXTCOLOR', (2,0), (2,-1), MUTED),
        ('TEXTCOLOR', (1,0), (1,-1), PRIMARY),
        ('TEXTCOLOR', (3,0), (3,-1), PRIMARY),
        ('FONT', (1,0), (1,-1), 'NotoKR-Bold', 9),
        ('FONT', (3,0), (3,-1), 'NotoKR-Bold', 9),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('LINEBELOW', (0,0), (-1,-1), 0.25, BORDER),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('TOPPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 14))
    return story


def footer(canvas, doc):
    canvas.saveState()
    canvas.setFont('NotoKR', 8)
    canvas.setFillColor(MUTED)
    canvas.drawString(20*mm, 12*mm, "한국기술교육원 · 임채훈 원장")
    canvas.drawRightString(190*mm, 12*mm, f"Page {doc.page}")
    canvas.setStrokeColor(BORDER)
    canvas.setLineWidth(0.3)
    canvas.line(20*mm, 15*mm, 190*mm, 15*mm)
    canvas.restoreState()


def build_lecture(path):
    S = styles()
    doc = SimpleDocTemplate(path, pagesize=A4, leftMargin=20*mm, rightMargin=20*mm, topMargin=20*mm, bottomMargin=22*mm, title="교안 · 고급 시스템 아키텍처 설계", author="임채훈 원장")
    story = []
    story.extend(cover_header(
        "고급 시스템 아키텍처 설계", "LECTURE CURRICULUM · 교안",
        [["과정코드", "KTEA-ARC-401", "총 차시", "4주 · 32시간"],
         ["교육대상", "5년차 이상 개발자", "선수과목", "분산시스템 기초"],
         ["교육기관", "한국기술교육원", "작성자", "임채훈 원장"],
         ["작성일", date.today().strftime("%Y-%m-%d"), "버전", "v1.0"]], S))
    story.append(Paragraph("01. 과정 개요", S['h1']))
    story.append(Paragraph("본 과정은 대규모 트래픽을 처리하는 실무 환경에서 요구되는 시스템 아키텍처 설계 역량을 체계적으로 습득하는 것을 목표로 한다. 이론과 실습을 병행하여 CAP 정리, 마이크로서비스, 성능 최적화, 클라우드 네이티브 아키텍처의 4개 축을 4주에 걸쳐 다룬다.", S['body']))
    story.append(Paragraph("02. 학습 목표", S['h1']))
    goals = [
        "분산 시스템의 근본 원리를 이해하고 CAP 정리에 기반한 설계 결정을 내릴 수 있다.",
        "마이크로서비스 아키텍처의 트레이드오프를 분석하고 실무에 적용할 수 있다.",
        "캐싱, 샤딩, 로드 밸런싱을 조합해 성능 목표를 달성할 수 있다.",
        "제로 트러스트 모델에 기반한 보안 아키텍처를 설계할 수 있다.",
        "Kubernetes 및 GitOps 파이프라인을 활용해 클라우드 네이티브 워크로드를 운영할 수 있다.",
    ]
    story.append(ListFlowable([ListItem(Paragraph(g, S['body']), leftIndent=14) for g in goals], bulletType='bullet', start='•', bulletColor=ACCENT, bulletFontSize=10, leftIndent=8))
    story.append(Paragraph("03. 주차별 커리큘럼", S['h1']))
    tbl_data = [
        ['주차', '주제', '핵심 학습 내용', '실습 과제'],
        ['1주차', '분산 시스템 기초', 'CAP 정리와 실무 적용\n마이크로서비스 패턴\n이벤트 드리븐 아키텍처', 'Kafka 기반 이벤트 파이프라인\n설계 (팀 프로젝트)'],
        ['2주차', '성능 최적화', '캐싱 전략 (Redis, CDN)\n데이터베이스 샤딩\n로드 밸런싱 설계', '10만 TPS 시뮬레이션\n부하 테스트 및 튜닝'],
        ['3주차', '보안 아키텍처', 'OAuth 2.0 / OIDC\nAPI 게이트웨이 보안\n제로 트러스트 모델', 'JWT 인증 서버 구축\n권한 정책 시나리오 설계'],
        ['4주차', '클라우드 네이티브', 'Kubernetes 오케스트레이션\n서버리스 아키텍처\nGitOps 파이프라인', 'EKS 클러스터에\nGitOps 배포 실습'],
    ]
    tbl = Table(tbl_data, colWidths=[16*mm, 30*mm, 62*mm, 62*mm], repeatRows=1)
    tbl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY),
        ('TEXTCOLOR', (0,0), (-1,0), white),
        ('FONT', (0,0), (-1,0), 'NotoKR-Bold', 10),
        ('FONT', (0,1), (-1,-1), 'NotoKR', 9.5),
        ('BACKGROUND', (0,1), (0,-1), LIGHT),
        ('FONT', (0,1), (0,-1), 'NotoKR-Bold', 9.5),
        ('TEXTCOLOR', (0,1), (0,-1), ACCENT),
        ('ALIGN', (0,0), (0,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('GRID', (0,0), (-1,-1), 0.4, BORDER),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(tbl)

    story.append(Paragraph("04. 평가 방식", S['h1']))
    eval_data = [
        ['평가 항목', '비중', '평가 방법'],
        ['출석 및 참여', '20%', '주차별 출석과 토론 참여도'],
        ['주차 실습 과제', '30%', '실무 시나리오 기반 개별 과제'],
        ['팀 프로젝트', '30%', '설계 산출물과 발표'],
        ['최종 평가', '20%', '아키텍처 설계 문서 및 구두 시험'],
    ]
    eval_tbl = Table(eval_data, colWidths=[45*mm, 25*mm, 100*mm], repeatRows=1)
    eval_tbl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), ACCENT),
        ('TEXTCOLOR', (0,0), (-1,0), white),
        ('FONT', (0,0), (-1,0), 'NotoKR-Bold', 10),
        ('FONT', (0,1), (-1,-1), 'NotoKR', 10),
        ('ALIGN', (1,0), (1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [white, LIGHT]),
        ('GRID', (0,0), (-1,-1), 0.4, BORDER),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('TOPPADDING', (0,0), (-1,-1), 7),
        ('BOTTOMPADDING', (0,0), (-1,-1), 7),
    ]))
    story.append(eval_tbl)

    story.append(PageBreak())
    story.append(Paragraph("부록 A. 1주차 상세 강의안 — 분산 시스템 기초", S['h1']))
    story.append(Paragraph("A.1 학습 시나리오", S['h2']))
    story.append(Paragraph("실시간 결제 시스템을 사례로 CAP 정리의 트레이드오프를 시각화한다. 학습자는 3가지 요구사항(가용성 우선, 일관성 우선, 파티션 관용성 우선)에 따라 각각 다른 스토리지 선택이 필요하다는 것을 발견한다.", S['body']))
    story.append(Paragraph("A.2 핵심 개념 정리", S['h2']))
    concepts = [
        ["개념", "정의", "실무 예시"],
        ["Consistency", "모든 노드가 동시에 같은 데이터 반환", "은행 잔액 조회 (RDBMS)"],
        ["Availability", "요청 시 항상 응답을 반환", "SNS 피드 (Cassandra)"],
        ["Partition Tolerance", "네트워크 분할 상황에서도 동작", "글로벌 분산 서비스"],
        ["Eventual Consistency", "일정 시간 후 일관성 수렴", "DNS, S3"],
        ["Saga Pattern", "분산 트랜잭션의 보상 처리", "주문-결제-배송 흐름"],
    ]
    concept_tbl = Table(concepts, colWidths=[38*mm, 68*mm, 64*mm], repeatRows=1)
    concept_tbl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), SUB_ACCENT),
        ('TEXTCOLOR', (0,0), (-1,0), white),
        ('FONT', (0,0), (-1,0), 'NotoKR-Bold', 10),
        ('FONT', (0,1), (-1,-1), 'NotoKR', 9.5),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [white, LIGHT]),
        ('GRID', (0,0), (-1,-1), 0.4, BORDER),
        ('LEFTPADDING', (0,0), (-1,-1), 7),
        ('RIGHTPADDING', (0,0), (-1,-1), 7),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(concept_tbl)
    story.append(Paragraph("A.3 실습 과제 · 지시사항", S['h2']))
    tasks = [
        "요구사항 명세서(4페이지 이상)를 팀별로 작성한다.",
        "Kafka 브로커 3대와 소비자 그룹을 구성해 최소 3개의 토픽을 정의한다.",
        "가상 결제 이벤트 10만 건을 발행하고 지연/처리량을 계측한다.",
        "장애 시나리오(브로커 1대 다운, 네트워크 지연)를 재현하고 대응 방안을 문서화한다.",
    ]
    story.append(ListFlowable([ListItem(Paragraph(t, S['body']), leftIndent=14) for t in tasks], bulletType='1', bulletFormat='%s.', bulletColor=ACCENT, leftIndent=8))
    story.append(Paragraph("A.4 참고 자료", S['h2']))
    refs = [
        "Designing Data-Intensive Applications (Martin Kleppmann, 2017)",
        "Building Microservices (Sam Newman, 2021)",
        "AWS Well-Architected Framework — Reliability Pillar",
        "Kafka: The Definitive Guide 2nd Edition",
    ]
    story.append(ListFlowable([ListItem(Paragraph(r, S['body']), leftIndent=14) for r in refs], bulletType='bullet', start='—', bulletColor=MUTED, leftIndent=8))

    doc.build(story, onFirstPage=footer, onLaterPages=footer)
    print(f"[OK] 교안 PDF 생성: {path}")


def build_proposal(path):
    S = styles()
    doc = SimpleDocTemplate(path, pagesize=A4, leftMargin=20*mm, rightMargin=20*mm, topMargin=20*mm, bottomMargin=22*mm, title="제안서 · 차세대 클라우드 협업 플랫폼 구축", author="임채훈 원장")
    story = []
    story.extend(cover_header(
        "차세대 클라우드 협업 플랫폼 구축 제안서", "PROJECT PROPOSAL · 제안서",
        [["프로젝트명", "Nexus Collaboration Platform", "제안번호", "KTEA-PRP-2026-014"],
         ["수신처", "발주기관 CIO/CTO", "제안기관", "한국기술교육원"],
         ["총 사업비", "1,850,000,000 KRW", "사업기간", "8개월 (2026.03~10)"],
         ["작성일", date.today().strftime("%Y-%m-%d"), "작성자", "임채훈 원장"]], S))
    story.append(Paragraph("1. 프로젝트 개요", S['h1']))
    story.append(Paragraph("본 제안서는 실시간 협업 도구를 통합한 차세대 클라우드 기반 협업 플랫폼 'Nexus'의 구축 계획을 담고 있다. 월 1,000만 MAU 처리와 99.99% 가용성을 보장하며, 문서·화상회의·업무 자동화를 하나의 워크스페이스에서 제공한다.", S['body']))

    story.append(Paragraph("1.1 핵심 목표", S['h2']))
    kpi_data = [
        ['목표 지표', '수치', '측정 기준'],
        ['월간 활성 사용자 (MAU)', '10,000,000', '출시 후 12개월 이내'],
        ['가용성 (SLA)', '99.99%', '연간 다운타임 52분 이하'],
        ['P95 응답 지연', '200ms 이하', '전 API 엔드포인트'],
        ['동시 접속 지원', '500,000 세션', '피크 타임 기준'],
        ['보안 인증', 'ISO 27001 / SOC 2', '출시 6개월 이내 취득'],
    ]
    kpi_tbl = Table(kpi_data, colWidths=[65*mm, 45*mm, 60*mm], repeatRows=1)
    kpi_tbl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY),
        ('TEXTCOLOR', (0,0), (-1,0), white),
        ('FONT', (0,0), (-1,0), 'NotoKR-Bold', 10),
        ('FONT', (0,1), (-1,-1), 'NotoKR', 10),
        ('ALIGN', (1,1), (1,-1), 'CENTER'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [white, LIGHT]),
        ('GRID', (0,0), (-1,-1), 0.4, BORDER),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('TOPPADDING', (0,0), (-1,-1), 7),
        ('BOTTOMPADDING', (0,0), (-1,-1), 7),
    ]))
    story.append(kpi_tbl)

    story.append(Paragraph("2. 기술 아키텍처", S['h1']))
    story.append(Paragraph("마이크로서비스와 이벤트 드리븐 아키텍처를 기반으로 하며, 프론트엔드부터 인프라까지 클라우드 네이티브 표준을 준수한다.", S['body']))
    stack_data = [
        ['레이어', '기술 선택', '선택 근거'],
        ['Frontend', 'React 18 + TypeScript + Vite', '컴포넌트 재사용성과 타입 안정성'],
        ['Backend', 'Node.js + NestJS (BFF)', 'GraphQL 게이트웨이 및 도메인 분리'],
        ['Realtime', 'WebSocket + Redis Pub/Sub', '저지연 협업 이벤트 브로드캐스트'],
        ['Database', 'PostgreSQL 16 + Redis 7', '트랜잭션 정합성과 캐싱 병행'],
        ['Search', 'OpenSearch 2.x', '전문 검색 및 감사 로그 집계'],
        ['Infra', 'AWS EKS + CloudFront + ArgoCD', 'GitOps 기반 무중단 배포'],
        ['Observability', 'OpenTelemetry + Grafana', '분산 트레이싱과 SLO 대시보드'],
    ]
    stack_tbl = Table(stack_data, colWidths=[35*mm, 60*mm, 75*mm], repeatRows=1)
    stack_tbl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), ACCENT),
        ('TEXTCOLOR', (0,0), (-1,0), white),
        ('FONT', (0,0), (-1,0), 'NotoKR-Bold', 10),
        ('FONT', (0,1), (-1,-1), 'NotoKR', 9.5),
        ('FONT', (0,1), (0,-1), 'NotoKR-Bold', 9.5),
        ('TEXTCOLOR', (0,1), (0,-1), PRIMARY),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [white, LIGHT]),
        ('GRID', (0,0), (-1,-1), 0.4, BORDER),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(stack_tbl)

    story.append(PageBreak())
    story.append(Paragraph("3. 추진 일정", S['h1']))
    story.append(Paragraph("총 8개월간 3단계로 나누어 점진적 산출물을 확보한다. 각 단계 종료 시점에 이해관계자 리뷰와 품질 게이트를 통과해야 다음 단계로 이행한다.", S['body']))
    schedule = [
        ['단계', '기간', '주요 산출물', '품질 게이트'],
        ['Phase 1\nMVP 개발', '2026.03 – 05\n(3개월)', '요구사항 명세서\n핵심 도메인 API v1\n기본 UI 프로토타입', '기능 커버리지 70%\n단위 테스트 80%'],
        ['Phase 2\n베타 런칭', '2026.06 – 08\n(3개월)', '실시간 협업 모듈\n권한/과금 시스템\n외부 파일럿 3개사', '동시 접속 5만 검증\n보안 취약점 0건'],
        ['Phase 3\n정식 출시', '2026.09 – 10\n(2개월)', '운영 자동화 파이프라인\n모니터링/알림 체계\n마케팅 랜딩', '99.99% SLA 달성\nISO 27001 심사 통과'],
    ]
    sch_tbl = Table(schedule, colWidths=[26*mm, 30*mm, 58*mm, 56*mm], repeatRows=1)
    sch_tbl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY),
        ('TEXTCOLOR', (0,0), (-1,0), white),
        ('FONT', (0,0), (-1,0), 'NotoKR-Bold', 10),
        ('FONT', (0,1), (-1,-1), 'NotoKR', 9.5),
        ('FONT', (0,1), (0,-1), 'NotoKR-Bold', 10),
        ('TEXTCOLOR', (0,1), (0,-1), ACCENT),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [white, LIGHT]),
        ('GRID', (0,0), (-1,-1), 0.4, BORDER),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('LEFTPADDING', (0,0), (-1,-1), 7),
        ('TOPPADDING', (0,0), (-1,-1), 7),
        ('BOTTOMPADDING', (0,0), (-1,-1), 7),
    ]))
    story.append(sch_tbl)

    story.append(Paragraph("4. 예산 구성", S['h1']))
    budget = [
        ['비목', '금액 (KRW)', '비중', '비고'],
        ['인건비 (개발/디자인 12명)', '1,120,000,000', '60.5%', '8개월 M/M 기준'],
        ['인프라 (AWS/모니터링)', '260,000,000', '14.1%', '베타/정식 운영 포함'],
        ['보안 감사 및 인증 취득', '150,000,000', '8.1%', 'ISO 27001 / SOC 2'],
        ['외주 (디자인/QA)', '180,000,000', '9.7%', '전문 파트너 협업'],
        ['교육 및 예비비', '140,000,000', '7.6%', '리스크 대응'],
        ['총계', '1,850,000,000', '100%', ''],
    ]
    bdg_tbl = Table(budget, colWidths=[60*mm, 40*mm, 20*mm, 50*mm], repeatRows=1)
    bdg_tbl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), ACCENT),
        ('TEXTCOLOR', (0,0), (-1,0), white),
        ('FONT', (0,0), (-1,0), 'NotoKR-Bold', 10),
        ('FONT', (0,1), (-1,-2), 'NotoKR', 9.5),
        ('ALIGN', (1,1), (2,-1), 'RIGHT'),
        ('ROWBACKGROUNDS', (0,1), (-1,-2), [white, LIGHT]),
        ('BACKGROUND', (0,-1), (-1,-1), PRIMARY),
        ('TEXTCOLOR', (0,-1), (-1,-1), white),
        ('FONT', (0,-1), (-1,-1), 'NotoKR-Bold', 10),
        ('GRID', (0,0), (-1,-1), 0.4, BORDER),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('TOPPADDING', (0,0), (-1,-1), 7),
        ('BOTTOMPADDING', (0,0), (-1,-1), 7),
    ]))
    story.append(bdg_tbl)

    story.append(Paragraph("5. 리스크 관리", S['h1']))
    risk = [
        ['리스크', '영향도', '발생확률', '대응 방안'],
        ['핵심 인력 이탈', '높음', '중', '더블 오너십 · 문서 자동화'],
        ['AWS 리전 장애', '높음', '낮음', '멀티 AZ + DR 리전 상시화'],
        ['보안 인증 지연', '중', '중', 'Phase 2 초기 사전 컨설팅'],
        ['외주 품질 편차', '중', '중', 'QA 게이트 및 코드 리뷰 의무화'],
        ['환율/클라우드 요금 변동', '중', '중', '분기별 리저브드 인스턴스 조정'],
    ]
    risk_tbl = Table(risk, colWidths=[52*mm, 22*mm, 22*mm, 74*mm], repeatRows=1)
    risk_tbl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), SUB_ACCENT),
        ('TEXTCOLOR', (0,0), (-1,0), white),
        ('FONT', (0,0), (-1,0), 'NotoKR-Bold', 10),
        ('FONT', (0,1), (-1,-1), 'NotoKR', 9.5),
        ('ALIGN', (1,1), (2,-1), 'CENTER'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [white, LIGHT]),
        ('GRID', (0,0), (-1,-1), 0.4, BORDER),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(risk_tbl)

    story.append(Paragraph("6. 기대 효과", S['h1']))
    benefits = [
        "업무 도구 통합으로 조직 내 컨텍스트 스위칭 30% 감소.",
        "실시간 협업 기능으로 의사결정 사이클 40% 단축.",
        "표준화된 감사 로그와 권한 체계로 규제 대응 비용 25% 절감.",
        "GitOps 기반 무중단 배포로 릴리스 빈도 3배 향상.",
    ]
    story.append(ListFlowable([ListItem(Paragraph(b, S['body']), leftIndent=14) for b in benefits], bulletType='bullet', start='◆', bulletColor=ACCENT, leftIndent=8))

    story.append(Paragraph("7. 제안 마무리", S['h1']))
    story.append(Paragraph("한국기술교육원은 20년 이상의 엔터프라이즈 시스템 구축 경험과 클라우드 네이티브 전문성을 바탕으로, 본 프로젝트를 성공적으로 완수할 준비가 되어 있다. 귀사와의 파트너십을 통해 국내 협업 플랫폼 시장의 새로운 표준을 함께 정립하고자 한다.", S['body']))

    story.append(Spacer(1, 24))
    sign_data = [
        ['', ''],
        [Paragraph("<b>제안 기관</b>", S['meta_b']), Paragraph("<b>제안 책임자</b>", S['meta_b'])],
        [Paragraph("한국기술교육원", S['body']), Paragraph("임채훈 · 원장", S['body'])],
        [Paragraph("서울특별시 강남구 테헤란로 000", S['meta']), Paragraph("chaehun.im@ktea.kr / 02-000-0000", S['meta'])],
    ]
    sign_tbl = Table(sign_data, colWidths=[85*mm, 85*mm])
    sign_tbl.setStyle(TableStyle([
        ('LINEABOVE', (0,1), (-1,1), 0.6, PRIMARY),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(sign_tbl)

    doc.build(story, onFirstPage=footer, onLaterPages=footer)
    print(f"[OK] 제안서 PDF 생성: {path}")


if __name__ == '__main__':
    import os
    out_dir = 'output'
    os.makedirs(out_dir, exist_ok=True)
    build_lecture(os.path.join(out_dir, '교안_고급시스템아키텍처설계.pdf'))
    build_proposal(os.path.join(out_dir, '제안서_차세대클라우드협업플랫폼.pdf'))
