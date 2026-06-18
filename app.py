import streamlit as st
import pandas as pd

# 1. 앱 페이지 및 디자인 설정 (나이스 블루 스타일)
st.set_page_config(page_title="대부고 수행평가 성적 검사", layout="wide")

st.markdown("""
<style>
    .stApp { background-color: #f8fafc; font-family: 'Malgun Gothic', sans-serif; }
    h1, h2 { color: #1E3A8A; font-weight: bold; }
    .reportview-container .main .block-container { padding-top: 2rem; }
</style>
""", unsafe_allow_html=True)

st.title("📘 대부고 1학기 전과목 수행평가 성적 검사기")
st.markdown("나이스(NEIS)에서 다운로드한 수행평가 성적 엑셀의 **만점 초과, 최저점수 미달, 점수 누락**을 완벽하게 찾아냅니다.")

# 2. 대부고 1학기 평가계획서 기반 전과목 수행평가 데이터 내장
# 형식을 완벽하게 맞춰두어 드롭다운 메뉴로 자동 연동됩니다.
DAEBU_SUBJECTS = {
    "공통국어1": {
        "시 에세이 쓰기": {"만점": 20, "최저점수": 8},
        "소설 비평문 작성하기": {"만점": 20, "최저점수": 8}
    },
    "문학": {
        "작품 해석 보고서 작성": {"만점": 30, "최저점수": 12},
        "문학 비평문 쓰기": {"만점": 20, "최저점수": 8}
    },
    "화법과 작문": {
        "주제 탐구 보고서 쓰기": {"만점": 25, "최저점수": 9}
    },
    "고전 읽기": {
        "고전 도서 요약하기": {"만점": 30, "최저점수": 12},
        "고전 비평 활동": {"만점": 20, "최저점수": 8}
    },
    "통합사회1": {
        "수업 참여 및 배움일지": {"만점": 10, "최저점수": 4},
        "사회 문제 탐구 포트폴리오": {"만점": 30, "최저점수": 12}
    },
    "세계지리": {
        "지리 정보 분석 보고서": {"만점": 20, "최저점수": 8},
        "기후 변화 대응 포스터": {"만점": 20, "최저점수": 8}
    },
    "윤리와 사상": {
        "사상가 가상 인터뷰 쓰기": {"만점": 25, "최저점수": 10},
        "도덕적 딜레마 토론": {"만점": 15, "최저점수": 6}
    },
    "생활과 윤리": {
        "현대 윤리 문제 에세이": {"만점": 20, "최저점수": 8},
        "윤리적 쟁점 포트폴리오": {"만점": 20, "최저점수": 8}
    },
    "한국사1": {
        "역사 인물 탐구 보고서": {"만점": 20, "최저점수": 8},
        "역사 지도 제작하기": {"만점": 20, "최저점수": 8}
    },
    "공통수학 I": {
        "수학 낱말 사전 만들기": {"만점": 15, "최저점수": 6},
        "수학적 모델링 보고서": {"만점": 25, "최저점수": 10}
    },
    "대수": {
        "함수의 그래프 탐구 보고서": {"만점": 20, "최저점수": 8},
        "수학 문제 해결 능력 평가": {"만점": 20, "최저점수": 8}
    },
    "확률과 통계": {
        "경우의 수 문제 해결하기": {"만점": 20, "최저점수": 6},
        "통계 자료 분석 프로젝트": {"만점": 20, "최저점수": 8}
    },
    "미적분": {
        "미분과 적분의 개념 지도": {"만점": 20, "최저점수": 8},
        "실생활 미적분 문제 해결": {"만점": 20, "최저점수": 8}
    },
    "통합과학1": {
        "과학 실험 보고서 작성": {"만점": 20, "최저점수": 8},
        "과학 탐구 포트폴리오": {"만점": 20, "최저점수": 8}
    },
    "화학Ⅰ": {
        "화학 반응 실험 수행": {"만점": 25, "최저점수": 10},
        "원소 스토링텔링 발표": {"만점": 15, "최저점수": 6}
    },
    "화학Ⅱ": {
        "화학 평형 탐구 활동": {"만점": 30, "최저점수": 12}
    },
    "체육": {
        "체력 측정 및 운동 계획": {"만점": 40, "최저점수": 16},
        "구기 경기 기능 평가": {"만점": 40, "최저점수": 16}
    },
    "음악": {
        "가창 수행 평가": {"만점": 30, "최저점수": 12},
        "음악 감상 비평문": {"만점": 20, "최저점수": 8}
    },
    "미술": {
        "발상과 표현 회화 작업": {"만점": 40, "최저점수": 16},
        "미술 비평 소감문 작성": {"만점": 20, "최저점수": 8}
    },
    "한문 I": {
        "나만의 성어 사전 만들기": {"만점": 20, "최저점수": 4}
    }
}

# 3. 드롭다운 과목 선택 (과목만 고르면 자동으로 내부 기준이 활성화됩니다)
selected_subject = st.selectbox("📋 검사할 과목을 드롭다운에서 선택하세요", list(DAEBU_SUBJECTS.keys()))
subject_rules = DAEBU_SUBJECTS[selected_subject]

# 해당 과목 기준 미리 보여주기
st.info(f"💡 **[{selected_subject}] 수행평가 기준 정보**")
cols = st.columns(len(subject_rules))
for i, (area, limits) in enumerate(subject_rules.items()):
    with cols[i]:
        st.metric(label=f"📌 {area}", value=f"만점: {limits['만점']}점", delta=f"최저: {limits['최저점수']}점", delta_color="inverse")

# 4. 나이스 엑셀 파일 업로드 영역
uploaded_file = st.file_uploader("📂 나이스에서 다운로드한 성적 엑셀 파일(.xlsx)을 넣어주세요", type=["xlsx"])

if uploaded_file:
    try:
        df = pd.read_excel(uploaded_file)
        errors = []

        # 5. 스마트 오입력 검출 로직 시작
        for idx, row in df.iterrows():
            student_name = row.get('성명', row.get('이름', f"{idx+1}번 학생"))
            student_num = row.get('학번', '-')

            for area, limits in subject_rules.items():
                # 엑셀 열 이름에서 수행평가 영역 텍스트가 부분적으로 포함된 열을 똑똑하게 찾습니다.
                target_col = next((c for c in df.columns if area.replace(" ", "") in str(c).replace(" ", "")), None)
                
                if target_col:
                    score = row[target_col]
                    
                    # 1) 점수가 비어있는 경우 (누락)
                    if pd.isna(score) or str(score).strip() == "":
                        errors.append({
                            "학번": student_num, "성명": student_name, "수행평가 항목": area,
                            "오류 유형": "점수 누락(빈칸)", "입력값": "없음", "올바른 기준": "점수 입력 필수"
                        })
                    
                    # 2) 점수가 숫자로 입력된 경우 범위 체크
                    elif isinstance(score, (int, float)) or str(score).replace('.', '', 1).isdigit():
                        score_float = float(score)
                        if score_float > limits["만점"]:
                            errors.append({
                                "학번": student_num, "성명": student_name, "수행평가 항목": area,
                                "오류 유형": "🔴 만점 초과 오류", "입력값": f"{score}점", "올바른 기준": f"{limits['만점']}점 이하"
                            })
                        elif score_float < limits["최저점수"]:
                            errors.append({
                                "학번": student_num, "성명": student_name, "수행평가 항목": area,
                                "오류 유형": "⚠️ 최저점수(기본점수) 미달", "입력값": f"{score}점", "올바른 기준": f"{limits['최저점수']}점 이상 입력"
                            })
                    
                    # 3) '결', '공', '인' 같은 인정문자 외에 이상한 텍스트가 들어간 경우
                    else:
                        clean_score = str(score).strip()
                        if clean_score not in ['결', '공', '인', '미']:
                            errors.append({
                                "학번": student_num, "성명": student_name, "수행평가 항목": area,
                                "오류 유형": "❌ 잘못된 문자 입력", "입력값": score, "올바른 기준": "숫자 또는 결시 기호(결/공/인)"
                            })

        # 6. 결과 리포트 출력
        st.subheader("🔍 검사 결과 분석 리포트")
        if errors:
            st.error(f"총 {len(errors)}개의 입력 오류 및 주의 사항이 발견되었습니다. 아래 내역을 확인해 주세요.")
            error_df = pd.DataFrame(errors)
            st.dataframe(error_df, use_container_width=True)
            
            # 엑셀/CSV로 결과 추출 기능 제공
            csv = error_df.to_csv(index=False).encode('utf-8-sig')
            st.download_button(label="📥 오류 명단 다운로드 (CSV)", data=csv, file_name=f"{selected_subject}_오류리스트.csv", mime="text/csv")
        else:
            st.success(f"🎉 완벽합니다! [{selected_subject}] 나이스 파일에 입력 오류가 전혀 없습니다. 그대로 마감하셔도 좋습니다!")
            
    except Exception as e:
        st.error(f"파일을 읽는 과정에서 에러가 발생했습니다: {e}")
