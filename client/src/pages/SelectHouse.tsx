import { useState, useEffect } from 'react';
import { useLocation } from 'wouter';
import './SelectHouse.css';

interface House {
    id: string;
    name: string;
    nameEn: string;
    image: string;
    clickimage: string;
  }
  
  const house: House[] = [
    {
      id: 'Gryffindor',
      name: '格兰芬多',
      nameEn: 'Gryffindor',
      image: '/Gryffindor1.png',
      clickimage: '/Gryffindor2.png',
    },
    {
      id: 'Hufflepuff',
      name: '赫奇帕奇',
      nameEn: 'Hufflepuff',
      image: '/Hufflepuff1.png',
      clickimage: '/Hufflepuff2.png',
    },
    {
      id: 'Ravenclaw',
      name: '拉文克劳',
      nameEn: 'Ravenclaw',
      image: '/Ravenclaw1.png',
      clickimage: '/Ravenclaw2.png',
    },
    {
      id: 'Slytherin',
      name: '斯莱特林',
      nameEn: 'Slytherin',
      image: '/Slytherin1.png',
      clickimage: '/Slytherin2.png',
    },
  ]

export default function SelectPhilosopher() {
    const [, setLocation] = useLocation();
    const [hoveredId, setHoveredId] = useState<string | null>(null);//悬浮设定
    const [imagesLoaded, setImagesLoaded] = useState(false);
    const [explodingId, setExplodingId] = useState<string | null>(null);
    const [isReturning, setIsReturning] = useState(false);
    const [containerHeight, setContainerHeight] = useState('100vh');


  // 检测是否从其他页面返回
  useEffect(() => {
    const hasVisited = sessionStorage.getItem('hasVisitedSelect');
    if (hasVisited) {
      setIsReturning(true);
    } else {
      sessionStorage.setItem('hasVisitedSelect', 'true');
    }
    
    // 检测浏览器对zoom的支持：Chrome/Edge需要166.67vh，Safari使用100vh
    const isChrome = /Chrome/.test(navigator.userAgent) && /Google Inc/.test(navigator.vendor);
    const isEdge = /Edg/.test(navigator.userAgent);
    if (isChrome || isEdge) {
      setContainerHeight('166.67vh');
    }
  }, []);

  // 预加载所有图片
  useEffect(() => {
    // 设置超时，确保即使图片加载失败也能显示
    const timeout = setTimeout(() => {
      console.log('Image preload timeout, showing images anyway');
      setImagesLoaded(true);
    }, 2000); // 2秒超时

    const imagePromises = house.map((phil) => {
      return new Promise((resolve, reject) => {
        const img = new Image();
        img.onload = resolve;
        img.onerror = reject;
        img.src = phil.image;
      });
    });

    Promise.all(imagePromises)
      .then(() => {
        clearTimeout(timeout);
        setImagesLoaded(true);
      })
      .catch((err) => {
        console.error('Failed to preload images:', err);
        clearTimeout(timeout);
        setImagesLoaded(true); // 即使失败也显示
      });

    return () => clearTimeout(timeout);
  }, []);

  const handleSelect = (id: string) => {
    setExplodingId(id);
    setTimeout(() => {
      setLocation(`/chat/${id}`);
    }, 1000);
  };

  return (
    <div className="text-white relative overflow-hidden flex flex-col" style={{
      height: containerHeight,
      backgroundColor: explodingId ? '#FAFAFA' : '#000000',
      transition: explodingId ? 'background-color 1.8s ease-in-out 0.5s' : 'none',
    }}>
    

      {/* 背景设计 */}
      <div className="absolute inset-0 pointer-events-none">      
        {/* 高清图片 */}
        <div className="absolute inset-0 opacity-[0.6]">
          <img 
            src="/select-bg.png" 
            alt="背景图片"
            className="w-full h-full object-cover" 
           />
        </div>
      </div>

      {/*文字 */}
      <div className="fixed top-50 left-1/2 transform -translate-x-1/2 
                 flex flex-col items-center animate-fade-in-up">
            <img 
                src="/select-text.png" 
                alt="select-text"
                className="mx-auto"
                style={{ 
                maxWidth: '100%',
                height: 'auto' 
                }}
            />
        </div>
           


      {/* 学院按钮 */}
      <div className={`relative w-full flex-1 top-30
       ${isReturning ? '' : 'animate-fadeInStep3'}`} 
       style={{
        opacity: explodingId ? 0 : 1,
        transition: explodingId ? 'opacity 1s ease-out 0.6s' : 'none',
        }}>

        {house.map((phil, index) => ( // 添加index参数用于计算位置
          <div
             key={phil.id}
             className="absolute cursor-pointer transition-all duration-500 z-20" // 移除left-1/2
             style={{
              top: '50%', // 固定垂直居中
              left: `${(index + 1) * (100 / (house.length + 1))}%`, // 横向等距分布计算
              width: '500px',
              height: '800px',
              transform: `translate(-50%, -50%) 
              scale(${hoveredId === phil.id ? 1.15 : hoveredId && hoveredId !== phil.id ? 0.85 : 1})`,
              opacity: hoveredId && hoveredId !== phil.id ? 0.3 : 1,
              filter: hoveredId && hoveredId !== phil.id ? 'blur(3px)' : 'none',
            }}
            onMouseEnter={() => setHoveredId(phil.id)}
            onMouseLeave={() => setHoveredId(null)}
            onClick={() => handleSelect(phil.id)}
          >
            
            {/* 图片 */}
            <img
              src={hoveredId === phil.id ? phil.clickimage : phil.image}      
              alt={phil.name}
              className="relative w-full h-full object-contain z-10"
              loading="eager"
              onError={(e) => {

              }}
              style={{
                opacity: explodingId === phil.id ? 0 : (imagesLoaded ? 1 : 0),
                transform: explodingId === phil.id ? 'scale(2)' : 'scale(1)',
                transition: explodingId === phil.id ? 
                'all 0.6s cubic-bezier(0.22, 1, 0.36, 1)' : 
                'filter 0.3s ease, opacity 0.5s ease',
              }}
            />

            {/* 信息卡片 */}
            {hoveredId === phil.id && (
              <div className="absolute left-full ml-12 top-1/2 transform -translate-y-1/2 bg-black/80 backdrop-blur-sm border border-white/20 rounded-lg p-6 w-64 animate-fadeIn">
                <h3 className="text-2xl font-bold mb-1">{phil.name}</h3>
                <p className="text-gray-400 text-sm mb-3">{phil.nameEn}</p>
                <p className="text-white/60 text-xs">点击进入对话 →</p>
              </div>
            )}

          </div>
        ))}
      </div>
    </div>
  );
}


