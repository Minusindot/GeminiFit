// ============================================================================
// 言の葉茶屋 (Kotonoha Chaya) - Quiz anti-spoiler audit
//
// Guards the rule that a question must never reveal its own answer:
//   1. promptJp must not contain the correct option
//   2. promptKo (the sub-hint under the question) must not contain the answer
//      or its reading — this is where "한자: 改札口" style leaks used to live
//   3. options must not contain duplicates
//   4. a target card equal to the correct option is listed as "masked", because
//      kotonoha_engine.js swaps it for the Korean cue at runtime
//
// Usage: node tools/audit_quiz_leaks.js
// Exit code 1 means the quiz data would show the answer before the user picks.
// ============================================================================
const fs = require('fs');
const path = require('path');
const vm = require('vm');

const root = path.resolve(__dirname, '..');
const sandbox = { window: {}, console };
vm.createContext(sandbox);
vm.runInContext(fs.readFileSync(path.join(root, 'kotonoha_data.js'), 'utf8'), sandbox);

const lessons = sandbox.window.KOTONOHA_LESSONS || [];

const stripRuby = (v) => String(v == null ? '' : v).replace(/<rt>.*?<\/rt>/gi, '').replace(/<[^>]+>/g, '');
const compact = (v) => stripRuby(v)
  .replace(/（[^）]*）|\([^)]*\)/g, '')
  .replace(/[\s\u3000~〜\-－·.。、/／]/g, '');
const jpPart = (opt) => {
  const s = stripRuby(opt);
  const m = s.match(/^(.*?)[（(]/);
  return (m ? m[1] : s).trim();
};
const readingPart = (opt) => {
  const m = stripRuby(opt).match(/[（(]([^）)]*)[）)]/);
  return m ? m[1].trim() : '';
};

const errors = [];
const masked = [];
let total = 0;

for (const lesson of lessons) {
  (lesson.quizzes || []).forEach((quiz, idx) => {
    total += 1;
    const label = `${lesson.id || lesson.dayNum} Q${idx + 1} (${quiz.type || 'quiz'})`;
    const options = quiz.options || [];
    const answer = options[quiz.answerIndex];
    if (answer == null) {
      errors.push(`${label}: answerIndex ${quiz.answerIndex} is out of range`);
      return;
    }

    const answerText = compact(jpPart(answer));
    const answerReading = compact(readingPart(answer));
    const prompt = compact(quiz.promptJp);
    const promptKo = compact(quiz.promptKo);

    if (answerText.length >= 2 && prompt.includes(answerText)) {
      errors.push(`${label}: prompt already contains the answer "${answer}"`);
    }
    if (answerText.length >= 1 && promptKo.includes(answerText)) {
      errors.push(`${label}: promptKo already contains the answer "${answer}"`);
    } else if (answerReading.length >= 2 && promptKo.includes(answerReading)) {
      errors.push(`${label}: promptKo already contains the answer reading "${answer}"`);
    }

    const seen = new Set();
    options.forEach((option) => {
      const key = compact(option);
      if (!key) return;
      if (seen.has(key)) errors.push(`${label}: duplicate option "${option}"`);
      seen.add(key);
    });

    const targetKey = compact(quiz.targetWord);
    const optionKey = compact(answer);
    if (targetKey && optionKey && (optionKey.includes(targetKey) || targetKey.includes(optionKey))) {
      masked.push(label);
    }
  });
}

console.log(`audited ${total} quizzes in ${lessons.length} lessons`);
console.log(`masked at runtime (target card → Korean cue): ${masked.length}`);
if (masked.length) masked.forEach((m) => console.log(`  · ${m}`));

if (errors.length) {
  console.error(`\n${errors.length} spoiler problem(s):`);
  errors.forEach((e) => console.error(`  ✗ ${e}`));
  process.exit(1);
}

console.log('\nOK: no quiz prompt reveals its own answer.');
