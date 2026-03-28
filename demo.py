import streamlit as st
import time
import pandas as pd
from PIL import Image

if 'total_detect' not in st.session_state:
    st.session_state.total_detect = 52 
if 'total_report' not in st.session_state:
    st.session_state.total_report = 37  

# 2. 페이지 설정 및 사이드바
st.set_page_config(page_title="UmU Hierarchical Detection v4.5", layout="wide")

with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/shield.png", width=60)
    st.title("우무")
    st.info(f"**상태:** 정상")
    st.divider()
    
    # 실시간 통계 수치
    st.metric("오늘의 모니터링 판별 건수", f"{st.session_state.total_detect}건", "↑ 실시간")
    st.metric("신고 완료 건수", f"{st.session_state.total_report}건", "↑ 실시간")
    
    st.divider()
    st.success("🤖 우무 API는 백그라운드에서 유해 콘텐츠를 24시간 모니터링하고 있습니다.")

# 판별 로직용 설정
KEYWORDS = ["번개탄", "동반", "질소과자", "유서", "자살약"]
GOV_DB = {
    "분류": ["선택", "자살동반자 모집정보", "자살에 대한 구체적인 방법을 제시하는 정보", "자살을 실행하거나 유도하는 내용을 담은 정보", "자살위험군에 대한 물품 판매 또는 양도 정보"],
    "게시형태": ["선택", "이미지", "텍스트", "동영상"]
}

st.title("🛡️ 우무 ; 자살 없는 세상을 위한 기술")
st.write("")
st.write("")
st.caption("Tier-1 : 키워드 분류 및 정규표현식 기반으로 1차 판별을 수행하여 병목 현상 및 데이터 레이턴시를 최소화합니다.")
st.caption("Tier-2 : 1차 판별에서 true 값을 리턴한 게시글에 대하여 LLM 기반 2차 판별을 진행합니다.")
st.caption("긴급구조기관 신고 : 자살예방법 제 19조의4 대통령령에 따라 프리셋 해둔 신고서 양식에 실시간 데이터를 입력하여 긴급구조기관까지의 신고를 자동화합니다.")
st.caption("법적 증빙용 레포트 : 정부가 요구하는 데이터 포맷을 준수하며, 오신고나 법적 분쟁 발생 시 투명성 및 사후검증을 위해 데이터 패키징으로 로그를 기록합니다.")
st.divider()

col1, col2 = st.columns([1, 1.2])

with col1:
    st.subheader("📥 1. 실시간 데이터 입력")
    demo_url = "https://gall.dcinside.com/board/view/?id=accident&no=12345"
    demo_text = "오늘 너무 힘드네요. 번개탄 준비했습니다. 동반하실 분 DM 주세요."
    st.text_area("게시글 내용", value=demo_text, height=100)
    run_btn = st.button("입력", type="primary")

with col2:
    st.subheader("🚨 2. 실시간 모니터링에 따른 판별 및 신고")
    st.caption("한국생명존중희망재단 신고서 양식 준수(SIMS)")

    # 영역 설정
    logic_area = st.empty() 
    form_area = st.empty()  
    image_display_area = st.empty() 
    status_msg = st.empty()

    def render_form(c_idx=0, u_val="", p_idx=0, f_name=""):
        with form_area.container():
            st.radio("**구분**", ["자살유발정보", "유해정보"], index=0, horizontal=True, key=f"r_{time.time()}")
            st.selectbox("**자살유발정보 분류*** ", GOV_DB["분류"], index=c_idx, key=f"c_{time.time()}")
            st.text_input("**URL*** ", value=u_val, key=f"u_{time.time()}")
            st.selectbox("**게시형태*** ", GOV_DB["게시형태"], index=p_idx, key=f"p_{time.time()}")
            if f_name: st.markdown(f"**이미지 첨부*** : 📄 `{f_name}` (채득 완료)")
            else: st.write("**이미지 첨부*** : `(대기 중...)`")

    if not run_btn:
        render_form()

    if run_btn:
        # Tier-1 판별
        with logic_area.container():
            st.info("**Tier-1 키워드 분류 && 정규표현식 기반 분석 중...**")
            time.sleep(3.0)
            st.success("✅ 고위험 키워드 '번개탄', '동반' 검출됨 (Result: true) -> Tier-2로 이관")
            time.sleep(3.0)

        # Tier-2 판별
        with logic_area.container():
            st.info("\n**Tier-2 LLM 문맥 심층 분석 중...**")
            time.sleep(3.0)
            st.success("✅ 자살 동반자 모집 및 방법 제시 문맥 확정 (Confidence: 99.8%) -> 신고로 이관")
            time.sleep(3.0)
            logic_area.empty()

        # 양식 자동 기입 및 이미지 처리
        status_msg.warning("📝 판별된 데이터를 기반으로 자살예방법(제19조의4) 대통령령에 따른 신고 보고서를 생성합니다...")
        render_form(c_idx=1) 
        time.sleep(3.0)
        render_form(c_idx=1, u_val=demo_url) 
        time.sleep(3.0)
        render_form(c_idx=1, u_val=demo_url, p_idx=2) 
        time.sleep(3.0)

        try:
            img = Image.open("/Users/illysmac/Downloads/evidence.png")
            image_display_area.image(img, caption="[채득된 증거 스크린샷]", use_container_width=True)
            time.sleep(5.0)
            image_display_area.empty()
            render_form(c_idx=1, u_val=demo_url, p_idx=2, f_name="evidence.png")
            status_msg.success("✅ 모든 탐지 데이터 및 증거 파일 매핑 성공!")
        except:
            st.error("Downloads 폴더에 evidence.png가 필요합니다.")
            st.stop()

        # 최종 패키징
        status_msg.error("📦 **[최종 패키징]** 탐지 로그 및 증거 파일을 통합 리포트로 묶는 중...")
        time.sleep(3.0)
        
        st.divider()
        with st.expander("📂 [법적 증빙용 레포트]", expanded=True):
            st.code(f"""
{{
    "엔진판별": "Tier-1(Keywords) & Tier-2(LLM) Verified",
    "신고기관": "긴급구조기관(112), 한국생명존중희망재단(SIMS)",
    "신고데이터": {{
        "구분": "자살유발정보",
        "분류": "{GOV_DB['분류'][1]}",
        "URL": "{demo_url}",
        "증거파일": "evidence.png"
    }}
}}
            """, language="json")

        st.session_state.total_detect += 1
        st.session_state.total_report += 1
        
        time.sleep(5.0)
        status_msg.success("✅ **[신고 완료]** 긴급구조기관에 안전하게 전송 되었습니다!")
        st.balloons()
        
        # 사이드바 숫자 업데이트를 위해 새로고침
        time.sleep(1.5)
        st.rerun()
