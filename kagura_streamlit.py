import random
import streamlit as st

st.set_page_config(page_title="카구라 키우기", page_icon="☂️")

# 게임 상태
DEFAULTS = {
    "health": 50,
    "hogam": 30,
    "name": "",
    "day": 0,
    "stage": "name",
    "event": None,
    "log": [],
    "finished": False,
}
for key, value in DEFAULTS.items():
    if key not in st.session_state:
        st.session_state[key] = value


def say(message):
    st.session_state.log.append(message)


def hogam_plus(amount):
    st.session_state.hogam += amount
    say(f"카구라의 호감도: {st.session_state.hogam}")


def health_plus(amount):
    st.session_state.health += amount
    say(f"건강: {st.session_state.health}")


def choose_event():
    st.session_state.event = random.randint(0, 10)
    st.session_state.stage = "event"


def finish_day():
    st.session_state.day += 1
    if st.session_state.day >= 7:
        st.session_state.stage = "ending"
    else:
        choose_event()


def apply_choice(message, affection, extra=None):
    say(message)
    hogam_plus(affection)
    if extra:
        say(extra)
    finish_day()


st.title("☂️ 카구라 키우기")
st.caption("카구라 생일 기념 전날에 허겁지겁 제작한 미소녀 육성 시뮬레이션")
st.caption("제작자: 림시(zerosteatime00)")
st.divider()

# 상태 표시
if st.session_state.stage != "name":
    c1, c2, c3 = st.columns(3)
    c1.metric("건강", st.session_state.health)
    c2.metric("카구라의 호감도", st.session_state.hogam)
    c3.metric("진행", f"{min(st.session_state.day + 1, 7)} / 7일")

# 지금까지의 이야기
with st.expander("지난 이야기 보기", expanded=True):
    if st.session_state.log:
        for line in st.session_state.log:
            st.write(line)
    else:
        st.write("아직 이야기가 시작되지 않았다.")

# 이름 입력
if st.session_state.stage == "name":
    st.write("당신의 이름을 알려 주세요.")
    with st.form("name_form"):
        player_name = st.text_input("이름")
        submitted = st.form_submit_button("게임 시작")
    if submitted and player_name.strip():
        st.session_state.name = player_name.strip()
        say(f"11월 3일, 길을 걷던 당신은 길에서 우산을 들고 치파오를 입은 한 아이를 발견했다.")
        health_plus(0)
        hogam_plus(0)
        st.session_state.stage = "intro"
        st.rerun()
    elif submitted:
        st.warning("이름을 입력해 주세요.")

# 첫 만남
elif st.session_state.stage == "intro":
    st.write("11월 3일, 길에서 우산을 들고 치파오를 입은 한 아이를 발견했다.")
    st.write("어떻게 할까?")
    col1, col2 = st.columns(2)
    if col1.button("1. 키운다", use_container_width=True):
        say("이름은 카구라, 야토족이라고 한다. 집으로 데려갔다.-호감도+20")
        hogam_plus(20)
        choose_event()
        st.rerun()
    if col2.button("2. 지나친다", use_container_width=True):
        say("배가 고프다며 따라왔다. 하는 수 없이 집에 데려갔다.-호감도+10")
        hogam_plus(10)
        choose_event()
        st.rerun()

# 7일간의 랜덤 이벤트
elif st.session_state.stage == "event":
    event = st.session_state.event
    name = st.session_state.name
    st.subheader(f"{st.session_state.day + 1}일 차")

    if event == 0:
        st.write("카구라와 그림을 그렸다.")
        st.write(f"카구라: {name}(이)다, 해!")
        st.write("카구라가 그린 그림에는 당신의 얼굴이 삐뚤빼뚤한 그림체로 그려져 있었다.")
        st.write("뭐라고 할까?")
        a, b = st.columns(2)
        if a.button("1. 고마워!! 너무 마음에 들어!!", use_container_width=True):
            apply_choice(
                f"카구라: (종이 귀퉁이에 이름을 휘갈겨 적는다.){name}, 특별히 주는 거다 해.(카구라가 종이를 찢어서 그림을 주었다.)(호감도+10)",
                10,
            )
            st.rerun()
        if b.button("2. 여기 선이 좀 이상한데...?", use_container_width=True):
            apply_choice(
                "카구라: 그래도 열심히 그렸다, 해..(카구라가 울상을 지었다)(호감도 -10)",
                -10,
            )
            st.rerun()

    elif event == 1:
        st.write("카구라가 길거리에서 친구들과 깡통 차기를 하고 놀다가 넘어져 무릎이 깨진 채로 귀가했다.")
        st.write(f"카구라: {name}, 들어봐라, 해. 나 오늘 깡통 차기 하다가 요땅 때문에 넘어져서 다쳤다 해")
        st.write("어떻게 할까?")
        a, b = st.columns(2)
        if a.button("1. 병원에 데려간다", use_container_width=True):
            apply_choice("카구라: 병원 싫다 해!!(호감도 -30)", -30)
            st.rerun()
        if b.button("2. 일단 상비약으로 치료부터 하고 본다", use_container_width=True):
            apply_choice(f"고맙다 해! {name}(이) 덕분에 하나도 안 아프다 해(호감도 +30)", 30)
            st.rerun()

    elif event == 2:
        st.write("카구라가 길고양이를 주워 왔다.")
        st.write("카구라: 고양이 키우게 해 달라, 해.")
        st.write("어떻게 할까?")
        a, b = st.columns(2)
        if a.button("1. 키우자", use_container_width=True):
            apply_choice("고맙다, 해!! 이름은 다시마 초절임이라고 지을 거다 해!!(호감도+30)", 30)
            st.rerun()
        if b.button("2. 안돼", use_container_width=True):
            apply_choice("역시 그런 거구나 해...풀어주고 오겠다, 해.(호감도-20)", -20)
            st.rerun()

    elif event == 3:
        st.write("놀러 간 카구라를 불러서 집에 오는 길, 아름다운 노을을 보았다.")
        apply_choice(f"{name}, 경치 참 예쁘다 해(호감도 +20)", 20)
        st.rerun()

    elif event == 4:
        st.write("하루 종일 비가 왔다. 카구라는 하루 종일 집에서 심심해 죽을 지경이었다. 카구라를 달래기 위해 다시마 초절임이라도 먹이기로 했다.(호감도 +10)")
        apply_choice("다시마 초절임을 먹었다.", 10)
        st.rerun()

    elif event == 5:
        st.write("실수로 카구라의 발을 밟았다.")
        apply_choice("카구라: 아야!!(호감도 -20)", -20)
        st.rerun()

    elif event == 6:
        right = random.randint(1, 10)
        st.write(f"카구라에게 수학을 가르쳐 주었다. 카구라는 10문제 중 {right}문제를 맞추었다.")
        st.write("카구라: 나 잘 했냐 해?")
        a, b = st.columns(2)
        if a.button("1. 잘했어", use_container_width=True):
            apply_choice("고맙다 해! 근데 수학은 나랑 안 맞는다 해.(호감도+10)", 10)
            st.rerun()
        if b.button("2. 좀만 더 해보자", use_container_width=True):
            apply_choice("아무래도 수학은 아닌 것 같다 해. 지쳤다 해!!(벌렁 드러누웠다.)(호감도-30)", -30)
            st.rerun()

    elif event == 7:
        st.write("카구라: 잠이 안 온다 해.")
        st.write("한밤중 카구라가 방문을 열고 들어왔다. 어떻게 할까?")
        a, b = st.columns(2)
        if a.button("1. 자장가를 불러준다", use_container_width=True):
            apply_choice(f"{name} 노래 잘 부른다 해. 카구라는 그렇게 말하고는 {name}의 어깨를 베고 잠들었다.(호감도+20)", 20)
            st.rerun()
        if b.button("2. 밤이 늦었다고 되돌려보낸다", use_container_width=True):
            apply_choice("그렇지만 잠이 안 온다 해. (카구라는 그렇게 말하고 돌아갔다.)(호감도-10)", -10)
            st.rerun()

    elif event == 8:
        st.write("카구라와 외식을 했다. 유명한 라멘집. 점보 초대형 라면을 5분 안에 다 먹으면 라면 값은 무료다. 카구라가 도전했다.")
        se = st.session_state.get("ramen_time")
        if se is None:
            se = random.randint(1, 8)
            st.session_state.ramen_time = se
        st.write("후루룩 후루룩. 카구라는 면을 계속 삼켰다.")
        st.write(f"카구라는 라면을 {se}분 만에 다 먹었다.")
        if se <= 5:
            st.write("성공했다. 라면값을 치르지 않아도 되었다.")
        else:
            st.write("실패했다. 점보 라면 값까지 치렀다. 5000엔이나 했다.")
        if st.button("다음 날로"):
            st.session_state.pop("ramen_time", None)
            finish_day()
            st.rerun()

    elif event == 9:
        st.write("카구라는 무럭무럭 자랐다.")
        if st.button("다음 날로"):
            finish_day()
            st.rerun()

    elif event == 10:
        st.write("카구라가 키를 잴 때면 늘 한 뼘씩 커져 있었다.")
        if st.button("다음 날로"):
            finish_day()
            st.rerun()

# 엔딩
elif st.session_state.stage == "ending":
    st.title("카구라는 어느덧 성인이 되었다.")
    st.write(f"카구라: 키워줘서 고마웠다 해. {st.session_state.name}의 은혜는 잊지 않겠다 해.")
    st.divider()
    if st.session_state.hogam >= 200:
        st.write("카구라: 사실 나는 신센구미의 치와와랑 결혼하기로 했다 해")
        st.write(f"{st.session_state.name}을 자주 찾아오겠다 해!")
    elif 100 <= st.session_state.hogam < 200:
        st.write("나, 독립한다 해!!")
        st.write("내가 하고 싶은 것들을 하며 살아가겠다 해!")
        st.write("지켜봐 달라 해!")
    else:
        st.write("카구라는 그 말을 마지막으로 야토 별로 돌아갔다.")
    st.success("육성 완료!")
    if st.button("처음부터 다시 하기"):
        for key in list(DEFAULTS):
            st.session_state.pop(key, None)
        st.session_state.pop("ramen_time", None)
        st.rerun()
