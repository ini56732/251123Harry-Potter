import { useEffect, useState } from 'react';
import { useLocation } from 'wouter';
import { motion, AnimatePresence } from 'framer-motion';


// 内容


export default function Background() {
  const [, setLocation] = useLocation();
  const [isHovered, setIsHovered] = useState(false); // 按钮添加
  const [hoveredId, setHoveredId] = useState<string | null>(null);
  const [containerHeight, setContainerHeight] = useState('100vh');

  useEffect(() => {

    const isChrome = /Chrome/.test(navigator.userAgent) && /Google Inc/.test(navigator.vendor);
    const isEdge = /Edg/.test(navigator.userAgent);
    if (isChrome || isEdge) {
      setContainerHeight('166.67vh');
    }
  }, []);

  // 开始对话按钮
  const handleStartChat = () => {
    setLocation('/select');
  };

  return (
    <div className={`bg-black flex flex-col relative overflow-hidden 
      transition-opacity duration-1000 
    `} style={{ height: containerHeight }}>

      {/* 背景设计 */}
      <div className="absolute inset-0 pointer-events-none">      
        {/* 高清图片 */}
        <div className="absolute inset-0 opacity-[0.6]">
          <img 
            src="/background-bg.png" 
            alt="背景图片"
            className="w-full h-full object-cover" 
           />
        </div>
      </div>  


      {/* 主内容区域 */}
      <div className="min-h-screen flex flex-col items-center justify-center px-8 md:px-16 py-12 gap-12 relative z-10">

        {/* 标题 */}
        <div className="text-center mt-10 mb-12 md:mb-16 lg:mb-20 max-w-6xl animate-fade-in-up">
            <img 
                src="/logo-background.png" 
                alt="logo-background"
                className="mx-auto"
                style={{ 
                maxWidth: '80%',
                height: 'auto' 
                }}
            />
        </div>

        {/* 文字 */}
          <div className="text-center mt-40 mb-12 md:mb-16 lg:mb-20 max-w-6xl animate-fade-in-up">
             <img 
                src="/background-txt.png" 
                alt="background-txt"
                className="mx-auto"
                style={{ 
                maxWidth: '100%',
                height: 'auto' 
                  }}
              />
           </div>

        {/* 按钮*/}
        <div
           className="fixed bottom-20 left-1/2 transform -translate-x-1/2 
                 flex flex-col items-center animate-fade-in-up"
           style={{ animationDelay: "0.6s"    }}
    >
             {/* 按钮容器：完全贴合 PNG 的容器 */}
            <div
            className={`
              cursor-pointer
              transition-transform duration-300 
             ${isHovered ? "scale-55" : "scale-50"}
            `}
            onMouseEnter={() => setIsHovered(true)}
            onMouseLeave={() => setIsHovered(false)}
            onClick={handleStartChat} // ← 点击逻辑
             >
                <img
                src="/background-button.png"
                alt="开始冒险"
                className="select-none pointer-events-none"
                draggable={false}
                style={{
                filter: isHovered ? 
                'brightness(1.1) drop-shadow(0 0 30px currentColor)' : 
                'brightness(1) drop-shadow(0 0 10px rgba(255,255,255,0.3))'
                }}
                />
            </div>
         </div>
    </div>
</div>
  );
}

