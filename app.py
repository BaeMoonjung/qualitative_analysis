import re
import pandas as pd
import streamlit as st
import io

def convert_df(df):
    return df.to_csv().encode('cp949')

# Streamlit 앱 제목 설정
st.title("질적연구분석 프로그램")

# 파일 업로드 기능
uploaded_file = st.file_uploader("텍스트 파일을 업로드하세요", type="txt")

if uploaded_file is not None:
    # 텍스트 파일을 불러와서 content 변수에 저장
    content = uploaded_file.read().decode('utf-8')

    # 텍스트 파일의 내용을 한 문장씩 나누어 리스트로 저장
    sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?|!)\s', content)

    # 딕셔너리 초기화
    qa_dict = {}

    # 문장(질문)마다 답변을 입력받아 딕셔너리에 저장
    st.write("각 문장에 대한 코드를 입력하세요. 적당한 코드가 없은 경우 기타로 코딩하세요:")
    for sentence in sentences:
        answer = st.text_input(f"문장: {sentence}", key=sentence)
        
        # 답변이 존재할 경우에만 딕셔너리에 저장
        if answer:
            if answer in qa_dict:
                qa_dict[answer].append(sentence)
            else:
                qa_dict[answer] = [sentence]

    # "결과 보기" 버튼 추가
    if st.button("결과 보기"):
        if qa_dict:
            # 딕셔너리를 DataFrame으로 변환
            qa_df = pd.DataFrame([(k, q.replace('\n', '').replace('\r', '')) for k, v in qa_dict.items() for q in v], columns=['코드', '문장'])

            # 같은 답변끼리 모아서 정렬 (Answer를 기준으로 정렬)
            qa_df = qa_df.sort_values(by='코드').reset_index(drop=True)

            # print(qa_df)


            # DataFrame 출력
            st.write("분석 결과:")
            st.dataframe(qa_df)

             # DataFrame을 CSV 파일로 저장하기 위한 준비
            qa_df_1 = convert_df(qa_df)
            
            # "저장하기" 버튼 추가
            st.download_button(
            label="Download data as CSV",
            data=qa_df_1,
            file_name='result.csv',
            mime='text/csv',)
        else:
            st.write("답변이 입력되지 않았습니다.")