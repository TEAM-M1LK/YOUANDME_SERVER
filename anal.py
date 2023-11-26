import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

def relation(input_text):
    df = pd.read_csv('./conversation.csv')

    model = SentenceTransformer('bert-base-nli-mean-tokens')

    # 입력 문자열을 줄 단위로 분리
    input_lines = input_text.split('\n')

    # 각 유형의 유사도를 저장할 리스트 초기화
    lover_similarity_list = []
    some_similarity_list = []
    friend_similarity_list = []
    business_similarity_list = []

    for line in input_lines:
        # 문장 임베딩 생성
        input_embedding = model.encode([line])

        # 각 유형 간 유사도 계산
        lover_similarity = cosine_similarity(input_embedding, model.encode(df['연인'].astype(str).tolist()))
        some_similarity = cosine_similarity(input_embedding, model.encode(df['썸'].astype(str).tolist()))
        friend_similarity = cosine_similarity(input_embedding, model.encode(df['친구'].astype(str).tolist()))
        business_similarity = cosine_similarity(input_embedding, model.encode(df['비즈니스'].astype(str).tolist()))

        # 결과 분석
        lover_similarity_list.append(lover_similarity[0][0])
        some_similarity_list.append(some_similarity[0][0])
        friend_similarity_list.append(friend_similarity[0][0])
        business_similarity_list.append(business_similarity[0][0])

    # 각 유형의 평균 유사도 계산
    average_lover_similarity = sum(lover_similarity_list) / len(lover_similarity_list)
    average_some_similarity = sum(some_similarity_list) / len(some_similarity_list)
    average_friend_similarity = sum(friend_similarity_list) / len(friend_similarity_list)
    average_business_similarity = sum(business_similarity_list) / len(business_similarity_list)

    # 평균 유사도에 대한 최종 결과 분석
    average_similarities = {
        'Lover': average_lover_similarity,
        'Some': average_some_similarity,
        'Friend': average_friend_similarity,
        'Business': average_business_similarity
    }

    # print(f"The average similarity scores for each type are: {average_similarities}")
    return {max(average_similarities, key=average_similarities.get)}, average_similarities
