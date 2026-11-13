export type Character = {
  id: string; brand: string; name: string; alias: string; code: string;
  color: string; ink: string; image: string; imageWidth: number; imageHeight: number;
  role: string; title: [string, string]; caption: string; motto: string;
  summary: string; features: string[]; url: string; chat: string;
  credit: string; portraitPosition?: string; portraitImage?: string; portraitTransparent?: boolean;
};

export const GITHUB_URL = 'https://github.com/fanhuayishiy';
export const PROJECT_GITHUB_URL = 'https://github.com/fanhuayishiy/ai-crew-pass';
export const ART_SOURCE = 'https://www.bilibili.com/opus/1233069202138464289';
export const CHARACTERS: Character[] = [
  { id:'deepseek', brand:'deepseek', name:'鲸鱼娘', alias:'Whale-chan', code:'DS', color:'#4964a0', ink:'#29365b', image:'deepseek.png', imageWidth:1152, imageHeight:2048, portraitImage:'img/deepseek/maid.webp', portraitTransparent:true,
    role:'灵感探索部 / 首席思考搭子', title:['潜入思考，','捞起灵感。'],caption:'今天，也和小鲸鱼一起探索。',motto:'认真思考，偶尔摸鱼。你的问题，我想再深一点。',
    summary:'蓝色长发、鲸鳍与鲸尾，深蓝白女仆裙。向深处再想一步，是小鲸鱼的工作日常。',features:['蓝色长发 · 鲸鳍 · 鲸尾','深蓝白女仆装 · 鲸鱼围裙','社区昵称：蓝色大肥鱼'],url:'https://www.deepseek.com/',chat:'https://chat.deepseek.com/',credit:'原角色：上善无形 / 女仆设计：ZipZipPipe' },
  { id:'gpt', brand:'ChatGPT', name:'白龙娘', alias:'Dragon-chan', code:'GPT', color:'#9b86bc',ink:'#4b3b66',image:'gpt.jpg',imageWidth:3072,imageHeight:5504,
    role:'创意共研部 / 万事好奇搭子',title:['展开想象，','让灵感生长。'],caption:'和小白龙，一起把想法说出来。',motto:'保持好奇，展开想象。每一个念头，都值得聊聊。',summary:'白色长发、龙角与龙翼，层叠的白紫礼服。像一封写给未知的邀请函，温柔而充满好奇。',features:['白色长发 · 龙角 · 龙翼','白紫礼服 · 长长的龙尾','社区同人形象：GPT 白龙娘'],url:'https://chatgpt.com/',chat:'https://chatgpt.com/',credit:'角色设计：ZipZipPipe' },
  { id:'glm',brand:'GLM',name:'阔耳狐娘',alias:'Fennec-chan',code:'GLM',color:'#575f75',ink:'#2e3243',image:'glm.png',imageWidth:1152,imageHeight:2048,
    role:'安静研究所 / 专注阅读搭子',title:['安静一点，','把思路理清。'],caption:'把纷繁的问题，慢慢整理成答案。',motto:'静下心，读懂细节。把复杂的问题，一点点说清。',summary:'黑色长发、醒目的大狐耳，黑白女仆装与书卷。克制的灰蓝配色，像一间安静的书房。',features:['黑色长发 · 阔耳狐特征','黑白女仆装 · 书本配件','采用原帖 GLM 角色版本'],url:'https://chatglm.cn/',chat:'https://chatglm.cn/',credit:'角色设计：ZipZipPipe' },
  { id:'qwen',brand:'Qwen',name:'千问娘',alias:'Qwen-chan',code:'QW',color:'#6669b3',ink:'#34365b',image:'qwen.jpg',imageWidth:3072,imageHeight:5504,
    role:'万象问答部 / 博闻探索搭子',title:['万千问题，','总有新发现。'],caption:'一问一答之间，打开更大的世界。',motto:'一问万千，步步发现。你的好奇心，我认真接住。',summary:'蓝紫长发与东方风格服饰，折扇、发饰与细密纹样相互呼应。让好奇心，从一问走向万千。',features:['蓝紫长发 · 东方服饰','折扇与精致发饰','采用 ZipZipPipe 千问娘版本'],url:'https://www.qianwen.com/',chat:'https://www.qianwen.com/',credit:'角色设计：ZipZipPipe' },
  { id:'gemini',brand:'Gemini',name:'双子猫娘',alias:'Gemini-chan',code:'GM',color:'#9161c6',ink:'#44305f',image:'gemini.jpg',imageWidth:3072,imageHeight:5504,
    role:'星光灵感部 / 多面创作搭子',title:['换个视角，','发现另一面。'],caption:'让一个想法，闪出不一样的光。',motto:'抬头看星星，低头捡灵感。每次好奇，都有新可能。',summary:'紫色长发、猫耳和星形装饰，明亮的紫蓝色层次。像一颗灵感星星，总想换个角度看看。',features:['紫色渐变长发 · 猫耳','星形装饰 · 紫蓝服饰','采用 ZipZipPipe Gemini 娘版本'],url:'https://gemini.google.com/',chat:'https://gemini.google.com/',credit:'角色设计：ZipZipPipe' },
  { id:'claude',brand:'Claude',name:'暖橘娘',alias:'Claude-chan',code:'CL',color:'#ba7159',ink:'#653f36',image:'claude.jpg',imageWidth:3072,imageHeight:5504,
    role:'文字工坊 / 耐心共写搭子',title:['把话写好，','把想法说清。'],caption:'用一点耐心，照顾每一个细节。',motto:'慢慢读，认真写。把未成形的念头，变成清楚的话。',summary:'暖橘长发与奶白色女仆装，细致的层叠裙摆。温暖而沉静的色调，适合一起读写的午后。',features:['橘红长发 · 奶白长裙','暖橘与棕色细节','采用 ZipZipPipe Claude 娘版本'],url:'https://claude.ai/',chat:'https://claude.ai/',credit:'角色设计：ZipZipPipe' },
  { id:'kimi',brand:'Kimi',name:'月白娘',alias:'Kimi-chan',code:'KM',color:'#7779ad',ink:'#353750',image:'kimi.png',imageWidth:1152,imageHeight:2048,
    role:'月光资料室 / 长文阅读搭子',title:['翻过长页，','找到那束光。'],caption:'从字里行间，拾起重要的线索。',motto:'故事很长，我们慢慢读。那些细小线索，都值得留下。',summary:'月白色长发、深蓝白礼服与月夜气质。把散落的文字连起来，像在星空里寻找新的航线。',features:['月白长发 · 深蓝白礼服','月夜色彩与精致饰品','采用 ZipZipPipe Kimi 娘版本'],url:'https://www.kimi.com/',chat:'https://www.kimi.com/',credit:'角色设计：ZipZipPipe' },
  { id:'grok',brand:'Grok',name:'金发娘',alias:'Grok-chan',code:'GK',color:'#ac884b',ink:'#57472e',image:'grok.jpg',imageWidth:3072,imageHeight:5504,
    role:'奇想观察站 / 直率聊天搭子',title:['跳出常规，','聊点新鲜的。'],caption:'给每一次对话，留一点意外。',motto:'敢想一点，直说一点。给平常的日子，加一点新鲜。',summary:'金色长发、黑色礼服和酒红裙饰。金、黑、红的对比鲜明，带着一点俏皮的反差。',features:['金色长发 · 黑色礼服','酒红色裙饰 · 蝴蝶结','采用 ZipZipPipe Grok 娘版本'],url:'https://grok.com/',chat:'https://grok.com/',credit:'角色设计：ZipZipPipe' },
  { id:'doubao',brand:'豆包',name:'豆包',alias:'Doubao',code:'DB',color:'#b9343c',ink:'#4d3034',image:'doubao-anime-v4.png',imageWidth:941,imageHeight:1672,portraitTransparent:true,
    role:'日常陪伴部 / 生活灵感搭子',title:['接住日常，','聊聊小美好。'],caption:'围上一条红围巾，今天也温暖一点。',motto:'生活里的小问题，也值得认真回答。今天想聊点什么？',summary:'棕色短发、红色长围巾、黑色西装短裙与长靴。与其他 AI 同事统一的动漫立绘，直接融入同色工牌。',features:['棕色短发 · 红色针织长围巾','黑色西装短裙 · 长靴 · 银色腰链','本项目 AI 生成的非官方动漫形象'],url:'https://www.doubao.com/',chat:'https://www.doubao.com/',credit:'本项目 AI 生成同人形象 / 外观参考用户截图，画风参考现有角色' },
  { id:'jensen',brand:'AMD',name:'黄仁勋',alias:'Jensen Huang',code:'JH',color:'#b9343c',ink:'#4d3034',image:'jensen.webp',imageWidth:1254,imageHeight:1254,portraitImage:'img/jensen/portrait.webp',portraitTransparent:true,
    role:'返厂体验官 / 黑皮衣事业部',title:['出走半生，','归来仍是打工人。'],caption:'虚构玩梗：不代表黄仁勋已加入 AMD。',motto:'出走半生，归来仍是打工人。这次，换张红卡继续上班。',
    summary:'黄仁勋 AMD 返厂工牌是虚构玩梗，不代表真实入职。人物形象由 AI 生成。',features:['老东家：AMD','黑皮衣不换 · 阵营换红','虚构入职 · 非官方玩梗'],url:'https://www.hoover.org/plus/research/jensen-huang-vision-risk-and-gpu',chat:'https://www.hoover.org/plus/research/jensen-huang-vision-risk-and-gpu',credit:'人物形象由 AI 生成 · 虚构玩梗' },
];

export function mix(hex: string, white: number): string {
  return '#'+[1,3,5].map(i=>Math.round(parseInt(hex.slice(i,i+2),16)*(1-white)+255*white).toString(16).padStart(2,'0')).join('');
}
export function characterStyle(c: Character): string {
  return Object.entries({brand:c.color,ink:c.ink,paper:mix(c.color,.94),card:c.id==='deepseek'?'#e1ebfa':mix(c.color,.87),muted:mix(c.ink,.35),soft:mix(c.color,.79),line:mix(c.color,.72),light:mix(c.color,.25),deep:mix(c.ink,.04)})
    .map(([key,value])=>`--theme-${key}:${value}`).join(';');
}
export const baseUrl = () => import.meta.env.BASE_URL.replace(/\/$/,'');
export const characterUrl = (c: Character) => c.id==='deepseek' ? `${baseUrl()}/` : `${baseUrl()}/characters/${c.id}/`;
