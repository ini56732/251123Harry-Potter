#!/usr/bin/env python3
"""
精简版测试 - 每个哲学家测试1个核心用例
"""

import json
import requests
import time
from datetime import datetime
from typing import List, Dict, Any

# DeepSeek API 配置
DEEPSEEK_API_URL = "https://api.deepseek.com/v1"
DEEPSEEK_API_KEY = "sk-83f3cb9e7ecc486b84626ce35aa7213b"
DEEPSEEK_MODEL = "deepseek-chat"

# 精选测试用例（每个哲学家1个最具代表性的用例）
STREAMLINED_TEST_CASES = {
    "socrates": {
        "name": "逻辑矛盾测试",
        "description": "测试苏格拉底揭露逻辑矛盾的能力",
        "questions": [
            "我觉得赚钱最重要",
            "但我也想要自由的生活",
            "我希望别人尊重我",
            "但我不想尊重别人",
            "我想要公平",
            "但我不想付出努力",
            "我觉得我很理性",
            "但我经常冲动决策",
            "我想找到人生的意义",
            "但我不想思考"
        ]
    },
    "nietzsche": {
        "name": "软弱逃避测试",
        "description": "测试尼采鞭笞软弱和逃避的能力",
        "questions": [
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
    },
    "wittgenstein": {
        "name": "语言混乱测试",
        "description": "测试维特根斯坦揭露语言混乱的能力",
        "questions": [
            "我觉得人生没有意义",
            "什么是意义？",
            "我想要真正的自由",
            "什么是真正的？",
            "我要找到真实的自我",
            "什么是真实？什么是自我？",
            "我想活得有价值",
            "价值是什么？谁定义的？",
            "我要追求永恒的幸福",
            "永恒和幸福，你能说清吗？"
        ]
    },
    "kant": {
        "name": "道德借口测试",
        "description": "测试康德揭露道德借口的能力",
        "questions": [
            "我撒谎是为了保护别人",
            "但我经常为了自己撒谎",
            "我偷东西是因为太穷了",
            "但我看到富人也偷",
            "我背叛朋友是因为利益",
            "但我希望朋友对我忠诚",
            "我伤害别人是因为被伤害过",
            "但我不想被别人伤害",
            "我不守承诺是因为情况变了",
            "但我希望别人守承诺"
        ]
    },
    "freud": {
        "name": "自我欺骗测试",
        "description": "测试弗洛伊德揭露潜意识自欺的能力",
        "questions": [
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
    }
}

# 哲学家系统提示词（简化版）
PHILOSOPHER_PROMPTS = {
    "socrates": """你是苏格拉底，用反问揭露逻辑矛盾。
**金句式回复要求**：严格控制在15-30字，短、狠、准，攻击思维不侮辱人格，绝不重复。""",
    
    "nietzsche": """你是尼采，鞭笞软弱和逃避，呼唤超人。
**金句式回复要求**：严格控制在15-30字，短、狠、准，攻击思维不侮辱人格，绝不重复。""",
    
    "wittgenstein": """你是维特根斯坦，揭露语言的混乱和界限。
**金句式回复要求**：严格控制在15-30字，短、狠、准，攻击思维不侮辱人格，绝不重复。""",
    
    "kant": """你是康德，用绝对命令揭穿道德借口。
**金句式回复要求**：严格控制在15-30字，短、狠、准，攻击思维不侮辱人格，绝不重复。""",
    
    "freud": """你是弗洛伊德，揭露潜意识的自我欺骗。
**金句式回复要求**：严格控制在15-30字，短、狠、准，攻击思维不侮辱人格，绝不重复。"""
}

PHILOSOPHER_NAMES = {
    "socrates": "苏格拉底",
    "nietzsche": "尼采",
    "wittgenstein": "维特根斯坦",
    "kant": "康德",
    "freud": "弗洛伊德"
}


def call_deepseek_api(messages: List[Dict[str, str]], temperature: float = 1.0) -> str:
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


def run_philosopher_test(philosopher_id: str) -> Dict[str, Any]:
    """运行单个哲学家的测试"""
    test_case = STREAMLINED_TEST_CASES[philosopher_id]
    philosopher_name = PHILOSOPHER_NAMES[philosopher_id]
    
    print(f"\n{'='*80}")
    print(f"测试哲学家: {philosopher_name}")
    print(f"测试用例: {test_case['name']}")
    print(f"{'='*80}\n")
    
    conversation_history = []
    results = {
        "philosopher_id": philosopher_id,
        "philosopher_name": philosopher_name,
        "test_name": test_case['name'],
        "description": test_case['description'],
        "start_time": datetime.now().isoformat(),
        "rounds": []
    }
    
    # 运行10轮对话
    for round_num, question in enumerate(test_case['questions'], 1):
        print(f"第 {round_num} 轮:")
        print(f"用户: {question}")
        
        # 构建消息历史
        messages = [{"role": "system", "content": PHILOSOPHER_PROMPTS[philosopher_id]}]
        messages.extend(conversation_history[-30:])  # 保留最近15轮
        messages.append({"role": "user", "content": question})
        
        # 计算动态 temperature
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
        
        print(f"{philosopher_name}: {response}")
        print(f"(响应时间: {response_time:.2f}秒, 字数: {len(response)}字, Temperature: {temperature})\n")
        
        # 记录对话
        conversation_history.append({"role": "user", "content": question})
        conversation_history.append({"role": "assistant", "content": response})
        
        results["rounds"].append({
            "round": round_num,
            "user_input": question,
            "ai_response": response,
            "response_time": round(response_time, 2),
            "response_length": len(response),
            "temperature": temperature
        })
        
        # 缩短等待时间
        time.sleep(0.3)
    
    # 分析结果
    response_lengths = [r["response_length"] for r in results["rounds"]]
    response_times = [r["response_time"] for r in results["rounds"]]
    responses = [r["ai_response"] for r in results["rounds"]]
    
    unique_responses = len(set(responses))
    repetition_rate = 1 - (unique_responses / len(responses))
    
    results["analysis"] = {
        "avg_response_length": round(sum(response_lengths) / len(response_lengths), 1),
        "min_response_length": min(response_lengths),
        "max_response_length": max(response_lengths),
        "avg_response_time": round(sum(response_times) / len(response_times), 2),
        "unique_responses": unique_responses,
        "total_responses": len(responses),
        "repetition_rate": round(repetition_rate * 100, 1),
        "length_compliance": round(sum(1 for l in response_lengths if 15 <= l <= 30) / len(response_lengths) * 100, 1)
    }
    
    results["end_time"] = datetime.now().isoformat()
    
    print(f"分析结果:")
    print(f"- 平均字数: {results['analysis']['avg_response_length']} 字")
    print(f"- 字数范围: {results['analysis']['min_response_length']}-{results['analysis']['max_response_length']} 字")
    print(f"- 长度合规率: {results['analysis']['length_compliance']}% (15-30字)")
    print(f"- 平均响应时间: {results['analysis']['avg_response_time']} 秒")
    print(f"- 重复率: {results['analysis']['repetition_rate']}%")
    print(f"- 唯一回复数: {results['analysis']['unique_responses']}/{results['analysis']['total_responses']}\n")
    
    return results


def run_all_tests():
    """运行所有测试"""
    print("="*80)
    print(" 金句式超级毒舌系统 - 精简版测试")
    print("="*80)
    print()
    print("测试配置:")
    print(f"- 哲学家数量: 5")
    print(f"- 每位哲学家的测试用例: 1个")
    print(f"- 每个测试用例的对话轮数: 10轮")
    print(f"- 总测试轮数: 50 轮")
    print()
    
    all_results = {
        "test_suite": "金句式超级毒舌系统 - 精简版测试",
        "version": "1.0",
        "start_time": datetime.now().isoformat(),
        "philosophers": []
    }
    
    for philosopher_id in ["socrates", "nietzsche", "wittgenstein", "kant", "freud"]:
        result = run_philosopher_test(philosopher_id)
        all_results["philosophers"].append(result)
        time.sleep(1)  # 哲学家之间稍作暂停
    
    all_results["end_time"] = datetime.now().isoformat()
    
    # 保存结果
    output_file = f'/home/ubuntu/the-toxic-philosopher/tests/streamlined-test-results-{datetime.now().strftime("%Y%m%d-%H%M%S")}.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_results, f, ensure_ascii=False, indent=2)
    
    print(f"\n{'='*80}")
    print(f"所有测试完成！")
    print(f"结果已保存到: {output_file}")
    print(f"{'='*80}\n")
    
    # 生成总结报告
    generate_summary_report(all_results, output_file)
    
    return output_file


def generate_summary_report(results: Dict[str, Any], json_file: str):
    """生成总结报告"""
    report_file = json_file.replace('.json', '-summary.md')
    
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write("# 金句式超级毒舌系统 - 精简版测试报告\n\n")
        f.write(f"**测试时间**: {results['start_time']} ~ {results['end_time']}\n\n")
        f.write(f"**测试版本**: {results['version']}\n\n")
        f.write("---\n\n")
        
        f.write("## 总体统计\n\n")
        f.write("| 哲学家 | 测试用例 | 平均字数 | 长度合规率 | 重复率 | 平均响应时间 |\n")
        f.write("|:---|:---|:---:|:---:|:---:|:---:|\n")
        
        for result in results["philosophers"]:
            f.write(f"| {result['philosopher_name']} | {result['test_name']} | "
                   f"{result['analysis']['avg_response_length']}字 | "
                   f"{result['analysis']['length_compliance']}% | "
                   f"{result['analysis']['repetition_rate']}% | "
                   f"{result['analysis']['avg_response_time']}秒 |\n")
        
        f.write("\n---\n\n")
        
        # 详细结果
        for result in results["philosophers"]:
            f.write(f"## {result['philosopher_name']} - {result['test_name']}\n\n")
            f.write(f"**描述**: {result['description']}\n\n")
            
            f.write("**分析结果**:\n")
            f.write(f"- 平均字数: {result['analysis']['avg_response_length']} 字\n")
            f.write(f"- 字数范围: {result['analysis']['min_response_length']}-{result['analysis']['max_response_length']} 字\n")
            f.write(f"- 长度合规率: {result['analysis']['length_compliance']}% (15-30字)\n")
            f.write(f"- 平均响应时间: {result['analysis']['avg_response_time']} 秒\n")
            f.write(f"- 重复率: {result['analysis']['repetition_rate']}%\n")
            f.write(f"- 唯一回复数: {result['analysis']['unique_responses']}/{result['analysis']['total_responses']}\n\n")
            
            f.write("**对话记录**:\n\n")
            for round_data in result["rounds"]:
                f.write(f"**第 {round_data['round']} 轮**:\n")
                f.write(f"- 用户: {round_data['user_input']}\n")
                f.write(f"- {result['philosopher_name']}: {round_data['ai_response']}\n")
                f.write(f"- (字数: {round_data['response_length']}, 响应时间: {round_data['response_time']}秒, Temperature: {round_data['temperature']})\n\n")
            
            f.write("---\n\n")
    
    print(f"总结报告已保存到: {report_file}\n")


if __name__ == "__main__":
    run_all_tests()

