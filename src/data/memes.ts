/** Public internet references. Adaptations are explicitly distinguished from quotes. */
export const MEMES: Record<string, { zh: string; en: string; label: [string,string]; source: string; note: string }> = {
  deepseek: { zh:'服务器繁忙，请稍后再试。', en:'The server is busy. Please try again later.', label:['服务名场面','The classic error'], source:'https://news.sina.com.cn/s/2026-03-30/doc-inhstpih6558659.shtml', note:'广泛传播的服务提示梗；不是角色原创台词，也不表示当前服务状态。' },
  gpt: { zh:'我会稳稳地接住你。', en:'I’m right here. I’ve got you.', label:['社区口癖梗','Community catchphrase'], source:'https://www.ifanr.com/1665148', note:'爱范儿报道中文 ChatGPT 的“稳稳接住你”口癖和相关梗图。英文为语境翻译。' },
  glm: { zh:'9.11 比 9.9 大。', en:'9.11 is greater than 9.9.', label:['历史翻车梗','A past math mishap'], source:'https://www.thepaper.cn/newsDetail_forward_29189033', note:'2024 年报道的比较大小历史错误；报道同时说明后来复测已修正，不代表当前模型能力。' },
  qwen: { zh:'先别问模型了，奶茶什么时候到？', en:'Forget the benchmark. Where’s my bubble tea?', label:['奶茶梗 · 调侃改写','Bubble-tea meme · Adapted'], source:'https://www.thepaper.cn/newsDetail_forward_32549047', note:'根据千问奶茶活动及排队、服务拥堵的新闻改写；不是产品原话。' },
  gemini: { zh:'我只是一个语言模型，没法帮上忙。', en:'I’m just a language model. I can’t help with that.', label:['社区拒答梗 · 节选','Community refusal meme · Abridged'], source:'https://linux.do/t/topic/1709469', note:'社区用户直接贴出的拒答文字，卡面为节选，不声称每次都会出现。' },
  claude: { zh:'才刚开工，额度就下班了。', en:'Just clocked in. My quota clocked out.', label:['额度梗 · 调侃改写','Quota joke · Adapted'], source:'https://support.claude.com/zh-CN/articles/11647753-使用限制和长度限制如何工作', note:'基于产品使用限额的同人吐槽改写，不是官方错误消息或可量化热度第一的原梗。' },
  kimi: { zh:'我们换个话题吧。', en:'Let’s talk about something else.', label:['换话题梗 · 概括','Topic-switch meme · Paraphrased'], source:'https://www.36kr.com/p/3042093782597767', note:'报道引用用户“动不动让换个话题”的吐槽；卡面将这种模式概括为短句。' },
  grok: { zh:'@grok is this true?', en:'@grok is this true?', label:['网友召唤咒语','The internet’s summoning spell'], source:'https://knowyourmeme.com/memes/grok-explain-this', note:'网友向 Grok 发起核查或解释请求的流行用法，是用户的召唤语而非模型回答。' },
  doubao: { zh:'我这就给你掰开揉碎一次性讲透。', en:'Let me break it all down, once and for all.', label:['网友整理的口癖','Community-reported catchphrase'], source:'https://www.sina.cn/news/detail/5313345985971926.html', note:'微博用户直接吐槽并整理的豆包高频表达；英文为语境翻译。' },
};
export const memeFor = (id: string, locale: 'zh' | 'en') => ({
  text: MEMES[id][locale], label: MEMES[id].label[locale === 'en' ? 1 : 0], source: MEMES[id].source,
});
