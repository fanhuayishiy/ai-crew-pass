import { memeFor } from './memes';
import { CHARACTERS, baseUrl, type Character } from './characters';
export type Locale = 'zh' | 'en';
const english: Record<string, Partial<Character>> = {
  deepseek: { name:'Whale-chan', role:'Inspiration Lab / Thinking Partner', title:['Dive into thought.','Surface with ideas.'], caption:'A little deeper, together.', motto:'Think deeply. Drift a little. Your questions deserve another dive.', summary:'Blue hair, whale fins and a sweeping tail, paired with a navy-and-white maid dress. Always ready to explore one layer deeper.', features:['Blue hair, whale fins and tail','Navy-and-white dress with a whale apron','Community nickname: the big blue whale'], credit:'Original character: Shangshan Wuxing / Maid design: ZipZipPipe' },
  gpt: { name:'Dragon-chan', role:'Creative Studio / Curious Collaborator', title:['Unfold imagination.','Let ideas grow.'], caption:'Give your next idea a little room to breathe.', motto:'Stay curious. Imagine freely. Every little idea is worth a conversation.', summary:'White hair, dragon horns and wings, with a layered white-and-lilac gown. A gentle invitation to explore the unknown.', features:['White hair, dragon horns and wings','White-and-lilac gown, long dragon tail','Community fan character: GPT Dragon-chan'], credit:'Character design: ZipZipPipe' },
  glm: { name:'Fennec-chan', role:'Quiet Study / Focused Reading Partner', title:['Find some quiet.','Find your clarity.'], caption:'Untangle a complicated question, one detail at a time.', motto:'Slow down. Read the details. Make the complicated a little clearer.', summary:'Dark hair, oversized fox ears and a monochrome maid outfit with books. A restrained blue-grey palette, like a quiet study.', features:['Dark hair and oversized fennec ears','Black-and-white maid outfit, books','Based on the original GLM fan design'], credit:'Character design: ZipZipPipe' },
  qwen: { name:'Qwen-chan', role:'Discovery Desk / Knowledge Explorer', title:['A thousand questions.','A new discovery.'], caption:'One question can open a whole new world.', motto:'Ask widely. Discover daily. Bring your curiosity along.', summary:'Blue-violet hair and an Eastern-inspired outfit, with a folding fan, delicate hair ornaments and intricate patterns.', features:['Blue-violet hair, Eastern-inspired outfit','Folding fan and delicate hair ornaments','Based on ZipZipPipe’s Qwen fan design'], credit:'Character design: ZipZipPipe' },
  gemini: { name:'Gemini-chan', role:'Starlight Studio / Creative Companion', title:['Shift your view.','Find a new spark.'], caption:'Let one idea shine in more than one way.', motto:'Look up at the stars. Gather little sparks. Curiosity opens possibilities.', summary:'Purple hair, cat ears and star-shaped details in luminous violet and blue. Always curious to see things from another angle.', features:['Purple gradient hair and cat ears','Star details, violet-and-blue outfit','Based on ZipZipPipe’s Gemini fan design'], credit:'Character design: ZipZipPipe' },
  claude: { name:'Claude-chan', role:'Writing Workshop / Thoughtful Co-writer', title:['Find the words.','Make ideas clear.'], caption:'A little patience for every detail.', motto:'Read slowly. Write thoughtfully. Give your ideas a clearer shape.', summary:'Warm orange hair and an ivory maid dress with a finely layered skirt. A calm, warm palette for an afternoon of reading and writing.', features:['Orange hair and a long ivory dress','Warm orange and brown accents','Based on ZipZipPipe’s Claude fan design'], credit:'Character design: ZipZipPipe' },
  kimi: { name:'Kimi-chan', role:'Moonlit Library / Long-read Companion', title:['Turn the page.','Follow the light.'], caption:'Pick up the clues between the lines.', motto:'Long story? Take your time. Even the smallest clues deserve a place.', summary:'Moon-white hair and a navy-and-white gown with a quiet night-sky mood. Connecting scattered words into new constellations.', features:['Moon-white hair, navy-and-white gown','Moonlit palette and delicate accessories','Based on ZipZipPipe’s Kimi fan design'], credit:'Character design: ZipZipPipe' },
  grok: { name:'Grok-chan', role:'Ideas Observatory / Candid Companion', title:['Break the routine.','Try a fresh thought.'], caption:'Leave a little room for the unexpected.', motto:'Think boldly. Speak freely. Add a little surprise to the everyday.', summary:'Golden hair, a black gown and wine-red skirt details. A playful contrast of gold, black and red.', features:['Golden hair and a black gown','Wine-red skirt details and bows','Based on ZipZipPipe’s Grok fan design'], credit:'Character design: ZipZipPipe' },
  doubao: { brand:'Doubao', name:'Doubao', role:'Everyday Studio / Daily Inspiration', title:['Share the everyday.','Find little joys.'], caption:'A red scarf and a little warmth for your day.', motto:'Little questions matter, too. What is on your mind today?', summary:'Short brown hair, a long red scarf, a black blazer and skirt, and tall boots. An anime fan character made to fit the crew.', features:['Short brown hair and a knitted red scarf','Black blazer and skirt, boots, silver waist chain','Unofficial AI-generated anime fan character'], credit:'AI-generated fan art / Appearance based on user reference' },
  jensen: { name:'Jensen Huang', alias:'', role:'Returnee / Leather Jacket Division', title:['Back to work,','with a different card.'], caption:'Fictional fan art · not a real job announcement.', motto:'Out in the world for years. Back to work with a red card.', summary:'A fictional Jensen Huang AMD reunion pass, made for fun. This is not a real job announcement. AI-generated portrait.', features:['Former employer: AMD','Same leather jacket · red team','Fictional return · unofficial fan art'], credit:'AI-generated portrait · fictional fan art' },
};
export const localizedCharacter = (c: Character, locale: Locale): Character => locale === 'en' ? {...c,...english[c.id]} : c;
export const localizedCharacters = (locale: Locale) => CHARACTERS.map(c=>localizedCharacter(c,locale));
export const localeCharacterUrl = (c: Character, locale: Locale) => `${baseUrl()}${locale==='en'?'/en':''}${c.id==='deepseek'?'/':`/characters/${c.id}/`}`;
export const characterCatchphrase = (id: string, locale: Locale) => memeFor(id, locale).text;
export function copy(locale: Locale) {
  const en = locale === 'en';
  return {
    siteName: en?'Anything Pass':'万物工牌',
    pickup: en?'Crew Pass Collection Desk':'工牌领取处',
    catchphrase: en?'Internet folklore':'互联网名场面',
    memeSource: en?'Behind the meme ↗':'梗从哪来 ↗',
    switchEmployee: en?'Switch employee':'切换员工',
    credits: en?'Artwork & credits':'素材与署名',
    community: en?'Fenghua AI Lab · WeChat':'风花AI实验室',
    communityIntro: en?'Follow 风花AI实验室 (Fenghua AI Lab) on WeChat for AI projects, practical tools and build notes.':'关注公众号「风花AI实验室」，一起探索 AI 创作、实用工具与有趣实验。获取项目更新与制作分享。',
    communityHint: en?'Scan with WeChat, or save this QR code to open it in WeChat.':'微信扫码关注，也可以保存二维码后在微信中识别。',
    saveQr: en?'Save QR code':'保存公众号二维码',
    close: en?'Close':'关闭',
    downloadSupportTitle: en?'Enjoy your crew pass?':'喜欢这张工牌？',
    downloadSupportText: en?'Star the project on GitHub to support the creator and more little experiments.':'去 GitHub 点个 Star，支持作者继续做有趣的小东西。',
    downloadSupportAction: en?'Star on GitHub':'给项目点个 Star',
    totalViews: en?'Total views':'总浏览量',
    viewsHint: en?'Site-wide page views via Busuanzi. Refreshes and character switches count as views.':'不蒜子统计的全站页面浏览量，刷新和切换角色也会计数。',
    previous: en?'Previous character':'上一位员工', next:en?'Next character':'下一位员工',
    download: en?'Download pass':'下载工牌', downloadBoth:en?'Download both · ZIP':'下载正反面 · ZIP', front:en?'Front · PNG':'正面 · PNG', backImage:en?'Back · PNG':'背面 · PNG', preparing:en?'Preparing…':'正在生成…', downloadHint:en?'Save either PNG or download both as ZIP. On mobile, you can also save the preview image.':'可单独保存透明 PNG 或打包下载；手机也可长按预览图保存。', downloadError:en?'Could not prepare the images. Please try again.':'图片生成失败，请重试。',
    edition: en?'Anything Pass':'万物工牌', official:en?'Website':'官网', gallery:en?'The crew':'员工图鉴',
    choose:en?'Choose a character':'选择角色工作牌', badge:en?'Crew pass':'工作牌', profile:en?'Character profile':'角色资料',
    arrived:en?'is on duty':'已到岗', all:en?'Meet the crew':'查看员工图鉴', chat:en?'Chat with':'聊聊',
    drag:en?'Drag to swing':'拖动摇摆', flip:en?'Click to flip':'点击翻面', unofficial:en?'Unofficial fan pass':'非官方同人工作牌',
    fan:en?'Fan-made crew pass · Unofficial':'同人工作牌 · 非官方出品', sourceNote:en?'Artwork sources and credits below':'原图来源与使用说明见页底',
    noncommercial:en?'Non-commercial showcase · Credits retained':'仅作非商用展示 · 保留原作者署名',
    heading:en?'Meet the crew':'员工图鉴',
    galleryHint:en?'Drag to explore. Click to flip. Open a character’s crew pass.':'左右拖动探索，点击翻面；打开属于 TA 的工作牌。',
    carousel:en?'Character carousel controls':'角色轮播控制', select:en?'Show':'查看', carouselHint:en?'Drag to explore · Click to flip':'左右拖动 · 点击翻面',
    open:en?'Open crew pass':'打开工作牌', back:en?'Back to crew pass':'返回工作牌',
    credit:en?'Original Whale-chan: Shangshan Wuxing · Eight AI character designs: ZipZipPipe · Doubao: AI-generated anime fan art based on the user’s reference, styled to match the crew.':'鲸鱼娘原角色：上善无形 · 八位 AI 娘设计：ZipZipPipe · 豆包：本项目 AI 生成动漫同人形象，外观参考用户截图，画风参考现有角色',
    rights:en?'Unofficial fan project for non-commercial display. Characters and brands belong to their respective owners. Artwork is used under its source-specific terms.':'非官方同人工作牌，仅作非商用展示。角色与品牌权利归原权利人；各素材按来源声明使用。',
    original:en?'Original artwork post':'角色原帖', notice:en?'Artwork notes':'素材说明', galleryBy:en?'Gallery based on':'图鉴基于', physicsBy:en?'Lanyard interaction':'工牌交互',
  };
}
