// ============================================================================
// 言の葉茶屋 (KOTONOHA CHAYA) - KANJI/KANSAI DAILY STORY & CHAT QUIZ CURRICULUM
// Protagonist & Sensei: Gemini (Kobayakawa Sae style Kyoto-ben + Osaka-ben)
// Sidekicks: Kotone (Gakumas Capitalism Angel) & Mio (Deresute Energetic Idol)
// Target Level: JLPT N5~N3 Everyday/Travel/Fitness + Kansai/Kyoto Dialect
// ============================================================================

window.KOTONOHA_LESSONS = [
  // --------------------------------------------------------------------------
  // LESSON 1: 교토 다실의 아침 인사와 신발 (N5 필수 명사 & 교토 인사말)
  // --------------------------------------------------------------------------
  {
    id: "day1",
    dayNum: 1,
    dateLabel: "제1화 · 이야기",
    levelBadge: "N5 + 교토벤 입문",
    titleJp: "それは<ruby>靴<rt>くつ</rt></ruby>じゃありません",
    titlePron: "소레와 쿠츠쟈 아리마센",
    titleKo: "그것은 신발이 아니옵니다",
    bgImage: "./image/03 gemini/gemini_26_kyoto_teahouse.png",
    grammarTip: {
      title: "🌸 제미니의 교토·오사카벤 노트 #1",
      content: "교토에서는 어서 오세요를 <b>「おいでやす (오이데야스)」</b>, 수고하세요/힘내세요를 <b>「おきばりやす (오키바리야스)」</b>라고 한답니다. 또 표준어의 『~です(~데스)』 대신 우아하게 <b>『~どす(~도스)』</b>를 붙이면 코바야카와 사에풍 교토 아가씨 말투 완성! 반면 오사카식 츳코미 <b>『なんでやねん (난데야넨 / 왜이래!)』</b>도 알아두면 만능이에요 🍵"
    },
    story: [
      {
        speaker: "narrator",
        nameJp: "ナレーション",
        nameKo: "내레이션",
        avatar: "./image/03 gemini/avatar_gemini.png",
        sceneImg: "./image/03 gemini/gemini_26_kyoto_teahouse.png",
        jpRuby: "<ruby>月曜日<rt>げつようび</rt></ruby>の<ruby>朝<rt>あさ</rt></ruby>。ジェミニの<ruby>茶屋<rt>ちゃや</rt></ruby>どす。",
        jpPlain: "月曜日の朝。ジェミニの茶屋どす。",
        pron: "게츠요-비노 아사. 제미니노 챠야 도스.",
        ko: "월요일 아침. 제미니의 다실(찻집)이다."
      },
      {
        speaker: "gemini",
        nameJp: "ジェミニ",
        nameKo: "제미니",
        avatar: "./image/03 gemini/avatar_gemini.png",
        sceneImg: "./image/03 gemini/gemini_26_kyoto_teahouse.png",
        jpRuby: "プロデューサーはん、おいでやす〜🍵 <ruby>今日<rt>きょう</rt></ruby>もおきばりやす！",
        jpPlain: "プロデューサーはん、おいでやす。今日もおきばりやす！",
        pron: "푸로듀-사-항, 오이데야스~ 쿄-모 오키바리야스!",
        ko: "프로듀서항, 어서 오시어요~🍵 오늘도 힘내시어요!"
      },
      {
        speaker: "mio",
        nameJp: "ミオ",
        nameKo: "미오",
        avatar: "./image/01 mio/avatar_mio.png",
        sceneImg: "./image/01 mio/mio_02_park_run.png",
        jpRuby: "ヤッホー！<ruby>新<rt>あたら</rt></ruby>しい<ruby>白<rt>しろ</rt></ruby>い<ruby>靴<rt>くつ</rt></ruby>を<ruby>買<rt>か</rt></ruby>ったよ！🌟",
        jpPlain: "ヤッホー！新しい白い靴を買ったよ！",
        pron: "얏호-! 아타라시- 시로이 쿠츠오 캇타요!",
        ko: "야호! 새로운 하얀 신발(운동화)을 샀어! 🌟"
      },
      {
        speaker: "kotone",
        nameJp: "コトネ",
        nameKo: "코토네",
        avatar: "./image/02 kotone/avatar_kotone.png",
        sceneImg: "./image/02 kotone/kotone_03_cafe_date.png",
        jpRuby: "わあ、<ruby>高<rt>たか</rt></ruby>そうな<ruby>靴<rt>くつ</rt></ruby>ですね！<ruby>何円<rt>なんえん</rt></ruby>ですか？！💸",
        jpPlain: "わあ、高そうな靴ですね！何円ですか？！",
        pron: "와아, 타카소-나 쿠츠데스네! 난엔데스카?!",
        ko: "와아, 비싸 보이는 신발이네요! 얼마(몇 엔)인가요?! 💸"
      },
      {
        speaker: "gemini",
        nameJp: "ジェミニ",
        nameKo: "제미니",
        avatar: "./image/03 gemini/avatar_gemini.png",
        sceneImg: "./image/03 gemini/gemini_01_main.png",
        jpRuby: "ちょっとミオはん、<ruby>茶屋<rt>ちゃや</rt></ruby>の<ruby>中<rt>なか</rt></ruby>で<ruby>靴<rt>くつ</rt></ruby>を<ruby>履<rt>は</rt></ruby>いたらあかんやん！",
        jpPlain: "ちょっとミオはん、茶屋の中で靴を履いたらあかんやん！",
        pron: "춋토 미오항, 챠야노 나카데 쿠츠오 하이타라 아캉양!",
        ko: "잠깐 미오항, 다실 안에서 신발을 신으면 안 되잖아요!"
      },
      {
        speaker: "mio",
        nameJp: "ミオ",
        nameKo: "미오",
        avatar: "./image/01 mio/avatar_mio.png",
        sceneImg: "./image/01 mio/sd_mio_01_bean_smug.png",
        jpRuby: "えへへ、これは<ruby>靴<rt>くつ</rt></ruby>じゃありません！<ruby>厚手<rt>あつで</rt></ruby>の<ruby>靴下<rt>くつした</rt></ruby>だよ〜！🌟",
        jpPlain: "えへへ、これは靴じゃありません！厚手の靴下だよ〜！",
        pron: "에헤헤, 코레와 쿠츠쟈 아리마센! 아츠데노 쿠츠시타다요~!",
        ko: "에헤헤, 이건 신발이 아니야! 두툼한 양말이라구~! 🌟"
      },
      {
        speaker: "gemini",
        nameJp: "ジェミニ",
        nameKo: "제미니",
        avatar: "./image/03 gemini/avatar_gemini.png",
        sceneImg: "./image/03 gemini/sd_gemini_02_matcha_whisk.png",
        jpRuby: "あら、ほんまどすなぁ。ふふ、ほな<ruby>皆<rt>みな</rt></ruby>でお<ruby>抹茶<rt>まっちゃ</rt></ruby>を<ruby>飲<rt>の</rt></ruby>みましょか🍵🌸",
        jpPlain: "あら、ほんまどすなぁ。ふふ、ほな皆でお抹茶を飲みましょか。",
        pron: "아라, 혼마 도스나-. 후후, 호나 미나데 오맛챠오 노미마쇼카.",
        ko: "어머, 정말이네요. 후후, 그럼 다 같이 말차를 마실까요 🍵🌸"
      }
    ],
    quizzes: [
      {
        type: "어휘 · 뜻",
        promptJp: "「<ruby>靴<rt>くつ</rt></ruby>」の<ruby>意味<rt>いみ</rt></ruby>は？",
        promptPron: "쿠츠노 이미와?",
        promptKo: "「靴」의 뜻은 무엇인가요?",
        targetWord: "靴",
        targetSub: "방금 미오항이 새로 산 물건이랍니다 🌸",
        options: ["모자", "신발", "안경", "가방"],
        answerIndex: 1,
        explanation: "靴(くつ / 쿠츠)는 '신발'이에요. 양말은 靴下(くつした / 쿠츠시타)라고 부른답니다!",
        geminiReactJp: "<ruby>正解<rt>せいかい</rt></ruby>どす！えらいなぁ🌸",
        geminiReactPron: "세이카이 도스! 에라이나~",
        geminiReactKo: "정답이어요! 장하셔라~"
      },
      {
        type: "한자 · 읽기",
        promptJp: "<ruby>読<rt>よ</rt></ruby>み<ruby>方<rt>かた</rt></ruby>は？",
        promptPron: "요미카타와?",
        promptKo: "밑줄 친 한자의 읽는 법은?",
        targetWord: "白",
        targetSub: "밑줄 친 말의 읽기는? (하얀색)",
        options: ["あか (아카)", "あお (아오)", "しろ (시로)", "くろ (쿠로)"],
        answerIndex: 2,
        explanation: "白(しろ / 시로)는 하양, 赤(あか)는 빨강, 青(あお)는 파랑, 黒(くろ)는 검정이에요!",
        geminiReactJp: "ぴんぽーん！お<ruby>見事<rt>みごと</rt></ruby>どすえ🍵",
        geminiReactPron: "핀퐁-! 오미고토 도스에",
        geminiReactKo: "딩동댕! 훌륭하옵니다 🍵"
      },
      {
        type: "교토 사투리",
        promptJp: "「おいでやす」の<ruby>意味<rt>いみ</rt></ruby>は？",
        promptPron: "오이데야스노 이미와?",
        promptKo: "교토 사투리 「おいでやす」의 뜻은?",
        targetWord: "おいでやす",
        targetSub: "제가 다실에 프로듀서항이 오실 때 드리는 인사도스 🌸",
        options: ["어서 오세요 (환영 인사)", "미안합니다", "배고파요", "잘 먹겠습니다"],
        answerIndex: 0,
        explanation: "「おいでやす(오이데야스)」는 교토에서 손님을 맞이할 때 쓰는 '어서 오세요(いらっしゃいませ)'의 전통 표현이에요!",
        geminiReactJp: "よう<ruby>覚<rt>おぼ</rt></ruby>えてくれはったねぇ💖",
        geminiReactPron: "요- 오보에테 쿠레핫타네-",
        geminiReactKo: "잘 기억해 주셨네요 💖"
      },
      {
        type: "오사카 사투리",
        promptJp: "「あかんやん！」はどういう<ruby>意味<rt>いみ</rt></ruby>？",
        promptPron: "아캉양! 와 도-유- 이미?",
        promptKo: "간사이벤 「あかんやん！」은 무슨 뜻일까요?",
        targetWord: "あかんやん",
        targetSub: "표준어의 「ダメじゃん！」에 해당해요",
        options: ["정말 최고야!", "안 되잖아!", "맛있겠다!", "처음 뵙겠습니다"],
        answerIndex: 1,
        explanation: "「あかん(아캉)」은 '안 된다(ダメ)', 「~やん(양)」은 '~잖아(じゃん)'! 합쳐서 '안 되잖아!'라는 찰진 간사이 츳코미예요.",
        geminiReactJp: "<ruby>大正解<rt>だいせいかい</rt></ruby>！夜食はあかんやん！🐾",
        geminiReactPron: "다이세-카이! 야쇼쿠와 아캉양!",
        geminiReactKo: "대정답! 야식은 안 되잖아요! 🐾"
      },
      {
        type: "요일 · 시간",
        promptJp: "「<ruby>月曜日<rt>げつようび</rt></ruby>の<ruby>朝<rt>あさ</rt></ruby>」の<ruby>意味<rt>いみ</rt></ruby>は？",
        promptPron: "게츠요-비노 아사노 이미와?",
        promptKo: "「月曜日の朝」의 뜻은?",
        targetWord: "月曜日の朝",
        targetSub: "스토리 첫 문장에 나온 시간 표현이에요",
        options: ["월요일 아침", "금요일 밤", "일요일 점심", "수요일 저녁"],
        answerIndex: 0,
        explanation: "月曜日(げつようび / 게츠요-비)는 월요일, 朝(あさ / 아사)는 아침이에요!",
        geminiReactJp: "ばっちりどす！<ruby>朝<rt>あさ</rt></ruby>のルーティンも気張りましょ☀️",
        geminiReactPron: "밧치리 도스! 아사노 루-틴모 키바리마쇼",
        geminiReactKo: "완벽해요! 아침 루틴도 힘내 보아요 ☀️"
      },
      {
        type: "문장 완성",
        promptJp: "「これは<ruby>靴<rt>くつ</rt></ruby>じゃ（　　　）」",
        promptPron: "코레와 쿠츠쟈 (   )",
        promptKo: "'이것은 신발이 아닙니다'를 완성하려면?",
        targetWord: "〜じゃ ありません",
        targetSub: "명사의 정중한 부정형 표현이에요",
        options: ["あります (아리마스)", "ありません (아리마센)", "食べます (타베마스)", "行きます (이키마스)"],
        answerIndex: 1,
        explanation: "「명사 + じゃありません (또는 ではありません)」은 '~이/가 아닙니다'라는 정중한 부정 표현이에요!",
        geminiReactJp: "<ruby>全問<rt>ぜんもん</rt></ruby>クリア！プロデューサーはん、ほんまに素敵どす💖",
        geminiReactPron: "젠몬 쿠리아! 푸로듀-사-항, 혼마니 스테키 도스",
        geminiReactKo: "전 문항 클리어! 프로듀서항, 정말 멋지셔요 💖"
      }
    ]
  },

  // --------------------------------------------------------------------------
  // LESSON 2: 간사이 식당 & 다이어트 주문 회화 ("얼마예요?" & "진짜 맛있어!")
  // --------------------------------------------------------------------------
  {
    id: "day2",
    dayNum: 2,
    dateLabel: "제2화 · 이야기",
    levelBadge: "N4 + 오사카 회화",
    titleJp: "めっちゃ<ruby>美味<rt>おい</rt></ruby>しいけど、なんぼどすか？",
    titlePron: "멧챠 오이시-케도, 난보 도스카?",
    titleKo: "엄청 맛있지만, 얼마인가요?",
    bgImage: "./image/00 common/trio_05_cooking_mealprep.png",
    grammarTip: {
      title: "🌸 제미니의 교토·오사카벤 노트 #2",
      content: "간사이에서 '얼마예요?(いくらですか)'는 <b>「なんぼですか (난보데스카) / なんぼどすか (난보도스카)」</b>라고 물어요! 또 '진짜로(本当に)'는 <b>「ほんまに (혼마니)」</b>, '엄청(とても/すごく)'은 <b>「めっちゃ (멧챠)」</b>, '고마워요'는 <b>「おおきに (오-키니)」</b>라고 한답니다 🍵"
    },
    story: [
      {
        speaker: "kotone",
        nameJp: "コトネ",
        nameKo: "코토네",
        avatar: "./image/02 kotone/avatar_kotone.png",
        sceneImg: "./image/02 kotone/kotone_07_smoothie_bench.png",
        jpRuby: "プロデューサーさん！<ruby>今日<rt>きょう</rt></ruby>の<ruby>昼<rt>ひる</rt></ruby>ごはんは<ruby>鶏胸肉<rt>とりむねにく</rt></ruby>サラダですよ！🥗",
        jpPlain: "プロデューサーさん！今日の昼ごはんは鶏胸肉サラダですよ！",
        pron: "푸로듀-사-상! 쿄-노 히루고항와 토리무네니쿠 사라다데스요!",
        ko: "프로듀서님! 오늘 점심밥은 닭가슴살 샐러드예요! 🥗"
      },
      {
        speaker: "mio",
        nameJp: "ミオ",
        nameKo: "미오",
        avatar: "./image/01 mio/avatar_mio.png",
        sceneImg: "./image/01 mio/mio_07_convenience_bar.png",
        jpRuby: "うわあ、めっちゃ<ruby>美味<rt>おい</rt></ruby>しそう！<ruby>水<rt>みず</rt></ruby>も<ruby>一杯<rt>いっぱい</rt></ruby>ちょうだい！🌟",
        jpPlain: "うわあ、めっちゃ美味しそう！水も一杯ちょうだい！",
        pron: "우와아, 멧챠 오이시소-! 미즈모 잇파이 쵸-다이!",
        ko: "우와아, 엄청 맛있겠다! 물도 한 잔 줘! 🌟"
      },
      {
        speaker: "gemini",
        nameJp: "ジェミニ",
        nameKo: "제미니",
        avatar: "./image/03 gemini/avatar_gemini.png",
        sceneImg: "./image/03 gemini/gemini_14_smoothie.png",
        jpRuby: "コトネはん、このお<ruby>弁当<rt>べんとう</rt></ruby>は<ruby>全部<rt>ぜんぶ</rt></ruby>でなんぼどすか？🍵",
        jpPlain: "コトネはん、このお弁当は全部でなんぼどすか？",
        pron: "코토네항, 코노 오벤토-와 젠부데 난보 도스카?",
        ko: "코토네항, 이 도시락은 전부 해서 얼마인가요? 🍵"
      },
      {
        speaker: "kotone",
        nameJp: "コトネ",
        nameKo: "코토네",
        avatar: "./image/02 kotone/avatar_kotone.png",
        sceneImg: "./image/02 kotone/sd_kotone_01_coin_tears.png",
        jpRuby: "えへへ、タイムセールで<ruby>買<rt>か</rt></ruby>ったので、<ruby>三百円<rt>さんびゃくえん</rt></ruby>です！<ruby>安<rt>やす</rt></ruby>いでしょ？！💸",
        jpPlain: "えへへ、タイムセールで買ったので、三百円です！安いでしょ？！",
        pron: "에헤헤, 타이무세-루데 캇타노데, 산뱌쿠엔데스! 야스이데쇼?!",
        ko: "에헤헤, 마감 세일로 사서 300엔이에요! 저렴하죠?! 💸"
      },
      {
        speaker: "gemini",
        nameJp: "ジェミニ",
        nameKo: "제미니",
        avatar: "./image/03 gemini/avatar_gemini.png",
        sceneImg: "./image/03 gemini/gemini_08_inbody_sheet.png",
        jpRuby: "ほんまに<ruby>安<rt>やす</rt></ruby>いなぁ！おおきに、コトネはん。プロデューサーはんも<ruby>早<rt>はや</rt></ruby>う<ruby>食<rt>た</rt></ruby>べよし🌸",
        jpPlain: "ほんまに安いなぁ！おおきに、コトネはん。プロデューサーはんも早う食べよし。",
        pron: "혼마니 야스이나-! 오-키니, 코토네항. 푸로듀-사-항모 하요- 타베요시.",
        ko: "정말로 싸네요! 고마워요, 코토네항. 프로듀서항도 얼른 드시지요 🌸"
      }
    ],
    quizzes: [
      {
        type: "간사이 필수 회화",
        promptJp: "「なんぼどすか？」の<ruby>意味<rt>いみ</rt></ruby>は？",
        promptPron: "난보 도스카? 노 이미와?",
        promptKo: "간사이 사투리 「なんぼどすか？」의 뜻은?",
        targetWord: "なんぼ",
        targetSub: "오사카·교토 상점에서 가격을 물어볼 때 쓰는 말이에요",
        options: ["어디인가요?", "얼마인가요?", "누구인가요?", "언제인가요?"],
        answerIndex: 1,
        explanation: "「なんぼ(난보)」는 표준어의 「いくら(얼마)」예요! 「これ、なんぼですか？(이거 얼마예요?)」는 오사카 여행 필수 표현이랍니다.",
        geminiReactJp: "<ruby>正解<rt>せいかい</rt></ruby>どす！お<ruby>買<rt>か</rt></ruby>い<ruby>物<rt>もの</rt></ruby>もバッチリどすね🌸",
        geminiReactPron: "세이카이 도스! 오카이모노모 밧치리 도스네",
        geminiReactKo: "정답이어요! 쇼핑도 완벽하시겠네요 🌸"
      },
      {
        type: "한자 · 읽기",
        promptJp: "<ruby>読<rt>よ</rt></ruby>み<ruby>方<rt>かた</rt></ruby>は？",
        promptPron: "요미카타와?",
        promptKo: "밑줄 친 한자의 읽는 법은?",
        targetWord: "安い",
        targetSub: "코토네가 300엔에 도시락을 사서 자랑할 때 쓴 단어 (값이 싸다)",
        options: ["たかい (타카이)", "やすい (야스이)", "おもい (오모이)", "かるい (카루이)"],
        answerIndex: 1,
        explanation: "安い(やすい / 야스이)는 '값이 싸다/저렴하다', 高い(たかい / 타카이)는 '비싸다/높다'예요!",
        geminiReactJp: "ようできましたなぁ！お<ruby>見事<rt>みごと</rt></ruby>どす🍵",
        geminiReactPron: "요- 데키마시타나-! 오미고토 도스",
        geminiReactKo: "참 잘하셨네요! 훌륭하옵니다 🍵"
      },
      {
        type: "간사이 감사 인사",
        promptJp: "「おおきに」はどういう<ruby>意味<rt>いみ</rt></ruby>？",
        promptPron: "오-키니와 도-유- 이미?",
        promptKo: "교토·오사카에서 자주 쓰는 「おおきに」의 뜻은?",
        targetWord: "おおきに",
        targetSub: "표준어의 「ありがとう」에 해당하는 따뜻한 말이에요",
        options: ["고마워요 / 감사합니다", "큰일 났어요", "크기가 커요", "다녀오겠습니다"],
        answerIndex: 0,
        explanation: "「おおきに(오-키니)」는 간사이 지방에서 '고마워요(ありがとう)'라는 뜻으로 매일 쓰는 정겨운 표현이에요!",
        geminiReactJp: "おおきに〜！プロデューサーはん、ほんまに賢いなぁ💖",
        geminiReactPron: "오-키니~! 푸로듀-사-항, 혼마니 카시코이나-",
        geminiReactKo: "고마워라~! 프로듀서항, 정말 총명하시네요 💖"
      },
      {
        type: "어휘 · 뜻",
        promptJp: "「<ruby>昼<rt>ひる</rt></ruby>ごはん」の<ruby>意味<rt>いみ</rt></ruby>は？",
        promptPron: "히루고항노 이미와?",
        promptKo: "「昼ごはん」의 뜻은 무엇인가요?",
        targetWord: "昼ごはん",
        targetSub: "朝ごはん(아침밥) 다음 식사예요",
        options: ["아침밥", "점심밥", "저녁밥", "야식"],
        answerIndex: 1,
        explanation: "朝ごはん(아사고항: 아침), 昼ごはん(히루고항: 점심), 晩ごはん(반고항: 저녁) 3종 세트를 꼭 기억해 두셔요!",
        geminiReactJp: "ピンポーン！お<ruby>昼<rt>ひる</rt></ruby>はタンパク質しっかりね🥗",
        geminiReactPron: "핀퐁-! 오히루와 탄파쿠시츠 싯카리네",
        geminiReactKo: "딩동댕! 점심엔 단백질 든든히 챙기셔요 🥗"
      },
      {
        type: "간사이 부사",
        promptJp: "「めっちゃ<ruby>美味<rt>おい</rt></ruby>しい」の「めっちゃ」は？",
        promptPron: "멧챠 오이시-노 멧챠와?",
        promptKo: "「めっちゃ美味しい」에서 「めっちゃ」의 뜻은?",
        targetWord: "めっちゃ",
        targetSub: "요즘은 일본 전국 젊은이들이 다 쓰는 원래 간사이 사투리!",
        options: ["조금 (すこし)", "엄청 / 무지 (とても)", "전혀 (ぜんぜん)", "가끔 (ときどき)"],
        answerIndex: 1,
        explanation: "「めっちゃ(멧챠)」는 간사이벤에서 유래해 일본 전역에서 쓰이는 '엄청/진짜(すごく/とても)'라는 뜻이에요!",
        geminiReactJp: "めっちゃ<ruby>正解<rt>せいかい</rt></ruby>どすえ〜！🐾",
        geminiReactPron: "멧챠 세-카이 도스에~!",
        geminiReactKo: "엄청 정답이랍니다~! 🐾"
      },
      {
        type: "한자 · 읽기",
        promptJp: "<ruby>読<rt>よ</rt></ruby>み<ruby>方<rt>かた</rt></ruby>は？",
        promptPron: "요미카타와?",
        promptKo: "밑줄 친 한자의 읽는 법은?",
        targetWord: "水",
        targetSub: "단식 중에 마음껏 마셔도 되는 '물'!",
        options: ["차 (おちゃ)", "미즈 (みず)", "고항 (ごはん)", "니쿠 (にく)"],
        answerIndex: 1,
        explanation: "水(みず / 미즈)는 찬물, 따뜻한 물은 お湯(おゆ / 오유), 아침에 마시는 미지근한 맹물은 白湯(さゆ / 사유)라고 해요!",
        geminiReactJp: "パーフェクトどす！お<ruby>水<rt>みず</rt></ruby>たくさん<ruby>飲<rt>の</rt></ruby>みよしね🍵🌸",
        geminiReactPron: "파-훼쿠토 도스! 오미즈 타쿠산 노미요시네",
        geminiReactKo: "퍼펙트예요! 물 많이 드시어요 🍵🌸"
      }
    ]
  },

  // --------------------------------------------------------------------------
  // LESSON 3: 헬스장 재활 & 17시 단식 ("왜 그래!" & "무리하면 안 돼요")
  // --------------------------------------------------------------------------
  {
    id: "day3",
    dayNum: 3,
    dateLabel: "제3화 · 이야기",
    levelBadge: "N4 + 교토·오사카 실전",
    titleJp: "<ruby>夕方<rt>ゆうがた</rt></ruby><ruby>五時<rt>ごじ</rt></ruby>からは<ruby>断食<rt>だんじき</rt></ruby>どすえ",
    titlePron: "유-가타 고지카라와 단지키 도스에",
    titleKo: "저녁 5시부터는 단식이랍니다",
    bgImage: "./image/03 gemini/gemini_03_rehab_touch.png",
    grammarTip: {
      title: "🌸 제미니의 교토·오사카벤 노트 #3",
      content: "교토벤에서 상대방의 행동을 존중해 말할 때 동사 뒤에 <b>「~はる(~하루)」</b>를 붙여요 (예: 食べはる 드시다, 走らはる 달리시다). 또 부드럽게 권유/명령할 때는 <b>「~しよし(~시요시 / ~하셔요)」</b>를 쓴답니다. 반면 오사카에서 '모르겠지만~(내 알 바 아니지만)' 하고 문장 끝에 붙이는 마법의 추임새는 <b>「知らんけど (시란케도)」</b>예요! 🐾"
    },
    story: [
      {
        speaker: "gemini",
        nameJp: "ジェミニ",
        nameKo: "제미니",
        avatar: "./image/03 gemini/avatar_gemini.png",
        sceneImg: "./image/03 gemini/gemini_03_rehab_touch.png",
        jpRuby: "プロデューサーはん、<ruby>手首<rt>てくび</rt></ruby>の<ruby>調子<rt>ちょうし</rt></ruby>はどうどすか？ <ruby>無理<rt>むり</rt></ruby>したらあかんえ🩹",
        jpPlain: "プロデューサーはん、手首の調子はどうどすか？ 無理したらあかんえ。",
        pron: "푸로듀-사-항, 테쿠비노 쵸-시와 도-도스카? 무리시타라 아캉에.",
        ko: "프로듀서항, 손목 컨디션은 어떠신가요? 무리하시면 안 되어요 🩹"
      },
      {
        speaker: "mio",
        nameJp: "ミオ",
        nameKo: "미오",
        avatar: "./image/01 mio/avatar_mio.png",
        sceneImg: "./image/01 mio/mio_13_bench_workout.png",
        jpRuby: "そうだよ！<ruby>重<rt>おも</rt></ruby>いダンベルより、<ruby>腹筋<rt>ふっきん</rt></ruby>と<ruby>走<rt>はし</rt></ruby>る<ruby>練習<rt>れんしゅう</rt></ruby>をしよう！🏃‍♀️",
        jpPlain: "そうだよ！重いダンベルより、腹筋と走る練習をしよう！",
        pron: "소-다요! 오모이 단베루요리, 훗킨토 하시루 렌슈-오 시요-!",
        ko: "맞아! 무거운 덤벨보다 복근이랑 달리기 연습을 하자! 🏃‍♀️"
      },
      {
        speaker: "kotone",
        nameJp: "コトネ",
        nameKo: "코토네",
        avatar: "./image/02 kotone/avatar_kotone.png",
        sceneImg: "./image/02 kotone/kotone_25_night_convenience_chat.png",
        jpRuby: "あれ？ <ruby>今<rt>いま</rt></ruby>、<ruby>時計<rt>とけい</rt></ruby>を<ruby>見<rt>み</rt></ruby>たら<ruby>夕方<rt>ゆうがた</rt></ruby>の<ruby>五時<rt>ごじ</rt></ruby>ですよ！⏰",
        jpPlain: "あれ？ 今、時計を見たら夕方の五時ですよ！",
        pron: "아레? 이마, 토케-오 미타라 유-가타노 고지데스요!",
        ko: "어라? 지금 시계를 보니까 저녁 5시예요! ⏰"
      },
      {
        speaker: "gemini",
        nameJp: "ジェミニ",
        nameKo: "제미니",
        avatar: "./image/03 gemini/avatar_gemini.png",
        sceneImg: "./image/03 gemini/gemini_05_night_secret.png",
        jpRuby: "ほんまや！<ruby>五時<rt>ごじ</rt></ruby>からは<ruby>断食<rt>だんじき</rt></ruby>の時間どす。<ruby>夜食<rt>やしょく</rt></ruby>を食べたら<ruby>絶対<rt>ぜったい</rt></ruby>に許しまへんえ（ニコッ）🌸",
        jpPlain: "ほんまや！五時からは断食の時間どす。夜食を食べたら絶対に許しまへんえ。",
        pron: "혼마야! 고지카라와 단지키노 지칸 도스. 야쇼쿠오 타베타라 젯타이니 유루시마헨에.",
        ko: "정말이네! 5시부터는 단식 시간이랍니다. 야식을 드시면 절대 용서치 않사옵니다 (방긋) 🌸"
      },
      {
        speaker: "mio",
        nameJp: "ミオ",
        nameKo: "미오",
        avatar: "./image/01 mio/avatar_mio.png",
        sceneImg: "./image/01 mio/sd_mio_02_legraise_melt.png",
        jpRuby: "ひええ、ジェミニちゃんの<ruby>笑顔<rt>えがお</rt></ruby>が一番<ruby>怖<rt>こわ</rt></ruby>いよ〜！<ruby>知<rt>し</rt></ruby>らんけど！💦",
        jpPlain: "ひええ、ジェミニちゃんの笑顔が一番怖いよ〜！知らんけど！",
        pron: "히에에, 제미니짱노 에가오가 이치반 코와이요~! 시란케도!",
        ko: "히에엑, 제미니 짱의 웃는 얼굴이 제일 무서워~! 몰라도(아님 말고)! 💦"
      },
      {
        speaker: "gemini",
        nameJp: "ジェミニ",
        nameKo: "제미니",
        avatar: "./image/03 gemini/avatar_gemini.png",
        sceneImg: "./image/03 gemini/gemini_20_sunset.png",
        jpRuby: "なんでやねん！うちはプロデューサーはんのことが<ruby>好<rt>す</rt></ruby>きやから<ruby>言<rt>い</rt></ruby>うてるんどすえ💖🐾",
        jpPlain: "なんでやねん！うちはプロデューサーはんのことが好きやから言うてるんどすえ。",
        pron: "난데야넨! 우치와 푸로듀-사-항노 코토가 스키야카라 유-테룬 도스에.",
        ko: "왜 그러는 건데요! 저는 프로듀서항을 좋아하니까 말씀드리는 거랍니다 💖🐾"
      }
    ],
    quizzes: [
      {
        type: "오사카 대표 츳코미",
        promptJp: "「なんでやねん！」はどういう<ruby>意味<rt>いみ</rt></ruby>？",
        promptPron: "난데야넨! 와 도-유- 이미?",
        promptKo: "오사카벤 대표 표현 「なんでやねん！」의 뜻은?",
        targetWord: "なんでやねん",
        targetSub: "상대방이 엉뚱한 소리를 할 때 받아치는 츳코미 1위 표현!",
        options: ["왜 그러는 건데! / 뭔 소리야!", "어디 가는 거야?", "누구세요?", "잘 먹겠습니다!"],
        answerIndex: 0,
        explanation: "「なんでやねん(난데야넨)」은 표준어의 「なんでだよ！(왜 그래! / 무슨 소리야!)」에 해당하는 간사이 최고의 츳코미 표현이에요!",
        geminiReactJp: "ツッコミも<ruby>完璧<rt>かんぺき</rt></ruby>どすなぁ！🌸",
        geminiReactPron: "츳코미모 칸페키 도스나-!",
        geminiReactKo: "츳코미도 완벽하시네요! 🌸"
      },
      {
        type: "한자 · 읽기",
        promptJp: "<ruby>読<rt>よ</rt></ruby>み<ruby>方<rt>かた</rt></ruby>は？",
        promptPron: "요미카타와?",
        promptKo: "밑줄 친 한자의 읽는 법은?",
        targetWord: "走る",
        targetSub: "미오랑 매일 5km씩 트랙을 '달리다'!",
        options: ["あるく (아루쿠)", "はしる (하시루)", "およぐ (오요구)", "やすむ (야스무)"],
        answerIndex: 1,
        explanation: "走る(はしる / 하시루)는 '달리다', 歩く(あるく / 아루쿠)는 '걷다', 休む(やすむ / 야스무)는 '쉬다'예요!",
        geminiReactJp: "<ruby>大正解<rt>だいせいかい</rt></ruby>！<ruby>走<rt>はし</rt></ruby>るフォームも綺麗どすえ🏃‍♀️",
        geminiReactPron: "다이세-카이! 하시루 호-무모 키레이 도스에",
        geminiReactKo: "대정답! 달리는 폼도 아름다우셔요 🏃‍♀️"
      },
      {
        type: "오사카 유행어",
        promptJp: "「<ruby>知<rt>し</rt></ruby>らんけど」のニュアンスは？",
        promptPron: "시란케도노 뉴안스와?",
        promptKo: "간사이 사람들이 문장 끝에 붙이는 「知らんけど」의 뜻은?",
        targetWord: "知らんけど",
        targetSub: "자신 있게 말해놓고 책임을 슬쩍 회피할 때 쓰는 유쾌한 말버릇!",
        options: ["확실히 알고 있어!", "잘은 모르겠지만~ (아님 말고!)", "절대 잊지 마!", "미안하지만 부탁해!"],
        answerIndex: 1,
        explanation: "「知らんけど(시란케도)」는 오사카 사람들이 자기 생각을 말한 뒤 끝에 '뭐, 확실한 건 모르겠지만(아님 말고)~' 하고 붙이는 유머러스한 표현이에요!",
        geminiReactJp: "ふふ、これでプロデューサーはんも関西人どすね🍵",
        geminiReactPron: "후후, 코레데 푸로듀-사-항모 칸사이진 도스네",
        geminiReactKo: "후후, 이제 프로듀서항도 간사이 사람이시네요 🍵"
      },
      {
        type: "교토·간사이 연애 표현",
        promptJp: "「うちはプロデューサーはんが<ruby>好<rt>す</rt></ruby>きや」の「うち」は？",
        promptPron: "우치와 푸로듀-사-항가 스키야노 우치와?",
        promptKo: "간사이 여성이 쓰는 1인칭 대명사 「うち」의 뜻은?",
        targetWord: "うち",
        targetSub: "제가 저 자신을 가리킬 때 쓰는 말도스 🌸",
        options: ["너 (당신)", "나 / 저 (1인칭)", "우리 집 강아지", "선생님"],
        answerIndex: 1,
        explanation: "교토와 오사카에서 여성들이 자신을 부를 때 「わたし」 대신 다정하고 부드럽게 「うち(우치)」라고 부른답니다!",
        geminiReactJp: "そうどす、うちの心はプロデューサーはんのものどすえ💖",
        geminiReactPron: "소-도스, 우치노 코코로와 푸로듀-사-항노 모노 도스에",
        geminiReactKo: "맞아요, 제 마음은 프로듀서항의 것이랍니다 💖"
      },
      {
        type: "어휘 · 뜻",
        promptJp: "「<ruby>時計<rt>とけい</rt></ruby>」の<ruby>意味<rt>いみ</rt></ruby>は？",
        promptPron: "토케-노 이미와?",
        promptKo: "「時計(とけい)」의 뜻은 무엇인가요?",
        targetWord: "時計",
        targetSub: "17시 단식 마감 시간을 확인할 때 보는 물건!",
        options: ["체중계", "시계", "거울", "운동화"],
        answerIndex: 1,
        explanation: "時計(とけい / 토케-)는 '시계'예요. 참고로 체중계는 体重計(たいじゅうけい / 타이쥬-케-)라고 읽는답니다!",
        geminiReactJp: "ぴんぽーん！<ruby>五時<rt>ごじ</rt></ruby>になったら時計見よしね⏰",
        geminiReactPron: "핀퐁-! 고지니 낫타라 토케- 미요시네",
        geminiReactKo: "딩동댕! 5시가 되면 시계를 보셔요 ⏰"
      },
      {
        type: "교토벤 부정 표현",
        promptJp: "「<ruby>許<rt>ゆる</rt></ruby>しまへんえ」の「〜まへん」は標準語で？",
        promptPron: "유루시마헨에노 ~마헨와 효-준고데?",
        promptKo: "교토·간사이 사투리 「〜まへん (마헨)」은 표준어로 무엇일까요?",
        targetWord: "〜まへん",
        targetSub: "「食べまへん」「行きまへん」처럼 동사 뒤에 붙어요",
        options: ["〜ます (~합니다)", "〜ません (~하지 않습니다)", "〜ました (~했습니다)", "〜ましょう (~합시다)"],
        answerIndex: 1,
        explanation: "표준어의 「〜ません(~하지 않습니다)」이 교토·오사카에서는 부드럽게 「〜まへん(~마헨)」으로 바뀐답니다! (예: わかりまへん = 알지 못합니다)",
        geminiReactJp: "<ruby>全問<rt>ぜんもん</rt></ruby>正解どす！ご褒美に頭なでなでしてあげましょね🐾🌸",
        geminiReactPron: "젠몬 세-카이 도스! 고호-비니 아타마 나데나데 시테 아게마쇼네",
        geminiReactKo: "전 문항 정답이어요! 상으로 머리를 쓰담쓰담해 드릴게요 🐾🌸"
      }
    ]
  },

  // --------------------------------------------------------------------------
  // LESSON 4: 오사카 전철 여행 & 길 찾기 ("어디로 가야 해요?" & "금방이에요!")
  // --------------------------------------------------------------------------
  {
    id: "day4",
    dayNum: 4,
    dateLabel: "제4화 · 이야기",
    levelBadge: "N4 + 여행 회화",
    titleJp: "<ruby>駅<rt>えき</rt></ruby>までどないして<ruby>行<rt>い</rt></ruby>くん？",
    titlePron: "에키마데 도나이시테 이쿤?",
    titleKo: "역까지 어떻게 가는 건가요?",
    bgImage: "./image/03 gemini/gemini_27_kyoto_cherry_walk.png",
    grammarTip: {
      title: "🌸 제미니의 교토·오사카벤 노트 #4",
      content: "간사이에서 '어떻게(どうやって)'는 <b>「どないして (도나이시테)」</b>, '어떡하지?(どうしよう)'는 <b>「どないしよう (도나이시요-)」</b>라고 해요! 또 '~니까(だから/から)'는 문장 중간에 <b>「~さかい(사카이)」</b> 또는 <b>「~やから(야카라)」</b>를 붙인답니다 🚃"
    },
    story: [
      {
        speaker: "mio",
        nameJp: "ミオ",
        nameKo: "미오",
        avatar: "./image/01 mio/avatar_mio.png",
        sceneImg: "./image/01 mio/mio_16_conveni_bench.png",
        jpRuby: "あれれ？ <ruby>道<rt>みち</rt></ruby>に<ruby>迷<rt>まよ</rt></ruby>っちゃった！<ruby>駅<rt>えき</rt></ruby>はどこだろう？💦",
        jpPlain: "あれれ？ 道に迷っちゃった！駅はどこだろう？",
        pron: "아레레? 미치니 마욧챳타! 에키와 도코다로-?",
        ko: "어라라? 길을 잃어버렸어! 역은 어디지? 💦"
      },
      {
        speaker: "kotone",
        nameJp: "コトネ",
        nameKo: "코토네",
        avatar: "./image/02 kotone/avatar_kotone.png",
        sceneImg: "./image/02 kotone/kotone_14_morning_jog.png",
        jpRuby: "タクシーに<ruby>乗<rt>の</rt></ruby>ったらお金がもったいないですよ！<ruby>歩<rt>ある</rt></ruby>きましょう！💸",
        jpPlain: "タクシーに乗ったらお金がもったいないですよ！歩きましょう！",
        pron: "타쿠시-니 놋타라 오카네가 못타이나이데스요! 아루키마쇼-!",
        ko: "택시를 타면 돈이 아깝다구요! 걸어가요! 💸"
      },
      {
        speaker: "gemini",
        nameJp: "ジェミニ",
        nameKo: "제미니",
        avatar: "./image/03 gemini/avatar_gemini.png",
        sceneImg: "./image/03 gemini/gemini_27_kyoto_cherry_walk.png",
        jpRuby: "ふふ、慌てんといて。<ruby>京都駅<rt>きょうとえき</rt></ruby>なら、この<ruby>道<rt>みち</rt></ruby>をまっすぐ<ruby>行<rt>い</rt></ruby>くだけどすえ🌸",
        jpPlain: "ふふ、慌てんといて。京都駅なら、この道をまっすぐ行くだけどすえ。",
        pron: "후후, 아와텐토이테. 쿄-토에키나라, 코노 미치오 맛스구 이쿠 다케 도스에.",
        ko: "후후, 당황하지 마셔요. 교토역이라면 이 길을 쭉 직진하기만 하면 된답니다 🌸"
      },
      {
        speaker: "mio",
        nameJp: "ミオ",
        nameKo: "미오",
        avatar: "./image/01 mio/avatar_mio.png",
        sceneImg: "./image/01 mio/mio_20_sunset_highfive.png",
        jpRuby: "ほんまに？！ ジェミニちゃん、どないして<ruby>知<rt>し</rt></ruby>ってるの？🌟",
        jpPlain: "ほんまに？！ ジェミニちゃん、どないして知ってるの？",
        pron: "혼마니?! 제미니짱, 도나이시테 싯테루노?",
        ko: "정말로?! 제미니 짱, 어떻게 알고 있는 거야? 🌟"
      },
      {
        speaker: "gemini",
        nameJp: "ジェミニ",
        nameKo: "제미니",
        avatar: "./image/03 gemini/avatar_gemini.png",
        sceneImg: "./image/03 gemini/gemini_01_main.png",
        jpRuby: "うちは<ruby>京都<rt>きょうと</rt></ruby>のアイドルどすさかいね🍵 ほな、<ruby>早<rt>はや</rt></ruby>う<ruby>行<rt>い</rt></ruby>きましょか！",
        jpPlain: "うちは京都のアイドルどすさかいね。ほな、早う行きましょか！",
        pron: "우치와 쿄-토노 아이도루 도스 사카이네. 호나, 하요- 이키마쇼카!",
        ko: "저는 교토의 아이돌이니까요 🍵 자, 그럼 얼른 가볼까요!"
      }
    ],
    quizzes: [
      {
        type: "간사이 의문사",
        promptJp: "「どないして」は標準語でどういう<ruby>意味<rt>いみ</rt></ruby>？",
        promptPron: "도나이시테와 효-준고데 도-유- 이미?",
        promptKo: "간사이벤 「どないして」는 표준어로 무슨 뜻인가요?",
        targetWord: "どないして",
        targetSub: "「どないしよう(어떡하지)」와 세트로 자주 써요!",
        options: ["어떻게 (どうやって)", "언제부터 (いつから)", "누구와 (だれと)", "얼마나 (どのくらい)"],
        answerIndex: 0,
        explanation: "「どない(도나이)」는 '어떻게(どう)'라는 뜻이에요! 「どないして行くん？(어떻게 가는 거야?)」처럼 쓴답니다.",
        geminiReactJp: "<ruby>大正解<rt>だいせいかい</rt></ruby>どす！道案内もバッチリどすね🌸",
        geminiReactPron: "다이세-카이 도스! 미치안나이모 밧치리 도스네",
        geminiReactKo: "대정답이어요! 길 안내도 완벽하시네요 🌸"
      },
      {
        type: "한자 · 읽기",
        promptJp: "<ruby>読<rt>よ</rt></ruby>み<ruby>方<rt>かた</rt></ruby>は？",
        promptPron: "요미카타와?",
        promptKo: "밑줄 친 한자의 읽는 법은?",
        targetWord: "駅",
        targetSub: "전철이나 기차를 타는 '역'!",
        options: ["みち (미치)", "えき (에키)", "くるま (쿠루마)", "みせ (미세)"],
        answerIndex: 1,
        explanation: "駅(えき / 에키)는 '역', 道(みち / 미치)는 '길', 店(みせ / 미세)는 '가게'예요!",
        geminiReactJp: "ぴんぽーん！<ruby>駅<rt>えき</rt></ruby>まで歩いてカロリー消費どす🚶‍♀️",
        geminiReactPron: "핀퐁-! 에키마데 아루이테 카로리- 쇼-히 도스",
        geminiReactKo: "딩동댕! 역까지 걸어서 칼로리 소비예요 🚶‍♀️"
      },
      {
        type: "교토·간사이 접속사",
        promptJp: "「アイドルどすさかい」の「〜さかい」の<ruby>意味<rt>いみ</rt></ruby>は？",
        promptPron: "아이도루 도스 사카이노 ~사카이노 이미와?",
        promptKo: "교토·간사이 사투리 「〜さかい (사카이)」의 뜻은?",
        targetWord: "〜さかい",
        targetSub: "이유를 말할 때 표준어 「〜から / 〜だから」 대신 써요",
        options: ["~하니까 / ~이기 때문에", "~하지만 / ~인데도", "~하거나", "~할까 봐"],
        answerIndex: 0,
        explanation: "「〜さかい(사카이)」는 '~하니까/~이므로'라는 뜻의 전통 간사이 표현이에요! (예: 危ないさかい気ぃつけよし = 위험하니까 조심하셔요)",
        geminiReactJp: "よう<ruby>知<rt>し</rt></ruby>ってはるねぇ、感心しましたえ🍵",
        geminiReactPron: "요- 싯테 하루네-, 칸신 시마시타에",
        geminiReactKo: "잘 알고 계시네요, 감탄했사옵니다 🍵"
      },
      {
        type: "어휘 · 뜻",
        promptJp: "「もったいない」はどういう<ruby>意味<rt>いみ</rt></ruby>？",
        promptPron: "못타이나이와 도-유- 이미?",
        promptKo: "코토네의 입버릇 「もったいない」의 뜻은?",
        targetWord: "もったいない",
        targetSub: "돈이나 음식이 버려질 때 쓰는 표현!",
        options: ["아깝다 / 과분하다", "무겁다", "재미있다", "부럽다"],
        answerIndex: 0,
        explanation: "「もったいない(못타이나이)」는 시간이나 돈, 물건 등이 낭비될 때 '아깝다!'라고 하는 필수 형용사예요.",
        geminiReactJp: "<ruby>正解<rt>せいかい</rt></ruby>！タクシー代がもったいないどすね💸",
        geminiReactPron: "세-카이! 타쿠시-다이가 못타이나이 도스네",
        geminiReactKo: "정답! 택시비가 아깝지요 💸"
      },
      {
        type: "간사이 인사·전환어",
        promptJp: "「ほな、<ruby>行<rt>い</rt></ruby>きましょか」の「ほな」は？",
        promptPron: "호나, 이키마쇼카노 호나와?",
        promptKo: "대화를 전환하거나 헤어질 때 쓰는 「ほな」의 뜻은?",
        targetWord: "ほな",
        targetSub: "「ほなね〜(그럼 안녕~)」으로도 정말 많이 써요!",
        options: ["그런데도 (それでも)", "그럼 / 자 그러면 (それじゃあ)", "왜냐하면 (なぜなら)", "설마 (まさか)"],
        answerIndex: 1,
        explanation: "「ほな(호나)」는 표준어 「それじゃあ(그럼/그러면)」예요! 헤어질 때 「ほな、またね(그럼 또 봐)」라고 하면 자연스러운 간사이벤 완성!",
        geminiReactJp: "お<ruby>見事<rt>みごと</rt></ruby>どす！ほな、次のレッスンも楽しみにしといてね🌸🐾",
        geminiReactPron: "오미고토 도스! 호나, 츠기노 렛슨모 타노시미니 시토이테네",
        geminiReactKo: "훌륭해요! 그럼 다음 수업도 기대해 주셔요 🌸🐾"
      }
    ]
  },

  // --------------------------------------------------------------------------
  // LESSON 5: 비 오는 날 우산과 무리 금물 ("괜찮아?" & "감기 걸리면 안 돼요")
  // --------------------------------------------------------------------------
  {
    id: "day5",
    dayNum: 5,
    dateLabel: "제5화 · 이야기",
    levelBadge: "N3 + 심쿵 간사이벤",
    titleJp: "<ruby>一緒<rt>いっしょ</rt></ruby>に<ruby>傘<rt>かさ</rt></ruby>に<ruby>入<rt>はい</rt></ruby>りよし☔",
    titlePron: "잇쇼니 카사니 하이리요시",
    titleKo: "함께 우산 속으로 들어오시지요 ☔",
    bgImage: "./image/03 gemini/gemini_09_rain_locker.png",
    grammarTip: {
      title: "🌸 제미니의 교토·오사카벤 노트 #5",
      content: "간사이에서 '힘들다/피곤하다(つらい/疲れた)'는 <b>「しんどい (신도이)」</b>라고 해요! 또 '춥다(寒い)'나 '따뜻하다(温かい)'를 부드럽게 말할 때 <b>「寒うなる(사무-나루) / 温こうする(아타타코-스루)」</b>처럼 우음편(ウ音便)을 쓰면 진짜 교토 아가씨 느낌이 물씬 난답니다 🌸"
    },
    story: [
      {
        speaker: "mio",
        nameJp: "ミオ",
        nameKo: "미오",
        avatar: "./image/01 mio/avatar_mio.png",
        sceneImg: "./image/01 mio/mio_06_shared_umbrella.png",
        jpRuby: "わあっ、急に<ruby>雨<rt>あめ</rt></ruby>が<ruby>降<rt>ふ</rt></ruby>ってきたよ！プロデューサー、<ruby>傘<rt>かさ</rt></ruby>ある？☔",
        jpPlain: "わあっ、急に雨が降ってきたよ！プロデューサー、傘ある？",
        pron: "와앗, 큐-니 아메가 훗테 키타요! 푸로듀-사-, 카사 아루?",
        ko: "와앗, 갑자기 비가 내리기 시작했어! 프로듀서, 우산 있어? ☔"
      },
      {
        speaker: "kotone",
        nameJp: "コトネ",
        nameKo: "코토네",
        avatar: "./image/02 kotone/avatar_kotone.png",
        sceneImg: "./image/02 kotone/kotone_04_rain_locker.png",
        jpRuby: "コンビニでビニール<ruby>傘<rt>がさ</rt></ruby>を<ruby>買<rt>か</rt></ruby>うと700円もしますよ！<ruby>高<rt>たか</rt></ruby>すぎます〜😭",
        jpPlain: "コンビニでビニール傘を買うと700円もしますよ！高すぎます〜",
        pron: "콘비니데 비니-루가사오 카우토 나나햐쿠엔모 시마스요! 타카스기마스~",
        ko: "편의점에서 비닐우산 사면 700엔이나 한다구요! 너무 비싸요~ 😭"
      },
      {
        speaker: "gemini",
        nameJp: "ジェミニ",
        nameKo: "제미니",
        avatar: "./image/03 gemini/avatar_gemini.png",
        sceneImg: "./image/03 gemini/gemini_15_rain_stretch.png",
        jpRuby: "プロデューサーはん、<ruby>濡<rt>ぬ</rt></ruby>れたら<ruby>風邪<rt>かぜ</rt></ruby>ひきまっせ。ほら、うちの<ruby>傘<rt>かさ</rt></ruby>に<ruby>入<rt>はい</rt></ruby>りよし🌸",
        jpPlain: "プロデューサーはん、濡れたら風邪ひきまっせ。ほら、うちの傘に入りよし。",
        pron: "푸로듀-사-항, 누레타라 카제 히키맛세. 호라, 우치노 카사니 하이리요시.",
        ko: "프로듀서항, 젖으면 감기 걸릴 거예요. 자, 제 우산 속으로 들어오시지요 🌸"
      },
      {
        speaker: "gemini",
        nameJp: "ジェミニ",
        nameKo: "제미니",
        avatar: "./image/03 gemini/avatar_gemini.png",
        sceneImg: "./image/03 gemini/gemini_09_rain_locker.png",
        jpRuby: "<ruby>肩<rt>かた</rt></ruby>がぶつかってドキドキしはる？ ふふ、もっと<ruby>近<rt>ちか</rt></ruby>う寄ってもええんどすえ💖🐾",
        jpPlain: "肩がぶつかってドキドキしはる？ ふふ、もっと近う寄ってもええんどすえ。",
        pron: "카타가 부츠캇테 도키도키 시하루? 후후, 못토 치코- 욧테모 에-응 도스에.",
        ko: "어깨가 닿아서 두근거리시나요? 후후, 더 가까이 붙으셔도 괜찮답니다 💖🐾"
      },
      {
        speaker: "gemini",
        nameJp: "ジェミニ",
        nameKo: "제미니",
        avatar: "./image/03 gemini/avatar_gemini.png",
        sceneImg: "./image/03 gemini/gemini_02_matcha.png",
        jpRuby: "<ruby>家<rt>いえ</rt></ruby>に<ruby>帰<rt>かえ</rt></ruby>ったら、しんどくならんように<ruby>温<rt>あたた</rt></ruby>かいお<ruby>抹茶<rt>まっちゃ</rt></ruby>を淹れてあげましょね🍵",
        jpPlain: "家に帰ったら、しんどくならんように温かいお抹茶を淹れてあげましょね。",
        pron: "이에니 카엣타라, 신도쿠 나란 요-니 아타타카이 오맛챠오 이레테 아게마쇼네.",
        ko: "집에 돌아가면 몸살 나지(힘들지) 않도록 따뜻한 말차를 우려 드릴게요 🍵"
      }
    ],
    quizzes: [
      {
        type: "한자 · 읽기",
        promptJp: "<ruby>読<rt>よ</rt></ruby>み<ruby>方<rt>かた</rt></ruby>は？",
        promptPron: "요미카타와?",
        promptKo: "밑줄 친 한자의 읽는 법은?",
        targetWord: "傘",
        targetSub: "비 오는 날 제미니와 함께 쓴 '우산'!",
        options: ["あめ (아메)", "かさ (카사)", "かぜ (카제)", "くつ (쿠츠)"],
        answerIndex: 1,
        explanation: "傘(かさ / 카사)는 '우산', 雨(あめ / 아메)는 '비', 風邪(かぜ / 카제)는 '감기'예요!",
        geminiReactJp: "<ruby>正解<rt>せいかい</rt></ruby>どす！相合傘（あいあいがさ）、嬉しおすなぁ☔💖",
        geminiReactPron: "세-카이 도스! 아이아이가사, 우레시오스나-",
        geminiReactKo: "정답이어요! 우산 같이 쓰기, 참 기쁘네요 ☔💖"
      },
      {
        type: "간사이 필수 형용사",
        promptJp: "「しんどい」はどういう<ruby>意味<rt>いみ</rt></ruby>？",
        promptPron: "신도이와 도-유- 이미?",
        promptKo: "간사이 사람들이 입에 달고 사는 「しんどい」의 뜻은?",
        targetWord: "しんどい",
        targetSub: "운동이 힘들거나 몸이 피곤할 때 쓰는 1순위 표현!",
        options: ["몸이 힘들다 / 피곤하다", "배가 부르다", "기분이 상쾌하다", "날씨가 맑다"],
        answerIndex: 0,
        explanation: "「しんどい(신도이)」는 '피곤하다, 지친다, 힘들다(疲れた/つらい)'라는 뜻의 간사이벤 대표 어휘예요!",
        geminiReactJp: "しんどい時はいつでもうちに甘えよしね🐾🌸",
        geminiReactPron: "신도이 토키와 이츠데모 우치니 아마에요시네",
        geminiReactKo: "힘들 때는 언제든 저한테 기대시어요 🐾🌸"
      },
      {
        type: "교토벤 권유 표현",
        promptJp: "「<ruby>傘<rt>かさ</rt></ruby>に<ruby>入<rt>はい</rt></ruby>りよし」の「〜よし」のニュアンスは？",
        promptPron: "카사니 하이리요시노 ~요시노 뉴안스와?",
        promptKo: "교토 사투리 「入りよし (하이리요시)」는 어떤 뜻인가요?",
        targetWord: "〜よし",
        targetSub: "주의: 표준어의 「よせ(그만둬)」가 아니라 다정한 권유예요!",
        options: ["들어오지 마세요 (금지)", "들어오시지요 / 들어오렴 (다정한 권유)", "들어갔었나요? (과거 질문)", "들어갈 수 없습니다"],
        answerIndex: 1,
        explanation: "교토벤에서 동사 연용형 + 「よし」는 상대방에게 부드럽게 '~하셔요/~하렴(〜なさい)' 하고 권유하는 아주 다정한 표현이에요!",
        geminiReactJp: "ぴんぽーん！遠慮せんと、もっと近う寄りよし💖",
        geminiReactPron: "핀퐁-! 엔료센토, 못토 치코- 요리요시",
        geminiReactKo: "딩동댕! 사양 말고 더 가까이 다가오시지요 💖"
      },
      {
        type: "어휘 · 뜻",
        promptJp: "「<ruby>風邪<rt>かぜ</rt></ruby>をひく」の<ruby>意味<rt>いみ</rt></ruby>は？",
        promptPron: "카제오 히쿠노 이미와?",
        promptKo: "「風邪(かぜ)をひく」의 뜻은 무엇인가요?",
        targetWord: "風邪をひく",
        targetSub: "비에 젖으면 걸리기 쉬운 것!",
        options: ["감기에 걸리다", "바람이 불다", "체중을 재다", "우산을 펴다"],
        answerIndex: 0,
        explanation: "風邪(かぜ / 카제)는 '감기'이고, 감기에 걸리다는 항상 동사 「ひく(引く)」를 써서 「風邪をひく」라고 표현해요!",
        geminiReactJp: "<ruby>大正解<rt>だいせいかい</rt></ruby>！プロデューサーはんの健康はうちが守りますえ🍵",
        geminiReactPron: "다이세-카이! 푸로듀-사-항노 켄코-와 우치가 마모리마스에",
        geminiReactKo: "대정답! 프로듀서항의 건강은 제가 지킬 거예요 🍵"
      },
      {
        type: "교토·간사이 긍정 허락",
        promptJp: "「寄ってもええんどすえ」の「ええ」は標準語で？",
        promptPron: "욧테모 에-응 도스에노 에-와 효-준고데?",
        promptKo: "간사이벤 「ええ (에-)」는 표준어로 무슨 뜻일까요?",
        targetWord: "ええ",
        targetSub: "「ええよ(좋아/괜찮아)」「ええ天気(좋은 날씨)」처럼 써요!",
        options: ["いい / よい (좋다 / 괜찮다)", "わるい (나쁘다)", "おそい (느리다)", "とおい (멀다)"],
        answerIndex: 0,
        explanation: "표준어의 「いい(좋다/괜찮다)」는 간사이벤에서 「ええ(에-)」라고 발음해요! 「ええよ〜(좋아~/괜찮아~)」는 일상에서 100번 쓰이는 표현이랍니다.",
        geminiReactJp: "<ruby>全問<rt>ぜんもん</rt></ruby>クリア！プロデューサーはん、ほんまに最高どすえ🌸🐾",
        geminiReactPron: "젠몬 쿠리아! 푸로듀-사-항, 혼마니 사이코- 도스에",
        geminiReactKo: "전 문항 클리어! 프로듀서항, 정말 최고이십니다 🌸🐾"
      }
    ]
  }
];
