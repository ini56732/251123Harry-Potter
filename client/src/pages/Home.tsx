import { useState, useEffect } from "react";
import { useLocation } from "wouter";
import "./Home.css"; 


export default function Home() {
  const [isExploding, setIsExploding] = useState(false);
  const [, setLocation] = useLocation();
  const [isLoaded, setIsLoaded] = useState(false);
  const [containerHeight, setContainerHeight] = useState('100vh');
  const [isHovered, setIsHovered] = useState(false); // 鼠标悬浮换图

  useEffect(() => {
    // 页面加载动画
    setTimeout(() => setIsLoaded(true), 100);
    
    // 检测浏览器对zoom的支持：Chrome/Edge需要166.67vh，Safari使用100vh
    const isChrome = /Chrome/.test(navigator.userAgent) && /Google Inc/.test(navigator.vendor);
    const isEdge = /Edg/.test(navigator.userAgent);
    if (isChrome || isEdge) {
      setContainerHeight('166.67vh');
    }
  }, []);

  const handleLogoClick = () => {
    setIsExploding(true);
    setTimeout(() => {
      setLocation("/background");
    }, 500);
  };


  return (
    <div className={`bg-black flex flex-col relative overflow-hidden 
      transition-opacity duration-1000 
    ${isLoaded ? 'opacity-100' : 'opacity-0'}`} style={{ height: containerHeight }}>

      {/* 背景 */}
      <div className="absolute inset-0 pointer-events-none">      
        <div className="absolute inset-0 ">
          <img 
            src="/home-bg.png" 
            alt="背景图片"
            className="w-full h-full object-cover" 
           />
        </div>
      </div>     

      {/* 内容 */}
      <div
        id="home"
        className={`flex-1 flex flex-col items-center justify-center px-6
           md:px-8 py-12 pt-24 md:pt-32 transition-opacity duration-500 relative z-10 ${
          isExploding ?  "hidden" : ""     //直接隐藏
        }`}
      >
        {/* 标题 */}
        <div className="text-center -mt-100 mb-12 md:mb-16 lg:mb-20 max-w-6xl animate-fade-in-up">
            <img 
                src="/app.logo.png" 
                alt="App Logo"
                className="mx-auto"
                style={{ 
                maxWidth: '80%',
                height: 'auto' 
                }}
            />
        </div>
      
      
      {/*文字 */}
        <div className="mt-10 mb-12 md:mb-16 bottom-10 lg:mb-20 max-w-6xl animate-fade-in-up">
            <img 
                src="/home-text.png" 
                alt="home-text"
                className="mx-auto"
                style={{ 
                maxWidth: '100%',
                height: 'auto' 
                }}
            />
        </div>

       
        {/* 魔杖按钮*/}
        <div
           className="fixed bottom-0 left-1/2 transform -translate-x-1/2 
                 flex flex-col items-center animate-fade-in-up"
           style={{ animationDelay: "0.6s" }}
    >
             {/* 按钮容器：完全贴合 PNG 的容器 */}
             <div
            className={`
              cursor-pointer
              transition-transform duration-300 
              ${isHovered ? "scale-85" : "scale-80"}
            `}
            onMouseEnter={() => setIsHovered(true)}
            onMouseLeave={() => setIsHovered(false)}
            onClick={handleLogoClick} // ← 点击逻辑
             >
            {/* 魔杖 PNG 按钮，悬停切换图片 */}
            <img
              src={isHovered ? "/home-start2.png" : "/home-start1.png"}
             alt="开始冒险"
             className="select-none pointer-events-none"
             draggable={false}
             />
             </div>
         </div>
      </div>

      {/* 页脚 */}
        <div 
          className="fixed bottom-0 left-1/2 transform -translate-x-1/2  w-screen animate-fade-in-up"
          style={{ margin: 0, padding: 0 }}
          >
          <img 
           src="/home-from.png" 
           alt="home-from"
           className="mx-auto"
            style={{
              width: '100vw',    
              height: 'auto',
              display: 'block',
              transform: 'scale(1.5)',          // ← 放大 2 倍
              transformOrigin: 'bottom center' // ← 从底部中心放大，不偏移
            }}
              />
        </div>
    </div>   
  );
}

