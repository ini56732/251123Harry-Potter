import { useState } from "react";

interface ShareButtonProps {
  message: string;
  philosopher: string;
}

export default function ShareButton({ message, philosopher }: ShareButtonProps) {
  const [copied, setCopied] = useState(false);

  const handleShare = async () => {
    const shareText = `${philosopher}对我说:"${message}" - 来自"毒舌哲学家"`;

    // 尝试使用Web Share API
    if (navigator.share) {
      try {
        await navigator.share({
          text: shareText,
        });
        return;
      } catch (err) {
        // 用户取消分享或不支持,继续使用复制功能
      }
    }

    // 降级到复制到剪贴板
    try {
      await navigator.clipboard.writeText(shareText);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch (err) {
      console.error("Failed to copy:", err);
    }
  };

  return (
    <button
      onClick={handleShare}
      className="text-xs opacity-60 hover:opacity-100 transition-opacity mt-2"
      title="分享这句话"
    >
      {copied ? "✓ 已复制" : "分享"}
    </button>
  );
}

