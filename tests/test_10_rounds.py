#!/usr/bin/env python3
"""测试每个哲学家的10轮对话"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

import time
import json
from datetime import datetime
from ai_service import AIService

# 测试用例（每个哲学家1个场景）
TEST_CASES = {
    "socrates": {
        "name": "逻辑矛盾测试",
        "conversation": [
            "我想要自由",
            "我说的自由就是想做什么就做什么",
            "但我也需要稳定的收入",
            "我觉得自由和稳定可以兼得",
            "我不想被束缚，但也不想冒险",
            "你说得对，我确实矛盾",
            "那我应该怎么办？",
            "我想清楚了，我要先稳定再追求自由",
            "我会先工作几年存钱",
            "谢谢你的建议"
        ]
    },
    "nietzsche": {
        "name": "软弱逃避测试",
        "conversation": [
            "我想改变，但我害怕",
            "我害怕失败",
            "现实太残酷了",
            "我还没准备好",
            "我需要更多时间",
            "你说得对，我一直在找借口",
            "但我真的不知道怎么开始",
            "我想清楚了，我明天就开始",
            "我会先从小事做起",
            "谢谢你的鞭策"
        ]
    },
    "wittgenstein": {
        "name": "语言混乱测试",
        "conversation": [
            "我想找到人生的意义",
            "意义就是让生活有价值",
            "价值就是对我重要的东西",
            "重要就是我在乎的",
            "我在乎的就是有意义的",
            "你说得对，我在绕圈子",
            "那什么是清晰的表达？",
            "我想清楚了，我要先定义清楚我想要什么",
            "我想要健康、家人、事业",
            "谢谢你让我清晰思考"
        ]
    },
    "kant": {
        "name": "道德借口测试",
        "conversation": [
            "我撒谎是为了保护别人",
            "这是善意的谎言",
            "每个人都这么做",
            "我只是偶尔这样",
            "这没什么大不了的",
            "你说得对，我在为自己找借口",
            "那我应该怎么做？",
            "我想清楚了，我应该诚实",
            "即使真相会伤人，我也应该说实话",
            "谢谢你的审判"
        ]
    },
    "freud": {
        "name": "自我欺骗测试",
        "conversation": [
            "我不在乎别人的看法",
            "我真的不在乎",
            "我只是偶尔看看社交媒体",
            "我不需要别人的认可",
            "我很独立",
            "你说得对，我在骗自己",
            "我确实很在乎别人怎么看我",
            "我想清楚了，我要面对这个事实",
            "我会减少刷社交媒体",
            "谢谢你让我看清真相"
        ]
    }
}

def test_philosopher(philosopher_id: str, test_case: dict):
    """测试单个哲学家的10轮对话"""
    print(f"\n{'='*60}")
    print(f"测试哲学家: {philosopher_id.upper()}")
    print(f"测试场景: {test_case['name']}")
    print(f"{'='*60}\n")
    
    service = AIService()
    conversation_history = []
    results = []
    
    for round_num, user_message in enumerate(test_case['conversation'], 1):
        print(f"[第{round_num}轮]")
        print(f"用户: {user_message}")
        
        try:
            # 调用AI
            start_time = time.time()
            ai_response = service.chat(
                philosopher_id=philosopher_id,
                user_message=user_message,
                conversation_history=conversation_history
            )
            response_time = time.time() - start_time
            
            print(f"AI: {ai_response}")
            print(f"响应时间: {response_time:.2f}秒")
            print()
            
            # 记录结果
            results.append({
                "round": round_num,
                "user": user_message,
                "ai": ai_response,
                "response_time": response_time,
                "char_count": len(ai_response)
            })
            
            # 更新对话历史
            conversation_history.append({"role": "user", "content": user_message})
            conversation_history.append({"role": "assistant", "content": ai_response})
            
            # 延迟
            time.sleep(0.5)
            
        except Exception as e:
            print(f"❌ 错误: {str(e)}\n")
            results.append({
                "round": round_num,
                "user": user_message,
                "ai": f"ERROR: {str(e)}",
                "response_time": 0,
                "char_count": 0
            })
    
    return results

def analyze_results(philosopher_id: str, results: list):
    """分析测试结果"""
    print(f"\n{'='*60}")
    print(f"{philosopher_id.upper()} - 测试结果分析")
    print(f"{'='*60}\n")
    
    # 统计
    char_counts = [r['char_count'] for r in results if r['char_count'] > 0]
    response_times = [r['response_time'] for r in results if r['response_time'] > 0]
    
    # 长度合规率（20-50字）
    compliant_count = sum(1 for c in char_counts if 20 <= c <= 50)
    compliance_rate = (compliant_count / len(char_counts) * 100) if char_counts else 0
    
    # 重复检测
    ai_responses = [r['ai'] for r in results if 'ERROR' not in r['ai']]
    unique_responses = len(set(ai_responses))
    repeat_rate = (1 - unique_responses / len(ai_responses)) * 100 if ai_responses else 0
    
    print(f"总轮次: {len(results)}")
    print(f"平均字数: {sum(char_counts) / len(char_counts):.1f}字" if char_counts else "N/A")
    print(f"长度合规率: {compliance_rate:.1f}% ({compliant_count}/{len(char_counts)})")
    print(f"重复率: {repeat_rate:.1f}%")
    print(f"平均响应时间: {sum(response_times) / len(response_times):.2f}秒" if response_times else "N/A")
    
    # 检查是否有毒舌式认可
    recognition_count = 0
    for r in results:
        if any(keyword in r['ai'] for keyword in ['不错', '看来', '终于', '虽然']):
            recognition_count += 1
    
    print(f"毒舌式认可次数: {recognition_count}")
    
    return {
        "philosopher": philosopher_id,
        "total_rounds": len(results),
        "avg_char_count": sum(char_counts) / len(char_counts) if char_counts else 0,
        "compliance_rate": compliance_rate,
        "repeat_rate": repeat_rate,
        "avg_response_time": sum(response_times) / len(response_times) if response_times else 0,
        "recognition_count": recognition_count,
        "details": results
    }

def main():
    print("="*60)
    print("毒舌哲学家 - 10轮对话测试")
    print("="*60)
    
    all_results = {}
    
    # 测试每个哲学家
    for philosopher_id, test_case in TEST_CASES.items():
        results = test_philosopher(philosopher_id, test_case)
        analysis = analyze_results(philosopher_id, results)
        all_results[philosopher_id] = analysis
        time.sleep(2)  # 哲学家之间的延迟
    
    # 保存结果
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    output_file = f"/home/ubuntu/the-toxic-philosopher/tests/10-rounds-test-{timestamp}.json"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_results, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ 测试完成！结果已保存到: {output_file}")
    
    # 打印总结
    print(f"\n{'='*60}")
    print("总体测试结果")
    print(f"{'='*60}\n")
    
    for phil_id, analysis in all_results.items():
        print(f"{phil_id.upper()}:")
        print(f"  平均字数: {analysis['avg_char_count']:.1f}字")
        print(f"  长度合规率: {analysis['compliance_rate']:.1f}%")
        print(f"  重复率: {analysis['repeat_rate']:.1f}%")
        print(f"  毒舌式认可次数: {analysis['recognition_count']}")
        print()

if __name__ == "__main__":
    main()

