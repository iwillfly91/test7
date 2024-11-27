import streamlit as st
import google.generativeai as genai
from PyPDF2 import PdfReader
import os

def extract_text_from_pdf(pdf_file):
    reader = PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

def main():
    st.title("📚 매뉴얼 해석 도우미")
    
    # API 키 입력
    api_key = st.text_input("Google API 키를 입력하세요:", type="password")
    
    if api_key:
        os.environ['GOOGLE_API_KEY'] = api_key
        genai.configure(api_key=api_key)
        
        # PDF 파일 업로드
        uploaded_file = st.file_uploader("PDF 파일을 업로드하세요", type=['pdf'])
        
        if uploaded_file:
            # PDF에서 텍스트 추출
            text_content = extract_text_from_pdf(uploaded_file)
            
            # Gemini 모델 설정
            model = genai.GenerativeModel('gemini-pro')
            
            # 사용자 질문 입력
            user_question = st.text_input("매뉴얼에 대해 질문하세요:")
            
            if user_question:
                # 프롬프트 구성
                prompt = f"""
                다음 매뉴얼 내용을 참고하여 질문에 답변해주세요:
                매뉴얼 내용: {text_content}
                
                질문: {user_question}
                """
                
                try:
                    # Gemini API 호출
                    response = model.generate_content(prompt)
                    
                    # 응답 표시
                    st.write("🤖 답변:")
                    st.write(response.text)
                    
                except Exception as e:
                    st.error(f"오류가 발생했습니다: {str(e)}")

if __name__ == "__main__":
    main()
