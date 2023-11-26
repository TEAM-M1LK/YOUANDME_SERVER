import re
from anal import relation
from datetime import datetime, timedelta

def extract_messages(text):
    # 날짜와 시간을 추출하는 정규 표현식
    date_time_pattern = re.compile(r'([A-Za-z]{3} \d{1,2}, \d{4} at \d{1,2}:\d{2} (?:AM|PM),)')
    date_time_pattern2 = re.compile(r'(([A-Za-z]+), ([A-Za-z]+) \d{1,2}, \d{4})')

    # 날짜와 시간으로 대화를 분리
    # conversations = conversations.split('\n')[3:]
    conversations = re.sub(date_time_pattern2, '', text)
    conversations = re.split(date_time_pattern,conversations)[1:]
    conversations = [line for line in conversations if line.strip()]
    # print(conversations)

    result = []
    for i in range(0, len(conversations)-1, 2):
        # 발신자와 메시지 추출
        sender_messages = conversations[i+1].split(' : ')
        sender = sender_messages[0]
        message = sender_messages[1]
        # print(sender, ' dfs ', message)
        # print(conversations[i+1])  

        # 대화 정보 저장
        conversation_info = {
            'date_time': conversations[i].strip(),
            'messages': {sender: message}

        }

        result.append(conversation_info)

    return result

def judgment_relation(p1_relation, p2_relation, intervals, person):
    # 1. 둘 다 연인일때 연락 빈도수
    # 2. 한쪽만 연인일때 연락 빈도수, 그리고 한쪽이 만약 비즈니스라면(잦을때, 드물때)
    # 3. 둘다 썸일때 연락 빈도수
    # 4. 한쪽만 썸일 때 연락 빈도수, 그리고 한쪽이 만약 비즈니스라면(2랑 4합치기)(잦을때, 드물때)
    # 5. 둘다 친구일 때 연락 빈도수
    # 6. 한쪽만 친구일때 연락 빈도수, 그리고 한쪽이 비즈니스라면(드물때) 혹은 연인이나 썸이라면(잦을때)
    # 7. 둘다 비즈니스일때
    if(p1_relation == 'Business' and p2_relation == 'Business'):
        return "철저히 공과 사를 나누는 사이"
    elif(p1_relation == 'Business' or p2_relation == 'Business'):
        if(p1_relation == 'Friend' or p2_relation == 'Friend'):
            return ("아직은 서로 더 친해져야 할 단계") if (intervals > 10) else (f"{person[0]}이 조금 더 마음을 열면 짱친이 될지도?" if p1_relation == 'Friend' else f"{person[1]}이 조금 더 마음을 열면 짱친이 될지도?") 
        elif(p1_relation == 'Some' or p2_relation == 'Some' or p1_relation == 'Lover' or p2_relation == 'Lover'):
            return (f"철옹성 같은 철벽을 치는 {person[1]}" if(p1_relation=='Lover' or p1_relation == 'Some') else f"철옹성 같은 철벽을 치는 {person[0]}") if (intervals > 5) else (f"{person[0]}, 너무 들이대는거 아니에요?" if(p1_relation=='Lover' or p1_relation == 'Some') else f"{person[1]}, 너무 들이대는거 아니에요?")
    elif(p1_relation == 'Friend' and p2_relation == 'Friend'):
        return "친하지만 자주 연락하는 사이는 아닙니다" if(intervals > 10) else "누가 뭐래도 우린 친구"
    elif(p1_relation == 'Freind' or p2_relation == 'Friend'):
        if(p1_relation == 'Some' or p2_relation == 'Some' or p1_relation == 'Lover' or p2_relation == 'Lover'):
            return (f"{person[0]}, 혼자만의 짝사랑 중이구나..." if(p1_relation=='Lover' or p1_relation == 'Some') else f"{person[1]}, 혼자만의 짝사랑 중이구나..." ) if (intervals > 5) else (f"{person[0]}, 친해서 더 괴로울 수도, 희망적일 수도 있겠네요." if(p1_relation=='Lover' or p1_relation == 'Some') else f"{person[1]}, 친해서 더 괴로울 수도, 희망적일 수도 있겠네요.")
    if(p1_relation == 'Some' and p2_relation == 'Some'):
        return"둘은 내꺼인 듯 내꺼 아닌 그런 썸을 타는 중?" if(intervals > 3) else "달달한 썸을 타고 계신가봐요."
    elif(p1_relation == 'Some' or p2_relation == 'Some'):
        return (f"{person[0]}, 더 많이 좋아하는 사람이 원래 힘든거다" if(p1_relation == 'Lover') else f"{person[1]}, 더 많이 좋아하는 사람이 원래 힘든거다") if(intervals > 4) else (f"{person[0]}, 좀만 더 하면 꼬실 수 있다!!" if(p1_relation == 'Lover') else f"{person[1]}, 좀만 더 하면 꼬실 수 있다!!")
    else:
        return"혹시 권태기...?" if(intervals>3) else "달달한 사랑을 하고 게신가봐여...."

def run(file_name):
    with open(f"./file/{file_name}", 'r', encoding='utf-8') as file:
        text = file.read()

    conversations = extract_messages(text)

    # 날짜들만 추출
    date_time = [] # 날짜 데이터들의 간격으로 평균 연락 텀을 구하고 관계를 파악하는데 자료로 쓸 예정임
    for conversation in conversations:
        date_time.append(conversation['date_time'].split(',')[0])
    date_time = list(set(date_time))

    # date_time을 datetime으로 바꾸기
    date_objects = [datetime.strptime(date + ' 2023', '%b %d %Y') for date in date_time]
    # print(date_objects)

    # 날짜와 문자열이 포함된 튜플을 정렬
    sorted_dates = sorted(zip(date_objects, date_time), key=lambda x: x[0])
    # print(sorted_dates)

    # datetime 객체만 추출
    date_objects = [date_obj for date_obj, _ in sorted_dates]
    # print(date_objects)

    # 간격 계산을 위한 함수
    def calculate_interval(dates):
        intervals = []
        for i in range(len(dates)-1):
            # 현재 날짜와 다음 날짜의 차이를 구함
            delta = dates[i+1] - dates[i]
            intervals.append(delta.days) 
        return intervals

    intervals = calculate_interval(date_objects)
    # print(sum(intervals)/len(intervals))
    intervals = (sum(intervals)/len(intervals)) if(len(intervals)> 1) else 1000


    #대화 상대 구하기
    all_keys = [msg['messages'].keys() for msg in conversations]
    person = list(set(key for keys in all_keys for key in keys))
    # print(person)

    # 대화 상대 별 보낸 메세지들 저장하기
    person1_message = []
    person2_message = []

    for msg in conversations:
        if person[0] in msg['messages'].keys():
            person1_message.append(msg['messages'][person[0]])
        if person[1] in msg['messages'].keys():
            person2_message.append(msg['messages'][person[1]])

    person1_message = ''.join(map(str, person1_message))
    person2_message = ''.join(map(str, person2_message))
    person1_message = re.sub('\n+', '\n', person1_message)
    person2_message = re.sub('\n+', '\n', person2_message)
    print(person1_message)
    print(person2_message)

    try:
        p1_relation, p1_sim = relation(person1_message)
        p2_relation, p2_sim = relation(person2_message)
        p1_relation = ', '.join(p1_relation)
        p2_relation = ', '.join(p2_relation)
    except Exception as e:    # 모든 예외의 에러 메시지를 출력할 때는 Exception을 사용
        print('예외가 발생했습니다.', e)

    result = judgment_relation(p1_relation, p2_relation, intervals, person)
    print(result)

    return {'intervals' : intervals, 'p1' : p1_relation, 'p2' : p2_relation, 'result' : result, 'p1_sim':p1_sim, 'p2_sim':p2_sim, 'person':person}

# if __name__ == "__main__":
#     relation = run()
#     print('p1 : ', relation['p1'])
#     print('p2 : ', relation['p2'])
#     print('relation is... ', relation['result'])

