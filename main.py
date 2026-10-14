import streamlit as st

# 1. 페이지 기본 설정 (Page Configuration)
st.set_page_config(
    page_title="MBTI Pokémon Finder | MBTI 포켓몬 단짝 찾기",
    page_icon="🐣",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 2. 커스텀 CSS (따뜻한 크림 & 하늘색 톤 + 큰 글씨 + 현대적인 카드 디자인)
st.markdown("""
    <style>
    /* 전체 배경: 따뜻한 크림색 */
    .stApp {
        background-color: #fdfbf7;
        color: #1e293b;
        font-family: -apple-system, BlinkMacSystemFont, "Pretendard", "Segoe UI", sans-serif;
    }

    /* 메인 타이틀 영역 */
    .title-box {
        text-align: center;
        padding: 24px 16px;
        background: linear-gradient(135deg, #e0f2fe 0%, #fef3c7 100%);
        border-radius: 24px;
        border: 2px solid #bae6fd;
        margin-bottom: 24px;
        box-shadow: 0 8px 20px rgba(56, 189, 248, 0.12);
    }
    .main-title {
        font-size: 2.2rem;
        font-weight: 800;
        color: #0284c7;
        margin-bottom: 6px;
    }
    .sub-title {
        font-size: 1.15rem;
        color: #475569;
        font-weight: 600;
    }

    /* 선택 상자 레이블 및 드롭다운 스타일 */
    .stSelectbox label {
        font-size: 1.25rem !important;
        font-weight: 700 !important;
        color: #0369a1 !important;
    }
    
    /* 포켓몬 결과 카드 */
    .result-card {
        background-color: #ffffff;
        border: 3px solid #7dd3fc;
        border-radius: 24px;
        padding: 28px 20px;
        text-align: center;
        box-shadow: 0 12px 28px rgba(2, 132, 199, 0.1);
        margin-top: 10px;
    }

    /* MBTI 태그 바 */
    .mbti-badge {
        display: inline-block;
        background-color: #e0f2fe;
        color: #0284c7;
        font-size: 1.1rem;
        font-weight: 800;
        padding: 6px 18px;
        border-radius: 30px;
        margin-bottom: 12px;
        border: 1px solid #7dd3fc;
    }

    /* 포켓몬 이름 */
    .poke-name-ko {
        font-size: 2.1rem;
        font-weight: 900;
        color: #0c4a6e;
        margin-bottom: 2px;
    }
    .poke-name-en {
        font-size: 1.1rem;
        color: #64748b;
        font-weight: 600;
        margin-bottom: 16px;
    }

    /* 정보 세션 박스 */
    .info-section {
        background-color: #f0f9ff;
        border-radius: 16px;
        padding: 16px;
        margin: 12px 0;
        text-align: left;
        border-left: 5px solid #38bdf8;
    }
    .info-label {
        font-size: 1.05rem;
        font-weight: 800;
        color: #0369a1;
        margin-bottom: 4px;
    }
    .info-text-ko {
        font-size: 1.05rem;
        line-height: 1.6;
        color: #1e293b;
        margin-bottom: 4px;
        word-break: keep-all;
    }
    .info-text-en {
        font-size: 0.95rem;
        line-height: 1.5;
        color: #475569;
        font-style: italic;
    }

    /* 타입 태그 */
    .type-badge {
        display: inline-block;
        background-color: #fef3c7;
        color: #b45309;
        font-weight: 700;
        font-size: 1rem;
        padding: 4px 14px;
        border-radius: 12px;
        border: 1px solid #fde68a;
    }
    </style>
""", unsafe_allow_html=True)

# 3. 16가지 MBTI & 포켓몬 매칭 데이터베이스
POKEMON_DATA = {
    "ENFP": {
        "ko_name": "피카츄",
        "en_name": "Pikachu",
        "img": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/25.png",
        "type": "전기 (Electric)",
        "features_ko": "밝은 에너지와 뛰어난 친화력, 넘치는 호기심",
        "features_en": "Bright energy, high sociability, and boundless curiosity",
        "reason_ko": "호기심 많고 톡톡 튀는 ENFP의 밝은 기운은 언제나 번개 같은 스파크를 발산하는 피카츄와 최고의 호흡을 자랑합니다. 어디서나 주변 분위기를 순식간에 환하게 만들어줍니다.",
        "reason_en": "ENFP's lively and curious nature perfectly matches Pikachu's sparky energy. Together, they light up any atmosphere in an instant!"
    },
    "ENFJ": {
        "ko_name": "푸린",
        "en_name": "Jigglypuff",
        "img": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/39.png",
        "type": "노말 / 페어리 (Normal / Fairy)",
        "features_ko": "사랑스러운 리더십, 뛰어난 감정 표현력",
        "features_en": "Charming leadership and expressive empathy",
        "reason_ko": "사람들을 다정하게 이끌고 아우르는 ENFJ처럼, 푸린도 감미로운 노래로 주변의 모든 이들을 끌어당기는 사랑스러운 리더입니다.",
        "reason_en": "Just like ENFJ who warmly guides and embraces others, Jigglypuff brings people together with charming melodies and affection."
    },
    "ENTP": {
        "ko_name": "파오리",
        "en_name": "Farfetch'd",
        "img": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/83.png",
        "type": "노말 / 비행 (Normal / Flying)",
        "features_ko": "기발한 엉뚱함, 재치 넘치는 모험가",
        "features_en": "Witty originality and clever unconventionality",
        "reason_ko": "고정관념을 뒤흔드는 아이디어 뱅크 ENTP는 대파 하나를 들고 당당하게 자신만의 방식으로 모험하는 파오리와 독창적인 콤비를 이룹니다.",
        "reason_en": "ENTP's innovative and witty mind pairs brilliantly with Farfetch'd's unique and confident style!"
    },
    "ENTJ": {
        "ko_name": "갸라도스",
        "en_name": "Gyarados",
        "img": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/130.png",
        "type": "물 / 비행 (Water / Flying)",
        "features_ko": "강력한 리더십, 과감한 추진력",
        "features_en": "Powerful charisma and decisive action",
        "reason_ko": "목표가 설정되면 거침없이 난관을 돌파하는 ENTJ의 강인한 리더십은 폭풍을 지배하는 갸라도스의 압도적인 패기와 정상을 향해 나아갑니다.",
        "reason_en": "ENTJ's unstoppable drive and commanding vision find their ultimate match in Gyarados's overwhelming presence."
    },
    "ESFP": {
        "ko_name": "이상해꽃",
        "en_name": "Venusaur",
        "img": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/3.png",
        "type": "풀 / 독 (Grass / Poison)",
        "features_ko": "화사한 만개의 에너지, 사교적인 무드메이커",
        "features_en": "Radiant presence and joyful, blooming vitality",
        "reason_ko": "현재를 즐기며 사람들에게 활력을 전하는 ESFP는 커다란 꽃을 펼쳐 햇살과 긍정적인 기운을 가득 나누는 이상해꽃과 닮았습니다.",
        "reason_en": "ESFP's vibrant and fun-loving spirit blossoms naturally alongside Venusaur's bright and radiant aura."
    },
    "ESFJ": {
        "ko_name": "럭키",
        "en_name": "Chansey",
        "img": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/113.png",
        "type": "노말 (Normal)",
        "features_ko": "헌신적인 다정함, 포근한 수호자",
        "features_en": "Warm devotion and gentle caretaking",
        "reason_ko": "주변 사람들을 세심하게 챙기고 위로를 건네는 ESFJ의 마음씨는 행복의 알을 나누어주며 온정을 베푸는 럭키와 깊은 공감대를 이룹니다.",
        "reason_en": "ESFJ's nurturing, caring nature resonates deeply with Chansey's selfless, happiness-sharing spirit."
    },
    "ESTP": {
        "ko_name": "리자몽",
        "en_name": "Charizard",
        "img": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/6.png",
        "type": "불꽃 / 비행 (Fire / Flying)",
        "features_ko": "화끈한 도전에의 열정, 자유로운 순발력",
        "features_en": "Bold adventurous passion and high-energy action",
        "reason_ko": "스릴 넘치는 모험과 즉각적인 행동을 즐기는 ESTP는 뜨거운 불꽃을 내뿜으며 하늘을 자유롭게 거침없이 누비는 리자몽과 최고의 케미를 보입니다.",
        "reason_en": "ESTP's action-oriented, thrill-seeking energy aligns flawlessly with Charizard's fiery passion and speed."
    },
    "ESTJ": {
        "ko_name": "코뿌리",
        "en_name": "Rhydon",
        "img": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/112.png",
        "type": "땅 / 바위 (Ground / Rock)",
        "features_ko": "철저한 책임감, 흔들리지 않는 신뢰감",
        "features_en": "Rock-solid reliability and strong discipline",
        "reason_ko": "원칙을 지키고 확실한 성과를 이끌어내는 ESTJ는 어떤 충격에도 단단하게 자리를 지키는 코뿌리의 신뢰감 넘치는 모습과 연결됩니다.",
        "reason_en": "ESTJ's structured, goal-driven reliability is perfectly mirrored in Rhydon's unshakable strength."
    },
    "INFP": {
        "ko_name": "이브이",
        "en_name": "Eevee",
        "img": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/133.png",
        "type": "노말 (Normal)",
        "features_ko": "무한한 잠재력, 따뜻하고 풍부한 내면",
        "features_en": "Boundless potential and rich imaginative world",
        "reason_ko": "순수한 감성과 무궁무진한 가능성을 가슴속에 품고 있는 INFP는 다양하고 아름다운 모습으로 진화할 수 있는 이브이 그 자체입니다.",
        "reason_en": "INFP's gentle, imaginative nature reflects Eevee's unique charm and limitless evolution paths."
    },
    "INFJ": {
        "ko_name": "가디안",
        "en_name": "Gardevoir",
        "img": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/282.png",
        "type": "에스퍼 / 페어리 (Psychic / Fairy)",
        "features_ko": "깊은 통찰력, 사려 깊은 조용한 수호자",
        "features_en": "Deep intuition and quiet, dedicated protection",
        "reason_ko": "타인의 감정을 깊게 헤아리고 소중한 신념을 조용히 지켜나가는 INFJ의 통찰은 가디안의 헌신적이고 신비로운 수호자의 모습과 한 쌍을 이룹니다.",
        "reason_en": "INFJ's empathetic intuition and quiet devotion resonate with Gardevoir's protective guardian spirit."
    },
    "INTP": {
        "ko_name": "폴리곤",
        "en_name": "Porygon",
        "img": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/137.png",
        "type": "노말 (Normal)",
        "features_ko": "논리적 분석력, 명확한 구조적 호기심",
        "features_en": "Logical analysis and deep curiosity for systems",
        "reason_ko": "복잡한 세상을 원리와 코드로 파헤치는 지적 탐구자 INTP는 데이터로 정교하게 설계된 폴리곤과 논리적인 조화를 이룹니다.",
        "reason_en": "INTP's analytical and logical mind pairs seamlessly with Porygon's unique digital concept."
    },
    "INTJ": {
        "ko_name": "뮤츠",
        "en_name": "Mewtwo",
        "img": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/150.png",
        "type": "에스퍼 (Psychic)",
        "features_ko": "철저한 용의주도함, 독창적인 통찰",
        "features_en": "Strategic foresight and independent intellect",
        "reason_ko": "멀리 내다보는 전략과 깊은 사색으로 자신만의 길을 개척하는 INTJ의 독립적인 지성은 차원이 다른 비전을 지닌 뮤츠와 잘 맞아떨어집니다.",
        "reason_en": "INTJ's strategic brilliance and self-directed independence reflect Mewtwo's profound intellect."
    },
    "ISFP": {
        "ko_name": "치코리타",
        "en_name": "Chikorita",
        "img": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/152.png",
        "type": "풀 (Grass)",
        "features_ko": "온화한 예술가 감성, 평화로운 따스함",
        "features_en": "Gentle sensibility and peaceful, natural warmth",
        "reason_ko": "자연스럽고 섬세한 아름다움을 가꾸는 ISFP는 상쾌한 향기로 지친 마음에 안식처를 전해주는 치코리타처럼 존재 자체로 힐링이 됩니다.",
        "reason_en": "ISFP's peaceful, artistic, and sensitive spirit is beautifully matched by Chikorita's soothing presence."
    },
    "ISFJ": {
        "ko_name": "밀탱크",
        "en_name": "Miltank",
        "img": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/241.png",
        "type": "노말 (Normal)",
        "features_ko": "묵묵한 성실함, 든든하고 따뜻한 보호",
        "features_en": "Faithful dedication and steadfast support",
        "reason_ko": "자신보다 남을 가만히 보살피고 헌신하는 ISFJ의 온화함은 영양 가득한 우유로 동료들에게 든든한 힘이 되어주는 밀탱크와 연결됩니다.",
        "reason_en": "ISFJ's steady, reliable care and selfless dedication shine alongside Miltank's comforting support."
    },
    "ISTP": {
        "ko_name": "팬텀",
        "en_name": "Gengar",
        "img": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/94.png",
        "type": "고스트 / 독 (Ghost / Poison)",
        "features_ko": "냉철한 문제해결사, 쿨한 임기응변",
        "features_en": "Cool problem-solver with clever adaptability",
        "reason_ko": "상황을 쿨하고 신속하게 분석하여 위기를 재치 있게 넘기는 ISTP는 유유히 나타나 놀라운 기지를 발휘하는 팬텀과 통합니다.",
        "reason_en": "ISTP's pragmatic, quick-thinking style matches Gengar's clever, flexible problem-solving skill."
    },
    "ISTJ": {
        "ko_name": "거북왕",
        "en_name": "Blastoise",
        "img": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/9.png",
        "type": "물 (Water)",
        "features_ko": "철두철미한 원칙주의, 묵직한 신뢰",
        "features_en": "Solid reliability and steadfast duty",
        "reason_ko": "맡은 바 임무를 오차 없이 신중하게 이행하는 ISTJ의 책임감은 단단한 껍질과 물대포로 동료들을 안전하게 수호하는 거북왕과 완벽히 닮았습니다.",
        "reason_en": "ISTJ's disciplined, reliable, and duty-bound nature aligns perfectly with Blastoise's steadfast shield."
    }
}

# 4. 앱 헤더 화면
st.markdown("""
    <div class="title-box">
        <div class="main-title">🐣 MBTI 포켓몬 단짝 찾기</div>
        <div class="sub-title">Find Your Soulmate Pokémon by MBTI</div>
    </div>
""", unsafe_allow_html=True)

st.write("아래에서 당신의 **MBTI 유형**을 선택해 보세요! / Choose your **MBTI type** below!")

# 5. MBTI 선택 드롭다운
mbti_list = list(POKEMON_DATA.keys())
selected_mbti = st.selectbox(
    "👉 MBTI 유형 선택 / Select MBTI:",
    options=mbti_list,
    index=0
)

# 6. 결과 출력 및 축하 효과
if selected_mbti:
    # 축하 화면 효과 (Streamlit Balloons)
    st.balloons()
    
    data = POKEMON_DATA[selected_mbti]
    
    # 포켓몬 결과 카드 시작
    st.markdown(f"""
        <div class="result-card">
            <div class="mbti-badge">✨ {selected_mbti} 추천 단짝 ✨</div>
            <div class="poke-name-ko">{data['ko_name']}</div>
            <div class="poke-name-en">({data['en_name']})</div>
        </div>
    """, unsafe_allow_html=True)
    
    # 이미지 표시 (중앙 정렬)
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image
