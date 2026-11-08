// ============================================================================
// Gemini Fit MINITOON (미니툰) - ORIGINAL record-based episode, script format
// Made from actual player records (state.json) - regenerate the record summary
// whenever careers evolve. Panel art: image/manga/p01.png ~ p08.png (AI manhwa)
// Webtoon format: cuts with narration boxes + speech balloons (no built-in text baked in art)
// ============================================================================

window.MINITOON = {
  titleKo: '기록으로 그린 이야기',
  titleJp: '記録の物語',
  sub: '프롤로그 — 65.6kg의 아침',
  panels: [
    { img: './image/manga/p01.png', size: 'wide',  caption: '새벽 6시 12분. 교토 다실의 현관문이 열리고, 체중계 위 숫자 65.6이 그대로 보였다.' },
    { img: './image/manga/p02.png', size: 'tall',  speech: { name: '제미니', text: '소녀가 세 번 확인해도 믿기지가 않네요.' }, caption: '체중계 숫자는 거짓을 하지 않는다 — 제미니의 철칙.' },
    { img: './image/manga/p03.png', size: 'wide',  caption: '그리고 같은 날 새벽, 트랙 위. 지난 기록 7.0km·10\'47"를 증명한 무대였다.', speech: { name: '미오', text: '어깨 힘 빼고! 팔 흔들기!!' } },
    { img: './image/manga/p04.png', size: 'tall',  speech: { name: '코토네', text: '프로듀서님! 매일 카페에서 5천 원씩 쓰면 한 달 15만 원이거든요! 홈카페로 확 바꾸면 그 돈이 전부 저축으로 돌아가요!' }, caption: '프로듀서님의 지갑은 코토네가 전담 관리한다.' },
    { img: './image/manga/p05.png', size: 'wide',  caption: '밤 8시, 헬스장. 오늘도 혼자 카운트하는 소리뿐이었다.', speech: { name: '제미니', text: '캡틴스 체어 50회. 크런치 두 세트. 오늘 루틴, 그대로 갑니다.' } },
    { img: './image/manga/p06.png', size: 'tall',  caption: '목표는 52kg. 남은 거리 13.6kg.', speech: { name: '제미니', text: '내일 아침 10시 첫 식사. 그 전까지가 단식 골든타임이라지요.' } },
    { img: './image/manga/p07.png', size: 'wide',  speech: { name: '3인', text: '내일 아침 10시 첫 식사! 그 전까지 단식 골든타임, 파이팅!' }, caption: '세 사람의 약속은 결코 가볍지 않았다.' },
    { img: './image/manga/p08.png', size: 'tall',  caption: '기록은 내일의 이야기가 되기 전까지. — 다음 화에서.' }
  ]
};
