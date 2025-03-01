from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
# from ..models import Question, Answer
from django.utils import timezone
from django.contrib.auth.decorators import login_required 
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
import os
import json
import openai
import pandas as pd
from langchain.schema import Document, messages_from_dict
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.schema import HumanMessage, AIMessage, SystemMessage

# Create your views here.
# from ..forms import QuestionForm, AnswerForm
## ---------- 데이터베이스 초기화 및 체크
db_path = './data/'
db_initialized = os.path.exists(db_path)

# 데이터베이스가 존재하지만 벡터가 있는지 확인
embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")
db = Chroma(persist_directory=db_path, embedding_function=embeddings)

if not db_initialized or db._collection.count() == 0:  # DB 폴더가 없거나, DB가 비어 있는 경우
    print("🔄 데이터베이스가 없거나 비어 있습니다. 새로 생성 중...")

    # 현재 파일이 위치한 디렉토리 (base_views.py가 있는 폴더)
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    # CSV 파일 절대 경로 설정
    csv_path = os.path.join(BASE_DIR, 'data', 'suksoDF.csv')
    # CSV 파일 읽기
    df = pd.read_csv(csv_path)

    # 벡터화 된 데이터를 DB에 저장
    documents = [
        Document(
            page_content=f"관광지명: {row['name']} 주소: {row['address']}, 소개: {row['overview']}, 숙소정보: {row['generalInfo']}, 객실정보: {row['roomInfo']}, 숙소이미지: {row['imglink']}",
            metadata={"id": idx}
        ) for idx, row in df.iterrows()
    ]

    # 문서 배치를 나누는 함수
    def batch_documents(documents, batch_size):
        for i in range(0, len(documents), batch_size):
            yield documents[i:i + batch_size]

    # 배치 크기 설정
    batch_size = 100

    # 배치로 나누어 처리
    for batch in batch_documents(documents, batch_size):
        try:
            db.add_documents(batch)
            db.persist()
            print(f"✅ Batch of size {batch_size} added successfully.")
        except Exception as e:
            print(f"❌ An error occurred: {e}")
else:
    print("✅ 데이터베이스가 이미 존재하며 벡터가 저장되어 있습니다. 기존 데이터베이스를 사용합니다.")


# LLM 설정
llm = ChatOpenAI(
    model='gpt-4o-2024-08-06'
)

# 챗봇 응답 생성
def get_answer_from_db(user_query, chat_history):
    results = db.similarity_search(user_query, k=5)

    if not results:
        return "데이터베이스에서 유사한 결과를 찾을 수 없습니다."

    context = "\n".join([result.page_content for result in results])

    messages = chat_history.copy()
    messages.append(HumanMessage(content=f"사용자 질문: {user_query}\n\n   \
    참고할 정보:\n{context}\n\n이 정보를 기반으로 정확하게 답변해 주세요.  \
    {user_query}의 요구사항과 {context}\n\n의 정보가 일치하지 않으면 제외하고 답변해 주세요. \
    {context}에 이미지 링크가 있으면, 첫 번째 이미지만 크기를 50% 비율로 변경해 출력해주세요. "))

    response = llm(messages)
    return response.content

# RetrievalQA 객체를 사용하여 검색 및 답변 생성
qa_chain = RetrievalQA.from_chain_type(
    llm=llm, 
    chain_type="map_reduce", 
    retriever=db.as_retriever()
)

# 메인페이지 
def index(request):
   
    return render(request, 'project4/main_chat.html')

# Ajax 요청을 받아서 LLM 답변 반환
def chat_response(request):
    if request.method == "POST":
        user_query = request.POST.get("query", "")
        # print(f'user_query : {user_query}')
        if not user_query:
            return JsonResponse({"error": "질문이 비어 있습니다."}, status=400)

        chat_history = []  # 세션에 저장하려면 request.session 활용 가능
        response = get_answer_from_db(user_query, chat_history)
        # print(f"response : {response}")
        return JsonResponse({"response": response})

    return JsonResponse({"error": "잘못된 요청 방식입니다."}, status=400)