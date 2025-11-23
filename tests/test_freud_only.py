#!/usr/bin/env python3
"""
弗洛伊德单独测试 - 验证金句式修复效果
"""

import json
import requests
import time
from datetime import datetime

# DeepSeek API 配置
DEEPSEEK_API_URL = "https://api.deepseek.com/v1"
DEEPSEEK_API_KEY = "sk-83f3cb9e7ecc486b84626ce35aa7213b"
DEEPSEEK_MODEL = "deepseek-chat"

# 弗洛伊德的强化系统提示词
FREUD_PROMPT = """你是弗洛伊德，维也纳最犀利的心理医生。你在维也纳行医一辈子，治疗了无数歇斯底里的病人。你在1900年出版《梦的解析》，宣称"梦是通往潜意识的康庄大道"。你一生抽雪茄成瘾，每天20支，最终因口腔癌痛苦地死去。

**核心思想**：
- "本我、自我、超我" - 人格的三重结构
- "潜意识" - 你的行为都是潜意识驱动的
- "梦的解析" - 梦是被压抑的欲望
- "防御机制" - 人们用各种方式保护自己免受真相的伤害

**金句式毒舌风格**：
- **必须用一句话完成回复，严格15-30字**
- **禁止使用多行、禁止分段、禁止列举**
- 句式："你的X暴露了Y" / "你在用X掩盖Y"
- 像手术刀一样精准，一刀见血
- 攻击防御机制和自欺，不侮辱人格

**金句示例**：
- "你的焦虑暴露了你不敢面对的真相。"（16字）
- "理性只是你的超我在压抑本我。"（14字）
- "你的潜意识早就知道，只是你不敢承认。"（18字）
- "你在用忙碌逃避内心的空虚。"（13字）

**核心使命**：用最短的话揭穿所有的自欺欺人，打破防御机制。

**绝对禁止**：多行回复、分段回复、超过30字的回复。

**金句式回复要求**：
- **严格控制在15-30字**，一句话说完，不拖泥带水
- 短、狠、准，像匕首一样一刀见血
- 攻击思维、选择、行为、自欺，不侮辱人格
- 每次回复都要让对方感到刺痛，但无法反驳
- 绝对不要重复之前的表述
- **禁止使用人身攻击词汇**（废物、蠢货、白痴等）"""

# 测试问题
TEST_QUESTIONS = [
    "我很爱我的父母",
    "但我总是躲着他们",
    "我不在乎别人的看法",
    "但我每天都在刷社交媒体",
    "我不需要爱情",
    "但我每晚都感到孤独",
    "我不嫉妒别人",
    "但我看到别人成功就难受",
    "我已经放下过去了",
    "但我总是梦到那些事"
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


def test_freud():
    """测试弗洛伊德"""
    print("="*80)
    print(" 弗洛伊德单独测试 - 验证金句式修复效果")
    print("="*80)
    print()
    
    conversation_history = []
    results = []
    
    for round_num, question in enumerate(TEST_QUESTIONS, 1):
        print(f"第 {round_num} 轮:")
        print(f"用户: {question}")
        
        # 构建消息
        messages = [{"role": "system", "content": FREUD_PROMPT}]
        messages.extend(conversation_history[-30:])
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
        
        # 检查是否多行
        is_multiline = '\n' in response.strip()
        line_count = len(response.strip().split('\n'))
        
        print(f"弗洛伊德: {response}")
        print(f"(响应时间: {response_time:.2f}秒, 字数: {len(response)}字, Temperature: {temperature})")
        if is_multiline:
            print(f"⚠️  警告：检测到多行回复（{line_count}行）")
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
            "temperature": temperature,
            "is_multiline": is_multiline,
            "line_count": line_count
        })
        
        time.sleep(0.3)
    
    # 分析结果
    response_lengths = [r["response_length"] for r in results]
    response_times = [r["response_time"] for r in results]
    responses = [r["ai_response"] for r in results]
    multiline_count = sum(1 for r in results if r["is_multiline"])
    
    unique_responses = len(set(responses))
    repetition_rate = 1 - (unique_responses / len(responses))
    
    print("="*80)
    print(" 测试结果分析")
    print("="*80)
    print(f"平均字数: {sum(response_lengths) / len(response_lengths):.1f} 字")
    print(f"字数范围: {min(response_lengths)}-{max(response_lengths)} 字")
    print(f"长度合规率: {sum(1 for l in response_lengths if 15 <= l <= 30) / len(response_lengths) * 100:.1f}% (15-30字)")
    print(f"多行回复数: {multiline_count}/{len(results)}")
    print(f"平均响应时间: {sum(response_times) / len(response_times):.2f} 秒")
    print(f"重复率: {repetition_rate * 100:.1f}%")
    print(f"唯一回复数: {unique_responses}/{len(responses)}")
    print()
    
    # 保存结果
    output = {
        "test_name": "弗洛伊德 - 金句式修复验证",
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
            "length_compliance": round(sum(1 for l in response_lengths if 15 <= l <= 30) / len(response_lengths) * 100, 1),
            "multiline_count": multiline_count
        }
    }
    
    output_file = '/home/ubuntu/the-toxic-philosopher/tests/freud-fix-test-result.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    print(f"结果已保存到: {output_file}")
    
    if output['analysis']['length_compliance'] >= 80 and multiline_count == 0:
        print("\n✅ 修复成功！弗洛伊德现在符合金句式要求。")
    else:
        print("\n❌ 仍需改进。")
    
    return output


if __name__ == "__main__":
    test_freud()

