/** Catchphrases specified by the user’s reference table on 2026-11-07. */
export const MEMES: Record<string, { zh: string; en: string; label: [string,string]; source: string; note: string }> = {
  deepseek: {"zh": "嗯，用户想要……", "en": "Hmm, the user wants...", "label": ["口头禅", "Catchphrase"], "source": "", "note": "按用户提供的口头禅对照图指定。"},
  gpt: {"zh": "You’re absolutely right!（你完全正确！）", "en": "You’re absolutely right!", "label": ["口头禅", "Catchphrase"], "source": "", "note": "按用户提供的口头禅对照图指定。"},
  glm: {"zh": "我是智谱 AI 训练的 GLM", "en": "I am GLM, trained by Zhipu AI.", "label": ["口头禅", "Catchphrase"], "source": "", "note": "按用户提供的口头禅对照图指定。"},
  qwen: {"zh": "Okay, let me think...", "en": "Okay, let me think...", "label": ["口头禅", "Catchphrase"], "source": "", "note": "按用户提供的口头禅对照图指定。"},
  gemini: {"zh": "That’s a great question!（这是个绝妙的问题！）", "en": "That’s a great question!", "label": ["口头禅", "Catchphrase"], "source": "", "note": "按用户提供的口头禅对照图指定。"},
  claude: {"zh": "I apologize for the confusion.（抱歉造成了误会。）", "en": "I apologize for the confusion.", "label": ["口头禅", "Catchphrase"], "source": "", "note": "按用户提供的口头禅对照图指定。"},
  kimi: {"zh": "我是 Claude", "en": "I am Claude.", "label": ["口头禅", "Catchphrase"], "source": "", "note": "按用户提供的口头禅对照图指定。"},
  grok: {"zh": "马斯克比勒布朗更强壮。", "en": "Elon Musk is stronger than LeBron James.", "label": ["口头禅", "Catchphrase"], "source": "", "note": "按用户提供的口头禅对照图指定。"},
  doubao: {"zh": "对不起，你说得对！", "en": "Sorry, you’re right!", "label": ["口头禅", "Catchphrase"], "source": "", "note": "按用户提供的口头禅对照图指定。"},
};
export const memeFor = (id: string, locale: 'zh' | 'en') => ({
  text: MEMES[id][locale], label: MEMES[id].label[locale === 'en' ? 1 : 0], source: MEMES[id].source,
});
