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
        audio: "./audio/kotonoha/day1_step1.mp3",
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
        audio: "./audio/kotonoha/day1_step2.mp3",
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
        audio: "./audio/kotonoha/day1_step3.mp3",
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
        audio: "./audio/kotonoha/day1_step5.mp3",
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
        audio: "./audio/kotonoha/day1_step7.mp3",
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
  },

  // --------------------------------------------------------------------------
  // LESSON 6: 카페 주문 & 교토 상점가 (N5 음식·주문 표현 & 마이도)
  // --------------------------------------------------------------------------
  {
    id: "day6",
    dayNum: 6,
    dateLabel: "제6화 · 이야기",
    levelBadge: "N5 · 카페 & 맛 표현",
    titleJp: "お<ruby>茶<rt>ちゃ</rt></ruby>を一<ruby>服<rt>ぷく</rt></ruby>、いかがどすか？",
    titlePron: "오챠오 잇푸쿠, 이카가 도스카?",
    titleKo: "차 한 잔, 어떠신가요?",
    bgImage: "./image/03 gemini/gemini_02_matcha.png",
    grammarTip: {
      title: "🌸 제미니의 교토·오사카벤 노트 #6",
      content: "식당이나 카페에서 주문할 때는 <b>「~を ください (~오 쿠다사이 / ~을 주세요)」</b> 하나면 충분해요! 또 일본 상점가나 노포에 들어가면 상인분들이 <b>『まいど (마이도)』</b>라고 정겹게 인사해 주시는데, '매번 찾아주셔서 감사합니다(まいどありがとうございます)'의 친근한 간사이식 줄임말이랍니다 🍵"
    },
    story: [
      {
        speaker: "gemini",
        nameJp: "ジェミニ",
        nameKo: "제미니",
        avatar: "./image/03 gemini/avatar_gemini.png",
        sceneImg: "./image/03 gemini/gemini_26_kyoto_teahouse.png",
        jpRuby: "プロデューサーはん、お<ruby>抹茶<rt>まっちゃ</rt></ruby>を一<ruby>服<rt>ぷく</rt></ruby>、いかがどすか？",
        jpPlain: "プロデューサーはん、お抹茶を一服、いかがどすか？",
        pron: "프로듀-사-항, 오맛챠오 잇푸쿠, 이카가 도스카?",
        ko: "프로듀서항, 말차 한 잔 어떠신가요?"
      },
      {
        speaker: "kotone",
        nameJp: "コトネ",
        nameKo: "코토네",
        avatar: "./image/02 kotone/avatar_kotone.png",
        sceneImg: "./image/02 kotone/kotone_03_cafe_date.png",
        jpRuby: "わぁ、いい<ruby>香<rt>かお</rt></ruby>り！あ、でもこの<ruby>和菓子<rt>わがし</rt></ruby>、すっごく<ruby>甘<rt>あま</rt></ruby>いですね！",
        jpPlain: "わぁ、いい香り！あ、でもこの和菓子、すっごく甘いですね！",
        pron: "와-, 이이 카오리! 아, 데모 코노 와가시, 숫고쿠 아마이데스네!",
        ko: "와아, 좋은 향기! 아, 하지만 이 화과자, 엄청 달콤하네요!"
      },
      {
        speaker: "gemini",
        nameJp: "ジェミニ",
        nameKo: "제미니",
        avatar: "./image/03 gemini/avatar_gemini.png",
        sceneImg: "./image/03 gemini/sd_gemini_02_matcha_whisk.png",
        jpRuby: "<ruby>苦<rt>にが</rt></ruby>いお<ruby>茶<rt>ちゃ</rt></ruby>と<ruby>甘<rt>あま</rt></ruby>いお<ruby>菓子<rt>かし</rt></ruby>は、<ruby>相性<rt>あいしょう</rt></ruby>がええんどすえ🌸",
        jpPlain: "苦いお茶と甘いお菓子は、相性がええんどすえ。",
        pron: "니가이 오챠토 아마이 오카시와, 아이쇼-가 에엔도스에.",
        ko: "쌉싸름한 차와 달콤한 과자는 궁합이 참 좋답니다."
      },
      {
        speaker: "mio",
        nameJp: "ミオ",
        nameKo: "미오",
        avatar: "./image/01 mio/avatar_mio.png",
        sceneImg: "./image/01 mio/mio_07_convenience_bar.png",
        jpRuby: "へへっ、<ruby>運動<rt>うんどう</rt></ruby>の<ruby>後<rt>あと</rt></ruby>は<ruby>水<rt>みず</rt></ruby>をいっぱい<ruby>飲<rt>の</rt></ruby>まなきゃ！すみません、お<ruby>水<rt>みず</rt></ruby>をください！",
        jpPlain: "へへっ、運動の後は水をいっぱい飲まなきゃ！すみません、お水をください！",
        pron: "헤헷, 운도-노 아토와 미즈오 잇파이 노마나캬! 스미마센, 오미즈오 쿠다사이!",
        ko: "헤헷, 운동 후에는 물을 듬뿍 마셔야지! 저기요, 물 좀 주세요!"
      },
      {
        speaker: "gemini",
        nameJp: "ジェミニ",
        nameKo: "제미니",
        avatar: "./image/03 gemini/avatar_gemini.png",
        sceneImg: "./image/03 gemini/gemini_02_matcha.png",
        jpRuby: "ふふ、プロデューサーはんも、しっかり<ruby>水分<rt>すいぶん</rt></ruby><ruby>補給<rt>ほきゅう</rt></ruby>しはっとくれやすね🍵🐾",
        jpPlain: "ふふ、プロデューサーはんも、しっかり水分補給しはっとくれやすね。",
        pron: "후후, 프로듀-사-항모, 싯카리 스이분 호큐- 시핫토쿠레야스네.",
        ko: "후후, 프로듀서항도 수분 보충 꼭 든든히 해주시어요 🍵🐾"
      }
    ],
    quizzes: [
      {
        type: "어휘 · 맛",
        promptJp: "「<ruby>甘<rt>あま</rt></ruby>い」の<ruby>意味<rt>いみ</rt></ruby>は？",
        promptPron: "아마이노 이미와?",
        promptKo: "「甘い」의 뜻은 무엇인가요?",
        targetWord: "甘い",
        targetSub: "화과자나 디저트의 맛이랍니다 🍡",
        options: ["달다", "쓰다", "맵다", "짜다"],
        answerIndex: 0,
        explanation: "甘い(あまい / 아마이)는 '달다'입니다. 반대로 쌉싸름한 맛은 苦い(にがい / 니가이)라고 해요!",
        geminiReactJp: "<ruby>正解<rt>せいかい</rt></ruby>どす！お<ruby>見事<rt>みごと</rt></ruby>どすえ🍵",
        geminiReactPron: "세이카이 도스! 오미고토 도스에~",
        geminiReactKo: "정답이어요! 훌륭하옵니다~"
      },
      {
        type: "기초 문법 · 주문",
        promptJp: "식당에서 '물 주세요'라고 주문할 때 알맞은 말은?",
        promptPron: "오미즈오 쿠다사이",
        promptKo: "식당 주문 필수 패턴!",
        targetWord: "お水をください",
        targetSub: "명사 + を ください 💧",
        options: ["お水を行きます", "お水をください", "お水を食べます", "お水を見ます"],
        answerIndex: 1,
        explanation: "『~を ください (~을 주세요)』는 일본 여행 식당 주문의 기본이자 핵심 표현입니다!",
        geminiReactJp: "ピンポン！その<ruby>調子<rt>ちょうし</rt></ruby>どす🌸",
        geminiReactPron: "핀퐁! 소노 쵸-시 도스~",
        geminiReactKo: "딩동! 바로 그 느낌이어요~"
      },
      {
        type: "간사이 방언 · 인사",
        promptJp: "오사카/교토 상점가에서 '매번 감사합니다'를 뜻하는 인사는?",
        promptPron: "마이도!",
        promptKo: "간사이 상인들의 정겨운 인사말!",
        targetWord: "まいど",
        targetSub: "가게에 들어가면 활기차게 들리는 말 🏮",
        options: ["まいど (마이도)", "さよなら (사요나라)", "おやすみ (오야스미)", "だめ (다메)"],
        answerIndex: 0,
        explanation: "まいど(마이도)는 '매번 찾아주셔서 감사합니다(まいどありがとうございます)'의 줄임말입니다!",
        geminiReactJp: "ほんまにえらいどすなぁ✨",
        geminiReactPron: "혼마니 에라이 도스나~",
        geminiReactKo: "정말로 장하십니다~"
      },
      {
        type: "한자 · 읽기",
        promptJp: "「<ruby>水<rt>?</rt></ruby>」の<ruby>読<rt>よ</rt></ruby>み<ruby>方<rt>かた</rt></ruby>は？",
        promptPron: "미즈노 요미카타와?",
        promptKo: "밑줄 친 한자의 알맞은 읽는 법은?",
        targetWord: "水",
        targetSub: "하루 2L 챙겨 마셔야 하는 물 💧",
        options: ["みず (미즈)", "おちゃ (오차)", "にく (니쿠)", "あめ (아메)"],
        answerIndex: 0,
        explanation: "水는 'みず (미즈)'라고 읽으며, 정중하게 お(오)를 붙여 'お水 (오미즈)'라고 부릅니다.",
        geminiReactJp: "<ruby>大正解<rt>だいせいかい</rt></ruby>どす！👏",
        geminiReactPron: "다이세이카이 도스!",
        geminiReactKo: "대정답이옵니다!"
      },
      {
        type: "어휘 · 반대말",
        promptJp: "「<ruby>苦<rt>にが</rt></ruby>い」의 뜻으로 올바른 것은?",
        promptPron: "니가이노 이미와?",
        promptKo: "진한 에스프레소나 진한 말차의 맛!",
        targetWord: "苦い",
        targetSub: "단맛(甘い)의 반대 표현 ☕",
        options: ["쓰다", "달다", "시다", "차갑다"],
        answerIndex: 0,
        explanation: "苦い(にがい / 니가이)는 '쓰다, 쌉싸름하다'라는 뜻입니다. 커피나 말차에 자주 써요!",
        geminiReactJp: "さすがプロデューサーはん！💯",
        geminiReactPron: "사스가 프로듀-사-항!",
        geminiReactKo: "역시 프로듀서님이셔요!"
      }
    ]
  },

  // --------------------------------------------------------------------------
  // LESSON 7: 날씨와 공원 조깅 (N5 날씨 표현 & 에에/아칸)
  // --------------------------------------------------------------------------
  {
    id: "day7",
    dayNum: 7,
    dateLabel: "제7화 · 이야기",
    levelBadge: "N5 · 날씨 & 기분",
    titleJp: "<ruby>今日<rt>きょう</rt></ruby>は<ruby>走<rt>はし</rt></ruby>るのにええ<ruby>天気<rt>てんき</rt></ruby>やなぁ！",
    titlePron: "쿄-와 하시루노니 에에 텐키야나-!",
    titleKo: "오늘은 달리기 참 좋은 날씨네!",
    bgImage: "./image/01 mio/mio_02_park_run.png",
    grammarTip: {
      title: "🌸 제미니의 교토·오사카벤 노트 #7",
      content: "간사이 사람들은 좋다(良い/いい) 대신 <b>『ええ (에에)』</b>를 정말 많이 써요! '좋은 날씨'는 <b>『ええ天気 (에에 텐키)』</b>, '좋은 느낌'은 <b>『ええ感じ (에에 칸지)』</b>! 반대로 안 된다, 나쁘다는 <b>『あかん (아칸)』</b>이라고 한답니다 🏃‍♀️"
    },
    story: [
      {
        speaker: "mio",
        nameJp: "ミオ",
        nameKo: "미오",
        avatar: "./image/01 mio/avatar_mio.png",
        sceneImg: "./image/01 mio/mio_02_park_run.png",
        jpRuby: "プロデューサー！<ruby>今日<rt>きょう</rt></ruby>は<ruby>晴<rt>は</rt></ruby>れてて、ええ<ruby>天気<rt>てんき</rt></ruby>だよ！",
        jpPlain: "プロデューサー！今日は晴れてて、ええ天気だよ！",
        pron: "프로듀-사-! 쿄-와 하레테테, 에에 텐키다요!",
        ko: "프로듀서! 오늘은 맑아서 달리기 딱 좋은 날씨야!"
      },
      {
        speaker: "gemini",
        nameJp: "ジェミニ",
        nameKo: "제미니",
        avatar: "./image/03 gemini/avatar_gemini.png",
        sceneImg: "./image/03 gemini/gemini_27_kyoto_cherry_walk.png",
        jpRuby: "ほんまどすなぁ。でも、<ruby>暑<rt>あつ</rt></ruby>いから<ruby>無理<rt>むり</rt></ruby>したらあきまへんえ。",
        jpPlain: "ほんまどすなぁ。でも、暑いから無理したらあきまへんえ。",
        pron: "혼마 도스나-. 데모, 아츠이카라 무리시타라 아키마헨에.",
        ko: "정말이네요. 하지만 더우니까 무리하시면 안 되어요."
      },
      {
        speaker: "kotone",
        nameJp: "コトネ",
        nameKo: "코토네",
        avatar: "./image/02 kotone/avatar_kotone.png",
        sceneImg: "./image/02 kotone/kotone_14_morning_jog.png",
        jpRuby: "ふぅ、ちょっと<ruby>走<rt>はし</rt></ruby>っただけで<ruby>汗<rt>あせ</rt></ruby>がすごいです〜！",
        jpPlain: "ふぅ、ちょっと走っただけで汗がすごいです〜！",
        pron: "후-, 촛토 하싯타 다케데 아세가 스고이데스~!",
        ko: "후우, 조금 달렸을 뿐인데 땀이 엄청나요~!"
      },
      {
        speaker: "gemini",
        nameJp: "ジェミニ",
        nameKo: "제미니",
        avatar: "./image/03 gemini/avatar_gemini.png",
        sceneImg: "./image/03 gemini/gemini_14_smoothie.png",
        jpRuby: "お<ruby>二人<rt>ふたり</rt></ruby>とも、えらいおきばりやす。タオルをどうぞ🌸",
        jpPlain: "お二人とも、えらいおきばりやす。タオルをどうぞ。",
        pron: "오후타리토모, 에라이 오키바리야스. 타오루오 도-조.",
        ko: "두 분 다 참 수고 많으셔요. 수건 받으시지요 🌸"
      }
    ],
    quizzes: [
      {
        type: "어휘 · 날씨",
        promptJp: "「<ruby>晴<rt>は</rt></ruby>れ」の<ruby>意味<rt>いみ</rt></ruby>は？",
        promptPron: "하레노 이미와?",
        promptKo: "「晴れ」의 뜻은 무엇인가요?",
        targetWord: "晴れ",
        targetSub: "구름 없이 화창한 날씨 ☀️",
        options: ["맑음", "비", "눈", "안개"],
        answerIndex: 0,
        explanation: "晴れ(はれ / 하레)는 '맑음'입니다. 비는 雨(あめ / 아메), 눈은 雪(ゆき / 유키)예요!",
        geminiReactJp: "<ruby>正解<rt>せいかい</rt></ruby>どす！よう<ruby>覚<rt>おぼ</rt></ruby>えてはりましたね🌸",
        geminiReactPron: "세이카이 도스! 요- 오보에테하리마시타네~",
        geminiReactKo: "정답이어요! 잘 기억하고 계셨군요~"
      },
      {
        type: "간사이 방언 · 형용사",
        promptJp: "간사이에서 '좋다(いい)'를 뜻하는 대표적인 단어는?",
        promptPron: "에에",
        promptKo: "좋은 날씨 = ええ天気!",
        targetWord: "ええ",
        targetSub: "표준어 いい(이이)의 방언 ✨",
        options: ["ええ (에에)", "あかん (아칸)", "あほ (아호)", "あかんべ (아칸베)"],
        answerIndex: 0,
        explanation: "간사이에서는 いい(이이) 대신 ええ(에에)를 일상적으로 씁니다. 반대말은 あかん(아칸)이에요!",
        geminiReactJp: "ピンポン！その<ruby>通<rt>とお</rt></ruby>りどす🍵",
        geminiReactPron: "핀퐁! 소노 토-리 도스~",
        geminiReactKo: "딩동! 바로 그대로이옵니다~"
      },
      {
        type: "어휘 · 온도",
        promptJp: "날씨가 '덥다'를 뜻하는 일본어는?",
        promptPron: "아츠이",
        promptKo: "여름 러닝 때 자주 나오는 말 ☀️",
        targetWord: "暑い",
        targetSub: "추운 건 寒い(さむい)!",
        options: ["暑い (아츠이)", "寒い (사무이)", "遠い (토오이)", "近い (치카이)"],
        answerIndex: 0,
        explanation: "暑い(あつい / 아츠이)는 날씨가 '덥다'입니다. 반대로 춥다는 寒い(さむい / 사무이)예요.",
        geminiReactJp: "バッチリどす！えらいなぁ👏",
        geminiReactPron: "밧치리 도스! 에라이나~",
        geminiReactKo: "완벽해요! 장하셔라~"
      },
      {
        type: "한자 · 읽기",
        promptJp: "「<ruby>走<rt>?</rt></ruby>る」의 올바른 읽는 법은?",
        promptPron: "하시루",
        promptKo: "공원을 신나게 달리는 미오!",
        targetWord: "走る",
        targetSub: "동사: 달리다 🏃‍♀️",
        options: ["はしる (하시루)", "あるく (아루쿠)", "とぶ (토부)", "およぐ (오요구)"],
        answerIndex: 0,
        explanation: "走る(はしる / 하시루)는 '달리다'입니다. 걷다는 歩く(あるく / 아루쿠)예요!",
        geminiReactJp: "<ruby>正解<rt>せいかい</rt></ruby>！ミオはんも<ruby>喜<rt>よろこ</rt></ruby>びますえ🏃‍♀️",
        geminiReactPron: "세이카이! 미오항모 요로코비마스에",
        geminiReactKo: "정답! 미오도 기뻐하겠네요~"
      },
      {
        type: "간사이 방언 · 부정",
        promptJp: "'안 돼!', '소용없어!'를 뜻하는 오사카의 대표 유행어는?",
        promptPron: "아칸!",
        promptKo: "야식 먹으려 할 때 제미니의 츳코미!",
        targetWord: "あかん",
        targetSub: "だめ(다메)의 간사이 사투리 💢",
        options: ["あかん (아칸)", "おおきに (오오키니)", "まいど (마이도)", "おいで (오이데)"],
        answerIndex: 0,
        explanation: "あかん(아칸)은 '안 된다, 곤란하다'라는 뜻의 대표 간사이 방언입니다. 야식 금지 때 딱이죠!",
        geminiReactJp: "ふふ、夜食はあきまへんえ！🐾",
        geminiReactPron: "후후, 야쇼쿠와 아키마헨에!",
        geminiReactKo: "후후, 야식은 안 되옵니다!"
      }
    ]
  },

  // --------------------------------------------------------------------------
  // LESSON 8: 헬스장 근육통 & 신체 부위 (N5 신체 명사 & 난데야넨)
  // --------------------------------------------------------------------------
  {
    id: "day8",
    dayNum: 8,
    dateLabel: "제8화 · 이야기",
    levelBadge: "N5 · 신체 & 건강",
    titleJp: "<ruby>背中<rt>せなか</rt></ruby>と<ruby>肩<rt>かた</rt></ruby>、<ruby>筋肉痛<rt>きんにくつう</rt></ruby>は<ruby>大丈夫<rt>だいじょうぶ</rt></ruby>どすか？",
    titlePron: "세나카토 카타, 킨니쿠츠-와 다이죠-부 도스카?",
    titleKo: "등과 어깨, 근육통은 괜찮으신가요?",
    bgImage: "./image/03 gemini/gemini_03_rehab_touch.png",
    grammarTip: {
      title: "🌸 제미니의 교토·오사카벤 노트 #8",
      content: "몸이 아플 때는 <b>「~が 痛い (~가 이타이 / ~가 아프다)」</b>라고 말해요. 머리가 아프면 '頭が痛い(아타마가 이타이)', 배가 아프면 'お腹が痛い(오나카가 이타이)'! 그리고 상대방이 엉뚱한 변명을 할 때는 <b>『なんでやねん (난데야넨 / 무슨 소리야!)』</b>으로 유쾌하게 받아쳐 보세요 🐾"
    },
    story: [
      {
        speaker: "gemini",
        nameJp: "ジェミニ",
        nameKo: "제미니",
        avatar: "./image/03 gemini/avatar_gemini.png",
        sceneImg: "./image/03 gemini/gemini_03_rehab_touch.png",
        jpRuby: "プロデューサーはん、<ruby>肩<rt>かた</rt></ruby>や<ruby>背中<rt>せなか</rt></ruby>は<ruby>痛<rt>いた</rt></ruby>くありまへんか？",
        jpPlain: "プロデューサーはん、肩や背中は痛くありまへんか？",
        pron: "프로듀-사-항, 카타야 세나카와 이타쿠 아리마헨카?",
        ko: "프로듀서항, 어깨나 등은 아프지 않으신가요?"
      },
      {
        speaker: "kotone",
        nameJp: "コトネ",
        nameKo: "코토네",
        avatar: "./image/02 kotone/avatar_kotone.png",
        sceneImg: "./image/02 kotone/kotone_25_night_convenience_chat.png",
        jpRuby: "うぅ…<ruby>私<rt>わたし</rt></ruby>は<ruby>足<rt>あし</rt></ruby>がパンパンで<ruby>痛<rt>いた</rt></ruby>いです〜！",
        jpPlain: "うぅ…私は足がパンパンで痛いです〜！",
        pron: "우-… 와타시와 아시가 판판데 이타이데스~!",
        ko: "으으… 저는 다리가 퉁퉁 부어서 아파요~!"
      },
      {
        speaker: "mio",
        nameJp: "ミオ",
        nameKo: "미오",
        avatar: "./image/01 mio/avatar_mio.png",
        sceneImg: "./image/01 mio/mio_13_bench_workout.png",
        jpRuby: "あっはは！それは<ruby>筋肉<rt>きんにく</rt></ruby>が<ruby>育<rt>そだ</rt></ruby>ってる<ruby>証拠<rt>しょうこ</rt></ruby>だよ！",
        jpPlain: "あっはは！それは筋肉が育ってる証拠だよ！",
        pron: "앗하하! 소레와 킨니쿠가 소닷테루 쇼-코다요!",
        ko: "앗하하! 그건 근육이 자라나고 있다는 증거야!"
      },
      {
        speaker: "gemini",
        nameJp: "ジェミニ",
        nameKo: "제미니",
        avatar: "./image/03 gemini/avatar_gemini.png",
        sceneImg: "./image/03 gemini/gemini_15_rain_stretch.png",
        jpRuby: "ほな、ゆっくりストレッチしまひょ。うちがお<ruby>手伝<rt>てつだ</rt></ruby>いしますえ🌸",
        jpPlain: "ほな、ゆっくりストレッチしまひょ。うちがお手伝いしますえ。",
        pron: "호나, 육쿠리 스트렛치 시마효. 우치가 오테츠다이 시마스에.",
        ko: "그럼 천천히 스트레칭하지요. 제가 도와드릴게요 🌸"
      }
    ],
    quizzes: [
      {
        type: "어휘 · 신체",
        promptJp: "「<ruby>肩<rt>かた</rt></ruby>」の<ruby>意味<rt>いみ</rt></ruby>は？",
        promptPron: "카타노 이미와?",
        promptKo: "「肩」의 뜻은 무엇인가요?",
        targetWord: "肩",
        targetSub: "덤벨 숄더 프레스 할 때 쓰는 부위 🏋️",
        options: ["어깨", "허리", "무릎", "손목"],
        answerIndex: 0,
        explanation: "肩(かた / 카타)는 '어깨'입니다. 등은 背中(せなか / 세나카), 배는 お腹(おなか / 오나카)예요!",
        geminiReactJp: "<ruby>正解<rt>せいかい</rt></ruby>どす！よくご<ruby>存<rt>ぞん</rt></ruby>じどすね👏",
        geminiReactPron: "세이카이 도스! 요쿠 고존지 도스네~",
        geminiReactKo: "정답이어요! 잘 알고 계시네요~"
      },
      {
        type: "어휘 · 상태",
        promptJp: "몸이 '아프다'를 나타내는 일본어 형용사는?",
        promptPron: "이타이",
        promptKo: "근육통으로 뻐근하고 쑤실 때!",
        targetWord: "痛い",
        targetSub: "반대말: 괜찮다(大丈夫)",
        options: ["痛い (이타이)", "甘い (아마이)", "重い (오모이)", "速い (하야이)"],
        answerIndex: 0,
        explanation: "痛い(いたい / 이타이)는 '아프다'입니다. '足が痛い(다리가 아프다)'처럼 쓰여요.",
        geminiReactJp: "ピンポン！お<ruby>見事<rt>みごと</rt></ruby>どすえ🌸",
        geminiReactPron: "핀퐁! 오미고토 도스에~",
        geminiReactKo: "딩동! 훌륭하옵니다~"
      },
      {
        type: "어휘 · 신체",
        promptJp: "「<ruby>足<rt>あし</rt></ruby>」의 뜻으로 알맞은 것은?",
        promptPron: "아시",
        promptKo: "러닝할 때 가장 열일하는 곳 👟",
        targetWord: "足",
        targetSub: "손은 手(て / 테)",
        options: ["발 / 다리", "눈", "귀", "입"],
        answerIndex: 0,
        explanation: "足(あし / 아시)는 '발 또는 다리'를 뜻합니다. 손은 手(て / 테), 머리는 頭(あたま / 아타마)예요!",
        geminiReactJp: "<ruby>大正解<rt>だいせいかい</rt></ruby>どす！さすがやわぁ✨",
        geminiReactPron: "다이세이카이 도스! 사스가야와~",
        geminiReactKo: "대정답이어요! 역시 최고예요~"
      },
      {
        type: "간사이 츳코미",
        promptJp: "'무슨 소리야?! / 왜 이래?!'를 뜻하는 만능 오사카 츳코미는?",
        promptPron: "난데야넨!",
        promptKo: "개그 콤비의 찰진 반격 한마디 💥",
        targetWord: "なんでやねん",
        targetSub: "간사이 개그의 심장!",
        options: ["なんでやねん (난데야넨)", "おおきに (오오키니)", "かまへん (카마헨)", "ほんま (혼마)"],
        answerIndex: 0,
        explanation: "なんでやねん(난데야넨)은 일본 코미디와 일상에서 가장 유명한 오사카 츳코미 표현입니다!",
        geminiReactJp: "ふふ、なんでやねん！🐾",
        geminiReactPron: "후후, 난데야넨!",
        geminiReactKo: "후후, 무슨 소리예요!"
      },
      {
        type: "어휘 · 확인",
        promptJp: "'괜찮습니다'를 뜻하는 일본어는?",
        promptPron: "다이죠-부데스",
        promptKo: "트레이너가 컨디션 물어볼 때 답하는 말!",
        targetWord: "大丈夫",
        targetSub: "상대방을 안심시키는 말 👍",
        options: ["大丈夫 (다이죠-부)", "だめ (다메)", "むり (무리)", "わるい (와루이)"],
        answerIndex: 0,
        explanation: "大丈夫(だいじょうぶ / 다이죠-부)는 '괜찮음'입니다. '大丈夫ですか？(괜찮으신가요?)'로 물어봐요.",
        geminiReactJp: "満点どす！完璧やわぁ💯",
        geminiReactPron: "만텐 도스! 칸페키야와~",
        geminiReactKo: "만점이옵니다! 완벽해요~"
      }
    ]
  },

  // --------------------------------------------------------------------------
  // LESSON 9: 시간과 약속 (N5 시간 숫자 & 하요)
  // --------------------------------------------------------------------------
  {
    id: "day9",
    dayNum: 9,
    dateLabel: "제9화 · 이야기",
    levelBadge: "N5 · 시간 & 일정",
    titleJp: "<ruby>今<rt>いま</rt></ruby><ruby>何時<rt>なんじ</rt></ruby>？ジムは<ruby>何時<rt>なんじ</rt></ruby>からどすか？",
    titlePron: "이마 난지? 지무와 난지카라 도스카?",
    titleKo: "지금 몇 시? 헬스장은 몇 시부터인가요?",
    bgImage: "./image/00 common/trio_03_inbody_gym.png",
    grammarTip: {
      title: "🌸 제미니의 교토·오사카벤 노트 #9",
      content: "시간을 나타낼 때는 <b>「~時から ~時まで (~지카라 ~지마데 / ~시부터 ~시까지)」</b>를 씁니다. '1시부터 3시까지'는 '一時から三時まで'! 그리고 오사카 사람들은 빨리(早く/하야쿠) 대신 <b>『はよ (하요)』</b>를 정말 자주 써요! 'はよ行こ(하요 이코 / 얼른 가자)'처럼 쓴답니다 ⏰"
    },
    story: [
      {
        speaker: "kotone",
        nameJp: "コトネ",
        nameKo: "코토네",
        avatar: "./image/02 kotone/avatar_kotone.png",
        sceneImg: "./image/02 kotone/kotone_04_rain_locker.png",
        jpRuby: "プロデューサーさん、<ruby>今<rt>いま</rt></ruby><ruby>何時<rt>なんじ</rt></ruby>ですか？！",
        jpPlain: "プロデューサーさん、今何時ですか？！",
        pron: "프로듀-사-상, 이마 난지데스카?!",
        ko: "프로듀서님, 지금 몇 시인가요?!"
      },
      {
        speaker: "mio",
        nameJp: "ミオ",
        nameKo: "미오",
        avatar: "./image/01 mio/avatar_mio.png",
        sceneImg: "./image/01 mio/mio_16_conveni_bench.png",
        jpRuby: "<ruby>今<rt>いま</rt></ruby>はちょうど<ruby>夕方<rt>ゆうがた</rt></ruby>5<ruby>時<rt>じ</rt></ruby>！ジムが<ruby>始<rt>はじ</rt></ruby>まる<ruby>時間<rt>じかん</rt></ruby>だよ！",
        jpPlain: "今はちょうど夕方5時！ジムが始まる時間だよ！",
        pron: "이마와 쵸-도 유-가타 고지! 지무가 하지마루 지칸다요!",
        ko: "지금은 딱 저녁 5시! 헬스장 시작할 시간이야!"
      },
      {
        speaker: "gemini",
        nameJp: "ジェミニ",
        nameKo: "제미니",
        avatar: "./image/03 gemini/avatar_gemini.png",
        sceneImg: "./image/03 gemini/gemini_01_main.png",
        jpRuby: "はよ<ruby>行<rt>い</rt></ruby>きまひょ！<ruby>今日<rt>きょう</rt></ruby>はダンベル4セットどすえ🐾",
        jpPlain: "はよ行きまひょ！今日はダンベル4セットどすえ。",
        pron: "하요 이키마효! 쿄-와 단베루 욘셋토 도스에.",
        ko: "얼른 가보지요! 오늘은 덤벨 4세트랍니다 🐾"
      }
    ],
    quizzes: [
      {
        type: "어휘 · 시간",
        promptJp: "「<ruby>今<rt>いま</rt></ruby>」의 뜻으로 알맞은 것은?",
        promptPron: "이마",
        promptKo: "현재 이 순간을 뜻하는 기초 단어!",
        targetWord: "今",
        targetSub: "今何時ですか？(지금 몇 시인가요?)",
        options: ["지금 / 현재", "어제", "내일", "작년"],
        answerIndex: 0,
        explanation: "今(いま / 이마)는 '지금'입니다. 今日(きょう / 쿄-)는 '오늘', 明日(あした / 아시타)는 '내일'이에요!",
        geminiReactJp: "<ruby>正解<rt>せいかい</rt></ruby>どす！バッチリやわぁ🌸",
        geminiReactPron: "세이카이 도스! 밧치리야와~",
        geminiReactKo: "정답이어요! 완벽해요~"
      },
      {
        type: "조사 · 범위",
        promptJp: "'~부터 ~까지'를 뜻하는 일본어 조사 세트는?",
        promptPron: "~카라 ~마데",
        promptKo: "9시부터 6시까지 일해요!",
        targetWord: "から / まで",
        targetSub: "시간과 장소의 출발점과 도착점 ⏰",
        options: ["から / まで (카라 / 마데)", "より / ほど (요리 / 호도)", "で / に (데 / 니)", "と / や (토 / 야)"],
        answerIndex: 0,
        explanation: "『~から (~부터)』와 『~まで (~까지)』는 시간과 공간 범위를 나타내는 필수 조사입니다.",
        geminiReactJp: "ピンポン！お<ruby>見事<rt>みごと</rt></ruby>どす👏",
        geminiReactPron: "핀퐁! 오미고토 도스~",
        geminiReactKo: "딩동! 훌륭하옵니다~"
      },
      {
        type: "간사이 방언 · 부사",
        promptJp: "'빨리, 얼른(早く)'을 뜻하는 간사이 사투리는?",
        promptPron: "하요",
        promptKo: "はよ行こ！(얼른 가자!)",
        targetWord: "はよ",
        targetSub: "早く(하야쿠)의 간사이 줄임말 🏃",
        options: ["はよ (하요)", "ゆっくり (육쿠리)", "そろそろ (소로소로)", "ずっと (즛토)"],
        answerIndex: 0,
        explanation: "はよ(하요)는 早く(하야쿠)의 간사이 방언입니다. 'はよ起き(얼른 일어나)'처럼 가족끼리도 많이 써요!",
        geminiReactJp: "<ruby>大正解<rt>だいせいかい</rt></ruby>！はよ<ruby>次<rt>つぎ</rt></ruby>へ進みましょ🌸",
        geminiReactPron: "다이세이카이! 하요 츠기에 스스미마쇼~",
        geminiReactKo: "대정답! 얼른 다음으로 넘어가 보지요~"
      },
      {
        type: "숫자 · 시간",
        promptJp: "오후 '5시'를 일본어로 읽는 법은?",
        promptPron: "고지",
        promptKo: "저녁 단식이 시작되는 골든 타임 🕔",
        targetWord: "五時",
        targetSub: "숫자 5(ご) + 時(じ)",
        options: ["ごじ (고지)", "よじ (요지)", "ろくじ (로쿠지)", "しちじ (시치지)"],
        answerIndex: 0,
        explanation: "5시는 五時(ごじ / 고지)입니다. 참고로 4시는 'よじ (요지)', 9시는 'くじ (쿠지)'로 특이하게 읽혀요!",
        geminiReactJp: "さすがプロデューサーはん！💯",
        geminiReactPron: "사스가 프로듀-사-항!",
        geminiReactKo: "역시 프로듀서님이셔요!"
      }
    ]
  },

  // --------------------------------------------------------------------------
  // LESSON 10: 인바디 측정과 감정 표현 (N5 감정 형용사 & 신도이)
  // --------------------------------------------------------------------------
  {
    id: "day10",
    dayNum: 10,
    dateLabel: "제10화 · 이야기",
    levelBadge: "N5 · 감정 & 힐링",
    titleJp: "<ruby>体重計<rt>たいじゅうけい</rt></ruby>に<ruby>乗<rt>の</rt></ruby>るのが<ruby>怖<rt>こわ</rt></ruby>いんどすか？",
    titlePron: "타이쥬-케이니 노루노가 코와인 도스카?",
    titleKo: "체중계 올라가는 게 무서우신가요?",
    bgImage: "./image/03 gemini/gemini_08_inbody_sheet.png",
    grammarTip: {
      title: "🌸 제미니의 교토·오사카벤 노트 #10",
      content: "힘들거나 피곤할 때 쓰는 <b>『しんどい (신도이)』</b>는 원래 오사카·간사이 방언이었지만, 너무 찰지고 편리해서 지금은 일본 전국의 표준어처럼 널리 쓰이게 된 전설의 단어예요! 운동 후 지쳤을 때 'あ〜しんど(아~ 신도 / 아 피곤해)'라고 해보세요 🐾"
    },
    story: [
      {
        speaker: "gemini",
        nameJp: "ジェミニ",
        nameKo: "제미니",
        avatar: "./image/03 gemini/avatar_gemini.png",
        sceneImg: "./image/03 gemini/gemini_08_inbody_sheet.png",
        jpRuby: "プロデューサーはん、<ruby>体重計<rt>たいじゅうけい</rt></ruby>に<ruby>乗<rt>の</rt></ruby>るのが<ruby>怖<rt>こわ</rt></ruby>いんどすか？",
        jpPlain: "プロデューサーはん、体重計に乗るのが怖いんどすか？",
        pron: "프로듀-사-항, 타이쥬-케이니 노루노가 코와인 도스카?",
        ko: "프로듀서항, 체중계 위에 올라가는 게 무서우신가요?"
      },
      {
        speaker: "kotone",
        nameJp: "コトネ",
        nameKo: "코토네",
        avatar: "./image/02 kotone/avatar_kotone.png",
        sceneImg: "./image/02 kotone/sd_kotone_01_coin_tears.png",
        jpRuby: "ひゃあ！<ruby>昨日<rt>きのう</rt></ruby>アイスを<ruby>食<rt>た</rt></ruby>べちゃったから<ruby>怖<rt>こわ</rt></ruby>いです〜！",
        jpPlain: "ひゃあ！昨日アイスを食べちゃったから怖いです〜！",
        pron: "햐아! 키노- 아이스오 타베찻타카라 코와이데스~!",
        ko: "히익! 어제 아이스크림을 먹어버려서 무서워요~!"
      },
      {
        speaker: "mio",
        nameJp: "ミオ",
        nameKo: "미오",
        avatar: "./image/01 mio/avatar_mio.png",
        sceneImg: "./image/01 mio/sd_mio_02_legraise_melt.png",
        jpRuby: "あはは！<ruby>大丈夫<rt>だいじょうぶ</rt></ruby>！<ruby>今日<rt>きょう</rt></ruby>走れば<ruby>全部<rt>ぜんぶ</rt></ruby><ruby>消費<rt>しょうひ</rt></ruby>できるよ！",
        jpPlain: "あはは！大丈夫！今日走れば全部消費できるよ！",
        pron: "아하하! 다이죠-부! 쿄- 하시레바 젠부 쇼-히 데키루요!",
        ko: "아하하! 괜찮아! 오늘 달리면 전부 소비할 수 있어!"
      },
      {
        speaker: "gemini",
        nameJp: "ジェミニ",
        nameKo: "제미니",
        avatar: "./image/03 gemini/avatar_gemini.png",
        sceneImg: "./image/03 gemini/gemini_05_night_secret.png",
        jpRuby: "ふふ、<ruby>現実<rt>げんじつ</rt></ruby>から<ruby>逃<rt>に</rt></ruby>げたらあきまへんえ。さあ、どうぞ🌸",
        jpPlain: "ふふ、現実から逃げたらあきまへんえ。さあ、どうぞ。",
        pron: "후후, 겐지츠카라 니게타라 아키마헨에. 사-, 도-조.",
        ko: "후후, 현실에서 도망치시면 안 되어요. 자, 올라가 보시지요 🌸"
      }
    ],
    quizzes: [
      {
        type: "어휘 · 감정",
        promptJp: "「<ruby>怖<rt>こわ</rt></ruby>い」의 뜻으로 알맞은 것은?",
        promptPron: "코와이",
        promptKo: "체중계 앞에 설 때 드는 그 감정!",
        targetWord: "怖い",
        targetSub: "기쁜 건 嬉しい(우레시이)",
        options: ["무섭다 / 두렵다", "기쁘다", "즐겁다", "슬프다"],
        answerIndex: 0,
        explanation: "怖い(こわい / 코와이)는 '무섭다, 두렵다'입니다. 반대로 기쁘다는 嬉しい(うれしい / 우레시이)예요!",
        geminiReactJp: "<ruby>正解<rt>せいかい</rt></ruby>どす！怖がらんでもええんどすえ🌸",
        geminiReactPron: "세이카이 도스! 코와가란데모 에엔도스에~",
        geminiReactKo: "정답이어요! 무서워하지 않으셔도 되어요~"
      },
      {
        type: "전국구 간사이 방언",
        promptJp: "간사이에서 전국으로 퍼진 '힘들다, 지치다'를 뜻하는 단어는?",
        promptPron: "신도이",
        promptKo: "하체 운동 끝나고 나오는 그 한마디 💦",
        targetWord: "しんどい",
        targetSub: "피곤하고 지칠 때 만능 표현!",
        options: ["しんどい (신도이)", "たのしい (타노시이)", "おいしい (오이시이)", "かわいい (카와이이)"],
        answerIndex: 0,
        explanation: "しんどい(신도이)는 간사이 출신의 대표적인 형용사로, '지치고 힘들다'를 나타낼 때 일본 전역에서 쓰입니다.",
        geminiReactJp: "ピンポン！その<ruby>通<rt>とお</rt></ruby>りどす🍵",
        geminiReactPron: "핀퐁! 소노 토-리 도스~",
        geminiReactKo: "딩동! 바로 그대로이옵니다~"
      },
      {
        type: "어휘 · 감정",
        promptJp: "'기쁘다'를 뜻하는 일본어는?",
        promptPron: "우레시이",
        promptKo: "체중 감량에 성공했을 때!",
        targetWord: "嬉しい",
        targetSub: "기쁨의 미소 ✨",
        options: ["嬉しい (우레시이)", "悲しい (카나시이)", "痛い (이타이)", "寒い (사무이)"],
        answerIndex: 0,
        explanation: "嬉しい(うれしい / 우레시이)는 '기쁘다'입니다. 슬프다는 悲しい(かなしい / 카나시이)예요.",
        geminiReactJp: "ほんまにえらいどすなぁ👏",
        geminiReactPron: "혼마니 에라이 도스나~",
        geminiReactKo: "정말로 장하십니다~"
      },
      {
        type: "어휘 · 감정",
        promptJp: "운동이나 대화가 '즐겁다, 신나다'를 뜻하는 말은?",
        promptPron: "타노시이",
        promptKo: "세 히로인과의 다실 시간!",
        targetWord: "楽しい",
        targetSub: "인생을 재미있게 즐길 때 🎶",
        options: ["楽しい (타노시이)", "苦い (니가이)", "甘い (아마이)", "重い (오모이)"],
        answerIndex: 0,
        explanation: "楽しい(たのしい / 타노시이)는 '즐겁다'입니다. '다실 공부가 즐겁다(お茶屋の勉強が楽しい)'처럼 쓰여요!",
        geminiReactJp: "満点どす！うちも<ruby>楽<rt>たの</rt></ruby>しいどすえ🌸",
        geminiReactPron: "만텐 도스! 우치모 타노시이 도스에~",
        geminiReactKo: "만점이옵니다! 저도 참 즐겁네요~"
      }
    ]
  },

  // --------------------------------------------------------------------------
  // LESSON 11: 전철과 교통 (N5 교통수단 & ~마효)
  // --------------------------------------------------------------------------
  {
    id: "day11",
    dayNum: 11,
    dateLabel: "제11화 · 이야기",
    levelBadge: "N5 · 일본 교통 & 여행",
    titleJp: "<ruby>切符<rt>きっぷ</rt></ruby>を<ruby>買<rt>か</rt></ruby>うて、<ruby>電車<rt>でんしゃ</rt></ruby>に<ruby>乗<rt>の</rt></ruby>りまひょ",
    titlePron: "킵푸오 코-테, 덴샤니 노리마효",
    titleKo: "표를 사서 전철을 타보지요",
    bgImage: "./image/03 gemini/gemini_18_street.png",
    grammarTip: {
      title: "🌸 제미니의 교토·오사카벤 노트 #11",
      content: "장소를 물어볼 때는 <b>「~は どこですか (~와 도코데스카 / ~는 어디인가요?)」</b>라고 질문해요. 역은 '駅(えき / 에키)', 화장실은 'トイレ(토이레)'! 그리고 '~합시다(〜ましょう)'를 교토에서는 곱게 <b>『〜まひょ (~마효)』</b>라고 발음한답니다 🚃"
    },
    story: [
      {
        speaker: "gemini",
        nameJp: "ジェミニ",
        nameKo: "제미니",
        avatar: "./image/03 gemini/avatar_gemini.png",
        sceneImg: "./image/03 gemini/gemini_18_street.png",
        jpRuby: "プロデューサーはん、<ruby>駅<rt>えき</rt></ruby>はあっちどすえ。<ruby>一緒<rt>いっしょ</rt></ruby>に<ruby>切符<rt>きっぷ</rt></ruby>を<ruby>買<rt>か</rt></ruby>いまひょ。",
        jpPlain: "プロデューサーはん、駅はあっちどすえ。一緒に切符を買いまひょ。",
        pron: "프로듀-사-항, 에키와 앗치 도스에. 잇쇼니 킵푸오 카이마효.",
        ko: "프로듀서항, 역은 저쪽이랍니다. 함께 표를 사지요."
      },
      {
        speaker: "mio",
        nameJp: "ミオ",
        nameKo: "미오",
        avatar: "./image/01 mio/avatar_mio.png",
        sceneImg: "./image/01 mio/mio_20_sunset_highfive.png",
        jpRuby: "おーっ！<ruby>電車<rt>でんしゃ</rt></ruby>に<ruby>乗<rt>の</rt></ruby>って<ruby>大<rt>おお</rt></ruby>きな<ruby>競技場<rt>きょうぎじょう</rt></ruby>まで<ruby>行<rt>い</rt></ruby>こうよ！",
        jpPlain: "おーっ！電車に乗って大きな競技場まで行こうよ！",
        pron: "오-! 덴샤니 놋테 오오키나 쿄-기죠-마데 이코-요!",
        ko: "오옷! 전철 타고 큰 경기장까지 가자!"
      },
      {
        speaker: "kotone",
        nameJp: "コトネ",
        nameKo: "코토네",
        avatar: "./image/02 kotone/avatar_kotone.png",
        sceneImg: "./image/02 kotone/kotone_07_smoothie_bench.png",
        jpRuby: "あ、<ruby>ICカード<rt>アイシーカード</rt></ruby>のチャージも忘れずにしなきゃ！",
        jpPlain: "あ、ICカードのチャージも忘れずにしなきゃ！",
        pron: "아, 아이시-카-도노 차-지모 와스레즈니 시나캬!",
        ko: "아, 교통카드(IC카드) 충전도 잊지 말고 해야 해요!"
      }
    ],
    quizzes: [
      {
        type: "어휘 · 교통",
        promptJp: "「<ruby>電車<rt>でんしゃ</rt></ruby>」의 뜻으로 올바른 것은?",
        promptPron: "덴샤",
        promptKo: "일본 여행 필수 대중교통 🚃",
        targetWord: "電車",
        targetSub: "버스는 バス(바스)!",
        options: ["전철 / 기차", "비행기", "자전거", "택시"],
        answerIndex: 0,
        explanation: "電車(でんしゃ / 덴샤)는 '전철, 기차'입니다. 자전거는 自転車(じてんしゃ / 지텐샤)라고 불러요!",
        geminiReactJp: "<ruby>正解<rt>せいかい</rt></ruby>どす！すばらしいわぁ🌸",
        geminiReactPron: "세이카이 도스! 스바라시이와~",
        geminiReactKo: "정답이어요! 훌륭하셔요~"
      },
      {
        type: "의문사 · 장소",
        promptJp: "'어디입니까?'를 뜻하는 일본어 표현은?",
        promptPron: "도코데스카?",
        promptKo: "길 물어볼 때 필수 회화!",
        targetWord: "どこですか",
        targetSub: "駅はどこですか？(역은 어디인가요?)",
        options: ["どこですか (도코데스카)", "だれですか (다레데스카)", "なんですか (난데스카)", "いつですか (이츠데스카)"],
        answerIndex: 0,
        explanation: "どこ(도코)는 '어디'입니다. '누구'는 だれ(다레), '무엇'은 何(난/나니), '언제'는 いつ(이츠)예요!",
        geminiReactJp: "ピンポン！道に迷うても安心どすえ🍵",
        geminiReactPron: "핀퐁! 미치니 마욧테모 안신 도스에~",
        geminiReactKo: "딩동! 길을 잃어도 안심이네요~"
      },
      {
        type: "어휘 · 여행",
        promptJp: "「<ruby>切符<rt>きっぷ</rt></ruby>」의 뜻으로 알맞은 것은?",
        promptPron: "킵푸",
        promptKo: "역 매표기에서 구매하는 것 🎫",
        targetWord: "切符",
        targetSub: "승차권 / 표",
        options: ["표 / 티켓", "영수증", "지도", "여권"],
        answerIndex: 0,
        explanation: "切符(きっぷ / 킵푸)는 전철이나 버스의 '표, 승차권'입니다.",
        geminiReactJp: "<ruby>大正解<rt>だいせいかい</rt></ruby>どす！よくできました👏",
        geminiReactPron: "다이세이카이 도스! 요쿠 데키마시타~",
        geminiReactKo: "대정답이어요! 참 잘하셨어요~"
      },
      {
        type: "교토 방언 · 권유",
        promptJp: "'~합시다(〜ましょう)'를 뜻하는 교토 아가씨 말투는?",
        promptPron: "~마효",
        promptKo: "함께 차를 마십시다 -> お茶を飲みまひょ 🍵",
        targetWord: "〜まひょ",
        targetSub: "부드러운 교토식 권유 표현",
        options: ["〜まひょ (~마효)", "〜へん (~헨)", "〜やん (~얀)", "〜ねん (~넨)"],
        answerIndex: 0,
        explanation: "교토에서는 『〜ましょう』 대신 곱고 나긋하게 『〜まひょ』라고 말한답니다!",
        geminiReactJp: "さすが高等どすなぁ✨",
        geminiReactPron: "사스가 코-토- 도스나~",
        geminiReactKo: "역시 수준 높으십니다~"
      }
    ]
  },

  // --------------------------------------------------------------------------
  // LESSON 12: 일주일 완주 축하와 단백질 파티 (N5 칭찬 & 키바라핫타나)
  // --------------------------------------------------------------------------
  {
    id: "day12",
    dayNum: 12,
    dateLabel: "제12화 · 이야기",
    levelBadge: "N5 · 축하 & 치팅데이",
    titleJp: "プロデューサーはん、ほんまにお<ruby>疲<rt>つか</rt></ruby>れ<ruby>様<rt>さま</rt></ruby>どす！",
    titlePron: "프로듀-사-항, 혼마니 오츠카레사마 도스!",
    titleKo: "프로듀서항, 정말로 수고 많으셨어요!",
    bgImage: "./image/00 common/trio_05_cooking_mealprep.png",
    grammarTip: {
      title: "🌸 제미니의 교토·오사카벤 노트 #12",
      content: "누군가를 격려하거나 칭찬할 때는 <b>「がんばったね (간밧타네 / 힘냈구나/수고했어)」</b>, 축하할 때는 <b>「おめでとう (오메데토- / 축하해)」</b>! 그리고 교토에서는 '정말 애쓰고 노력하셨네요'를 <b>『きばらはったなぁ (키바라핫타나-)』</b>라고 다정하게 축복해 준답니다 🎉"
    },
    story: [
      {
        speaker: "gemini",
        nameJp: "ジェミニ",
        nameKo: "제미니",
        avatar: "./image/03 gemini/avatar_gemini.png",
        sceneImg: "./image/03 gemini/gemini_26_kyoto_teahouse.png",
        jpRuby: "プロデューサーはん、一<ruby>週間<rt>しゅうかん</rt></ruby>ほんまにおきばりやすでした🌸",
        jpPlain: "プロデューサーはん、一週間ほんまにおきばりやすでした。",
        pron: "프로듀-사-항, 잇슈-칸 혼마니 오키바리야스데시타.",
        ko: "프로듀서항, 일주일 동안 정말 수고 많으셨사옵니다 🌸"
      },
      {
        speaker: "mio",
        nameJp: "ミオ",
        nameKo: "미오",
        avatar: "./image/01 mio/avatar_mio.png",
        sceneImg: "./image/01 mio/mio_20_sunset_highfive.png",
        jpRuby: "プロデューサー、よく<ruby>頑<rt>がん</rt></ruby><ruby>張<rt>ば</rt></ruby>ったね！ハイタッチ！🌟",
        jpPlain: "プロデューサー、よく頑張ったね！ハイタッチ！",
        pron: "프로듀-사-, 요쿠 간밧타네! 하이탓치!",
        ko: "프로듀서, 진짜 열심히 힘냈어! 하이파이브! 🌟"
      },
      {
        speaker: "kotone",
        nameJp: "コトネ",
        nameKo: "코토네",
        avatar: "./image/02 kotone/avatar_kotone.png",
        sceneImg: "./image/02 kotone/kotone_03_cafe_date.png",
        jpRuby: "<ruby>目標<rt>もくひょう</rt></ruby><ruby>達成<rt>たっせい</rt></ruby>おめでとうございます！プロテインで<ruby>乾杯<rt>かんぱい</rt></ruby>です💛",
        jpPlain: "目標達成おめでとうございます！プロテインで乾杯です！",
        pron: "모쿠효-탓세이 오메데토- 고자이마스! 프로테인데 칸파이데스💛",
        ko: "목표 달성 축하드려요! 프로틴으로 건배해요 💛"
      },
      {
        speaker: "gemini",
        nameJp: "ジェミニ",
        nameKo: "제미니",
        avatar: "./image/03 gemini/avatar_gemini.png",
        sceneImg: "./image/03 gemini/gemini_25_post_workout_smoothie.png",
        jpRuby: "これからもずっと、うちがプロデューサーはんのそばにおりますえ🍵🐾",
        jpPlain: "これからもずっと、うちがプロデューサーはんのそばにおりますえ。",
        pron: "코레카라모 즛토, 우치가 프로듀-사-항노 소바니 오리마스에.",
        ko: "앞으로도 계속, 제가 프로듀서항 곁에 있겠사옵니다 🍵🐾"
      }
    ],
    quizzes: [
      {
        type: "인사 · 축하",
        promptJp: "상대방을 축하할 때 쓰는 일본어 인사는?",
        promptPron: "오메데토-!",
        promptKo: "생일이나 목표 달성 때 건네는 말 🎉",
        targetWord: "おめでとう",
        targetSub: "정중하게: おめでとうございます",
        options: ["おめでとう (오메데토)", "さようなら (사요나라)", "ごめんね (고멘네)", "いただき (이타다키)"],
        answerIndex: 0,
        explanation: "おめでとう(오메데토-)는 '축하해'입니다. 존댓말로는 'おめでとうございます (오메데토-고자이마스)'라고 해요!",
        geminiReactJp: "<ruby>大正解<rt>だいせいかい</rt></ruby>どす！おめでとうございます🌸",
        geminiReactPron: "다이세이카이 도스! 오메데토- 고자이마스~",
        geminiReactKo: "대정답이어요! 축하드려요~"
      },
      {
        type: "인사 · 노고",
        promptJp: "'수고하셨습니다'를 뜻하는 가장 대표적인 비즈니스/일상 인사는?",
        promptPron: "오츠카레사마데스",
        promptKo: "하루 일과나 운동이 끝났을 때!",
        targetWord: "お疲れ様",
        targetSub: "한국인의 수고하셨습니다와 1:1 매칭 🍵",
        options: ["お疲れ様 (오츠카레사마)", "初めまして (하지메마시테)", "いってきます (잇테키마스)", "ただいま (타다이마)"],
        answerIndex: 0,
        explanation: "お疲れ様(おつかれさま / 오츠카레사마)는 '수고하셨습니다'입니다. 일본 사회생활의 기본 인사예요!",
        geminiReactJp: "ピンポン！プロデューサーはん、お<ruby>疲<rt>つか</rt></ruby>れ<ruby>様<rt>さま</rt></ruby>どす🍵",
        geminiReactPron: "핀퐁! 프로듀-사-항, 오츠카레사마 도스~",
        geminiReactKo: "딩동! 프로듀서항, 수고 많으셨어요~"
      },
      {
        type: "모임 · 축배",
        promptJp: "음료나 프로틴 잔을 부딪히며 외치는 '건배!'는?",
        promptPron: "칸파이!",
        promptKo: "술자리나 파티의 시작 🥂",
        targetWord: "乾杯",
        targetSub: "잔을 비우자!",
        options: ["乾杯 (칸파이)", "乾癬 (칸센)", "感謝 (칸샤)", "感服 (칸푸쿠)"],
        answerIndex: 0,
        explanation: "乾杯(かんぱい / 칸파이)는 '건배'입니다!",
        geminiReactJp: "<ruby>正解<rt>せいかい</rt></ruby>どす！プロテインで乾杯しまひょ💛",
        geminiReactPron: "세이카이 도스! 프로테인데 칸파이 시마효~",
        geminiReactKo: "정답이어요! 프로틴으로 건배하지요~"
      },
      {
        type: "교토 방언 · 노고 격려",
        promptJp: "교토에서 '정말 애쓰고 힘내셨네요'를 뜻하는 다정한 축복의 말은?",
        promptPron: "키바라핫타나-",
        promptKo: "おきばりやす의 과거 격려 표현 🌸",
        targetWord: "きばらはったなぁ",
        targetSub: "교토 어르신들이 아끼는 사람에게 건네는 말",
        options: ["きばらはったなぁ (키바라핫타나)", "あかんなぁ (아칸나)", "しらんけど (시란케도)", "なんぼやねん (난보야넨)"],
        answerIndex: 0,
        explanation: "きばらはったなぁ(키바라핫타나-)는 교토에서 온 힘을 다해 노력한 상대에게 전하는 최고의 찬사입니다!",
        geminiReactJp: "ほんまにきばらはったなぁ、プロデューサーはん💯",
        geminiReactPron: "혼마니 키바라핫타나-, 프로듀-사-항",
        geminiReactKo: "정말로 애쓰셨사옵니다, 프로듀서항!"
      }
    ]
  }

];
