"""
교안(강의 커리큘럼) 및 제안서(프로젝트 제안서) PDF 생성 스크립트
professional-doc-generator 프로젝트의 템플릿을 기반으로 A4 PDF를 출력한다.

사용법:
    pip install reportlab
    sudo apt-get install -y fonts-nanum
    python3 scripts/build_pdfs.py

결과물은 output/ 디렉터리에 두 개의 PDF로 저장된다.
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
    PageBreak, KeepTogether, HRFlowable, ListFlowable, ListItem
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
    doc.build(story, onFirstPage=footer, onLaterPages=footer)
    print(f"[OK] 제안서 PDF 생성: {path}")


if __name__ == '__main__':
    import os
    out_dir = 'output'
    os.makedirs(out_dir, exist_ok=True)
    build_lecture(os.path.join(out_dir, '교안_고급시스템아키텍처설계.pdf'))
    build_proposal(os.path.join(out_dir, '제안서_차세대클라우드협업플랫폼.pdf'))
