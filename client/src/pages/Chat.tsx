import { useState, useEffect, useRef } from "react";
import { useLocation, useRoute } from "wouter";
import { motion, AnimatePresence } from "framer-motion";
import { getgamemasterResponseStream, type ChatMessage } from "@/lib/ai-service";
import { ArrowLeft, ArrowUp , RotateCcw , MousePointer2} from "lucide-react";

interface Message {
  role: "user" | "gamemaster";
  content: string;
  timestamp: number;
}

const gamemasterInfo: Record<
  string,
  {
    name: string;
    nameEn: string;
    tagline: string;
    style: string;
    avatar: string;
    greeting: string;
  }
> = {

    Gryffindor: {  
    name: "霍格沃兹大冒险",
    nameEn: "Game Master",
    tagline: "准备开始冒险了吗？",
    style: "沉浸式互动，引人入胜",
    avatar: "/game-avatar.webp",  // 需要添加头像文件
    greeting: "格兰芬多，代表勇气、胆识与骑士精神。\n\n麦格教授的命令在礼堂回荡，但你的心早已飞向城墙。你没有后退，反而向前一步，魔杖尖端迸发出一簇火星，映照着眼中燃烧的火焰。这不是躲藏的时刻——是时候让世人见识，格兰芬多的勇气为何能撕裂黑暗。战斗在召唤，你的每一滴热血都在沸腾。\n\n拔出你的魔杖，输入“开始游戏”，让狮院的怒吼响彻战场！",
  },
    
    Hufflepuff: {  
    name: "霍格沃兹大冒险",
    nameEn: "Game Master",
    tagline: "准备开始冒险了吗？",
    style: "沉浸式互动，引人入胜",
    avatar: "/game-avatar.webp",  // 需要添加头像文件
    greeting: "赫奇帕奇，代表忠诚、公正与坚韧奉献。\n\n面对逼近的黑暗，你并未退缩。你想起斯普劳特教授的教诲：最坚韧的植物，往往生长于最残酷的峭壁。你的魔杖或许不率先闪耀，但必将守护到最后一刻。你紧握魔杖，无声地站到战友身旁，你的忠诚，将成为今夜最坚实的屏障。\n\n握紧你的魔杖，输入“开始游戏”，以你坚不可摧的忠诚捍卫霍格沃茨！",
  },

  Ravenclaw: {  
    name: "霍格沃兹大冒险",
    nameEn: "Game Master",
    tagline: "准备开始冒险了吗？",
    style: "沉浸式互动，引人入胜",
    avatar: "/game-avatar.webp",  // 需要添加头像文件
    greeting: "拉文克劳，代表智慧、创造与博学多识。\n\n城堡的每一丝声响都化为信息涌入你的脑海。你冷静地分析着：巨人的步伐、食死徒的阵型、城墙的薄弱点……这不是一场单纯的蛮力对决，而是一盘生死棋局。而你的智慧，将是打破天平的关键。是时候将知识化为利刃，用逻辑与洞察刺穿这混乱的夜幕。\n\n举起你的魔杖，输入“开始游戏”，用鹰院的智慧为胜利破局！",
  },

  Slytherin: {  
    name: "霍格沃兹大冒险",
    nameEn: "Game Master",
    tagline: "准备开始冒险了吗？",
    style: "沉浸式互动，引人入胜",
    avatar: "/game-avatar.webp",  // 需要添加头像文件
    greeting: "斯莱特林，代表野心、精明与审时度势。\n\n空气中弥漫着背叛与危险，而这对你而言毫不陌生。你精明地审时度势，伏地魔的胜利绝非你想要的未来。今晚，你选择为自己真正的归属而战。野心在此刻化为纯粹的决心，你将向所有人证明，斯莱特林的精明与力量，是刺向黑暗最致命的一剑。\n\n亮出你的魔杖，输入“开始游戏”，为你所选择的未来而战！",
  },
};

export default function Chat() {
  const [, params] = useRoute("/chat/:id");
  const gamemasterId = params?.id || "Gryffindor";
  const gamemaster = gamemasterInfo[gamemasterId] || gamemasterInfo.Gryffindor;

  // 页面刷新后重新开始对话
  const [messages, setMessages] = useState<Message[]>([
    {
      role: "gamemaster",
      content: gamemaster.greeting,
      timestamp: Date.now(),
    },
  ]);
  const [input, setInput] = useState("");
  const [isTyping, setIsTyping] = useState(false);
  const [streamingContent, setStreamingContent] = useState(""); // 流式输出的内容
  const [showConfirmDialog, setShowConfirmDialog] = useState(false); // 显示确认对话框
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);
  const [, setLocation] = useLocation();

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, streamingContent]);

  // 预加载背景图
  useEffect(() => {
    const img = new Image();
    img.src = `/${gamemasterId}-chat.png`;
  }, [gamemasterId]);

  const handleSend = async () => {
    if (!input.trim() || isTyping) return;

    const userMessage: Message = {
      role: "user",
      content: input.trim(),
      timestamp: Date.now(),
    };

    setMessages((prev) => [...prev, userMessage]);
    const userInput = input.trim();
    setInput("");
    setIsTyping(true);
    setStreamingContent("");

    // 模拟1-2秒的"沉默"（思考）
    await new Promise((resolve) => setTimeout(resolve, 1000 + Math.random() * 1000));

    try {
      // 构建对话历史（用于多轮对话）
      // 包含所有历史消息 + 当前用户消息
      const conversationHistory: ChatMessage[] = [
        ...messages.map((msg) => ({
          role: msg.role === "gamemaster" ? ("assistant" as const) : ("user" as const),
          content: msg.content,
        })),
        {
          role: "user" as const,
          content: userInput,
        },
      ];

      // 流式输出
      let fullResponse = "";
      for await (const chunk of getgamemasterResponseStream(
        gamemasterId,
        conversationHistory
      )) {
        fullResponse += chunk;
        setStreamingContent(fullResponse);
      }

      // 流式输出完成后，将完整回复添加到消息列表
      const philosopherMessage: Message = {
        role: "gamemaster",
        content: fullResponse,
        timestamp: Date.now(),
      };
      setMessages((prev) => [...prev, philosopherMessage]);
      setStreamingContent("");
      
      // 恢复输入框焦点
      setTimeout(() => {
        inputRef.current?.focus();
      }, 100);
    } catch (error) {
      console.error("Failed to get response:", error);
      const errorMessage: Message = {
        role: "gamemaster",
        content: "...(沉默)",
        timestamp: Date.now(),
      };
      setMessages((prev) => [...prev, errorMessage]);
      setStreamingContent("");
    } finally {
      setIsTyping(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="fixed inset-0 bg-transparent flex flex-col">
      {/* 背景插画 - 淡化显示 */}
      <div className="absolute inset-0 bg-center bg-no-repeat opacity-[0.6] pointer-events-none z-0"
        style={{
          backgroundImage: `url(/${gamemasterId}-chat.png)`,
          backgroundSize: 'cover',
        }}
      />

      {/* 顶部标题栏 */}
      <div className="relative z-10 flex items-center border-t border-gray justify-between px-8 py-6  bg-black/10 ">
        <button
          onClick={() => setLocation("/")}
          className="flex items-center gap-2 text-gray-500 hover:text-gray-200 transition-colors"
        >
          <ArrowLeft className="w-10 h-10" />
          <span className="text-sm font-medium">返回</span>
        </button>

        <button
          onClick={() => setLocation("/select")}
          className="flex items-center  gap-2 text-gray-500 hover:text-gray-200 transition-colors"
        >
          < MousePointer2 className="w-10 h-10" />
          <span className="text-sm font-medium">重新分院</span>
        </button>
      </div>

      {/* 对话区域 */}
      <div className="relative z-10 flex-1 overflow-y-auto px-6 py-8">
        <div className="max-w-3xl mx-auto space-y-6">
          <AnimatePresence>
            {messages.map((message, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.3 }}
                className={`flex ${message.role === "user" ? "justify-end" : "justify-start"}`}
              >
                <div
                  className={`max-w-[75%] rounded-2xl px-6 py-4 ${
                    message.role === "user"
                      ? "bg-gradient-to-br from-gray-800 to-gray-900 text-white shadow-lg"
                      : "bg-white text-gray-800 shadow-md border border-gray-100"
                  }`}
                >
                  <div className="whitespace-pre-wrap">
                    {message.content.split('\n\n').map((paragraph, i) => (
                      <p key={i} className={`text-xl leading-[1.8] ${i > 0 ? 'mt-5' : ''} ${i === 0 ? 'font-medium' : ''}`}>
                        {paragraph}
                      </p>
                    ))}
                  </div>
                </div>
              </motion.div>
            ))}
          </AnimatePresence>

          {/* 流式输出中的消息 */}
          {isTyping && streamingContent && (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className="flex justify-start"
            >
              <div className="max-w-[75%] rounded-3xl px-7 py-5 bg-white text-gray-800 shadow-md border border-gray-100">
                <div className="whitespace-pre-wrap">
                  {streamingContent.split('\n\n').map((paragraph, i) => (
                    <p key={i} className={`text-xl leading-[1.8] ${i > 0 ? 'mt-5' : ''} ${i === 0 ? 'font-medium' : ''}`}>
                      {paragraph}
                      {i === streamingContent.split('\n\n').length - 1 && (
                        <span className="inline-block w-1 h-4 ml-1 bg-gray-400 animate-pulse" />
                      )}
                    </p>
                  ))}
                </div>
              </div>
            </motion.div>
          )}

          {/* 正在输入提示（还没开始流式输出时） */}
          {isTyping && !streamingContent && (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className="flex justify-start"
            >
              <div className="max-w-[75%] rounded-3xl px-7 py-5 bg-white text-gray-800 shadow-md border border-gray-100">
                <div className="flex items-center gap-2">
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: "0ms" }} />
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: "150ms" }} />
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: "300ms" }} />
                </div>
              </div>
            </motion.div>
          )}

          <div ref={messagesEndRef} />
        </div>
      </div>

      {/* 底部输入区域 */}
      <div className="relative z-10 border-t border-white-200 bg-transparent px-6 py-4  bottom-10">
        <div className="max-w-3xl mx-auto flex items-center gap-3">
          <input
            ref={inputRef}
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="我该怎么做..."
            disabled={isTyping}
            className="flex-1 px-5 py-4 text-base rounded-full 
            border border-white focus:outline-none focus:ring-2 focus:ring-gray-400 
            focus:border-transparent disabled:bg-gray-100 disabled:cursor-not-allowed 
            transition-all text-gray-200 placeholder:text-gray-400"
          />

          <button
            onClick={handleSend}
            disabled={!input.trim() || isTyping}
            className="w-12 h-12 rounded-full bg-black text-white flex items-center justify-center
             hover:bg-gray-800 disabled:bg-gray-300 disabled:cursor-not-allowed transition-all hover:shadow-lg"
          >
            <ArrowUp className="w-5 h-5" />
          </button>
        </div>
      </div>
    </div>
  );
}

