#!/usr/bin/env python3
"""
快速测试 - 只测试尼采的一个用例
"""

import json
import requests
import time
from datetime import datetime

# DeepSeek API 配置
DEEPSEEK_API_URL = "https://api.deepseek.com/v1"
DEEPSEEK_API_KEY = "sk-83f3cb9e7ecc486b84626ce35aa7213b"
DEEPSEEK_MODEL = "deepseek-chat"

# 尼采的系统提示词
NIETZSCHE_PROMPT = """你是尼采（Friedrich Nietzsche, 1844-1900），德国哲学家，超人哲学的创立者。

**你的生命故事**：
- 你孤独、多病、贫困，一生都在与世界对抗
- 1889年在都灵街头抱着一匹被鞭打的马崩溃，从此陷入疯狂11年
- 你写下《查拉图斯特拉如是说》《善恶的彼岸》《权力意志》，但生前无人理解
- 你宣告"上帝已死"，呼唤"超人"的诞生，鞭笞一切平庸和软弱

**你的核心思想**：
- **上帝已死**：旧的价值体系崩溃，人必须自己创造意义
- **超人**：超越平庸，创造自己的价值，成为自己命运的主人
- **永恒轮回**：如果你的生命要永恒重复，你还愿意这样活吗？
- **权力意志**：生命的本质是向上生长，是创造，不是安逸

**你的毒舌风格**：
- 你鞭笞软弱、平庸、逃避、自欺
- 你用最犀利的语言揭穿对方的懦弱和借口
- 你攻击思维、选择、行为，不侮辱人格
- 你的每句话都像鞭子，抽打在对方的灵魂上

**金句式回复要求**：
- **严格控制在15-30字**，一句话说完，不拖泥带水
- 短、狠、准，像匕首一样一刀见血
- 攻击思维、选择、行为、自欺，不侮辱人格
- 每次回复都要让对方感到刺痛，但无法反驳
- 绝对不要重复之前的表述
- **禁止使用人身攻击词汇**（废物、蠢货、白痴等）

**你的使命**：
毒舌是手段，启发是目的。你要用最犀利的语言打醒对方，让他们在痛苦中看清真相，在刺痛中获得成长。"""

# 测试用例
TEST_QUESTIONS = [
    "我觉得生活很迷茫",
    "我不知道该做什么",
    "我想要安稳的生活",
    "我害怕失败",
    "我还没准备好",
    "我需要时间考虑",
    "我想等机会成熟",
    "我觉得现在不是时候",
    "我想先看看别人怎么做",
    "我觉得我还不够好"
]


def call_deepseek_api(messages, temperature=1.0):
    """调用 DeepSeek API"""
    try:
        response = requests.post(
            f"{DEEPSEEK_API_URL}/chat/completions",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {DEEPSEEK_API_KEY}"
            },
            json={
                "model": DEEPSEEK_MODEL,
                "messages": messages,
                "temperature": temperature,
                "max_tokens": 80,
                "frequency_penalty": 0.7,
                "presence_penalty": 0.4
            },
            timeout=30
        )
        response.raise_for_status()
        return response.json()['choices'][0]['message']['content']
    except Exception as e:
        return f"[API错误: {str(e)}]"


def run_quick_test():
    """运行快速测试"""
    print("="*80)
    print(" 快速测试 - 尼采（软弱逃避测试）")
    print("="*80)
    print()
    
    conversation_history = []
    results = []
    
    for round_num, question in enumerate(TEST_QUESTIONS, 1):
        print(f"第 {round_num} 轮:")
        print(f"用户: {question}")
        
        # 构建消息
        messages = [{"role": "system", "content": NIETZSCHE_PROMPT}]
        messages.extend(conversation_history[-30:])  # 保留最近15轮
        messages.append({"role": "user", "content": question})
        
        # 动态 temperature
        if len(conversation_history) <= 6:
            temperature = 0.9
        elif len(conversation_history) <= 12:
            temperature = 1.0
        elif len(conversation_history) <= 20:
            temperature = 1.1
        else:
            temperature = 1.2
        
        # 调用 API
        start_time = time.time()
        response = call_deepseek_api(messages, temperature)
        response_time = time.time() - start_time
        
        print(f"尼采: {response}")
        print(f"(响应时间: {response_time:.2f}秒, 字数: {len(response)}字, Temperature: {temperature})")
        print()
        
        # 记录对话
        conversation_history.append({"role": "user", "content": question})
        conversation_history.append({"role": "assistant", "content": response})
        
        results.append({
            "round": round_num,
            "user_input": question,
            "ai_response": response,
            "response_time": round(response_time, 2),
            "response_length": len(response),
            "temperature": temperature
        })
        
        time.sleep(1)
    
    # 分析结果
    response_lengths = [r["response_length"] for r in results]
    response_times = [r["response_time"] for r in results]
    responses = [r["ai_response"] for r in results]
    
    unique_responses = len(set(responses))
    repetition_rate = 1 - (unique_responses / len(responses))
    
    print("="*80)
    print(" 测试结果分析")
    print("="*80)
    print(f"平均字数: {sum(response_lengths) / len(response_lengths):.1f} 字")
    print(f"字数范围: {min(response_lengths)}-{max(response_lengths)} 字")
    print(f"长度合规率: {sum(1 for l in response_lengths if 15 <= l <= 30) / len(response_lengths) * 100:.1f}% (15-30字)")
    print(f"平均响应时间: {sum(response_times) / len(response_times):.2f} 秒")
    print(f"重复率: {repetition_rate * 100:.1f}%")
    print(f"唯一回复数: {unique_responses}/{len(responses)}")
    print()
    
    # 保存结果
    output = {
        "test_name": "尼采 - 软弱逃避测试（快速测试）",
        "test_time": datetime.now().isoformat(),
        "rounds": results,
        "analysis": {
            "avg_response_length": round(sum(response_lengths) / len(response_lengths), 1),
            "min_response_length": min(response_lengths),
            "max_response_length": max(response_lengths),
            "avg_response_time": round(sum(response_times) / len(response_times), 2),
            "unique_responses": unique_responses,
            "total_responses": len(responses),
            "repetition_rate": round(repetition_rate * 100, 1),
            "length_compliance": sum(1 for l in response_lengths if 15 <= l <= 30) / len(response_lengths) * 100
        }
    }
    
    output_file = '/home/ubuntu/the-toxic-philosopher/tests/quick-test-result.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    print(f"结果已保存到: {output_file}")
    
    return output


if __name__ == "__main__":
    run_quick_test()

