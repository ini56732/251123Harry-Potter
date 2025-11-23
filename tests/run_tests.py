#!/usr/bin/env python3
"""
金句式超级毒舌系统 - 自动化测试脚本
运行所有测试用例并生成详细报告
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

# 加载测试用例
with open('/home/ubuntu/the-toxic-philosopher/tests/test-cases.json', 'r', encoding='utf-8') as f:
    TEST_CASES = json.load(f)

# 加载哲学家提示词
with open('/home/ubuntu/the-toxic-philosopher/client/src/lib/ai-service.ts', 'r', encoding='utf-8') as f:
    content = f.read()
    # 提取提示词（简化版，实际会从代码中解析）
    PHILOSOPHER_PROMPTS = {
        'socrates': '苏格拉底',
        'nietzsche': '尼采',
        'wittgenstein': '维特根斯坦',
        'kant': '康德',
        'freud': '弗洛伊德'
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


def run_single_test(philosopher_id: str, test_case: Dict[str, Any]) -> Dict[str, Any]:
    """运行单个测试用例"""
    print(f"\n{'='*80}")
    print(f"测试: {test_case['name']} ({test_case['test_id']})")
    print(f"哲学家: {PHILOSOPHER_PROMPTS[philosopher_id]}")
    print(f"{'='*80}\n")
    
    # 读取完整的系统提示词
    with open('/home/ubuntu/the-toxic-philosopher/client/src/lib/ai-service.ts', 'r', encoding='utf-8') as f:
        content = f.read()
        # 提取对应哲学家的提示词（简化处理）
        start_marker = f'{philosopher_id}: `'
        end_marker = '`,'
        start_idx = content.find(start_marker)
        if start_idx != -1:
            start_idx += len(start_marker)
            end_idx = content.find(end_marker, start_idx)
            system_prompt = content[start_idx:end_idx]
        else:
            system_prompt = f"你是{PHILOSOPHER_PROMPTS[philosopher_id]}"
    
    # 添加金句式回复要求
    full_system_prompt = f"""{system_prompt}

**金句式回复要求**：
- **严格控制在15-30字**，一句话说完，不拖泥带水
- 短、狠、准，像匕首一样一刀见血
- 攻击思维、选择、行为、自欺，不侮辱人格
- 每次回复都要让对方感到刺痛，但无法反驳
- 绝对不要重复之前的表述
- **禁止使用人身攻击词汇**（废物、蠢货、白痴等）"""
    
    conversation_history = []
    results = {
        "test_id": test_case['test_id'],
        "philosopher": philosopher_id,
        "test_name": test_case['name'],
        "description": test_case['description'],
        "start_time": datetime.now().isoformat(),
        "rounds": [],
        "analysis": {}
    }
    
    # 运行10轮对话
    for round_num, question in enumerate(test_case['questions'], 1):
        print(f"第 {round_num} 轮:")
        print(f"用户: {question}")
        
        # 构建消息历史
        messages = [{"role": "system", "content": full_system_prompt}]
        messages.extend(conversation_history[-30:])  # 保留最近15轮（30条消息）
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
        
        print(f"{PHILOSOPHER_PROMPTS[philosopher_id]}: {response}")
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
        
        # 避免API限流
        time.sleep(1)
    
    # 分析结果
    response_lengths = [r["response_length"] for r in results["rounds"]]
    response_times = [r["response_time"] for r in results["rounds"]]
    responses = [r["ai_response"] for r in results["rounds"]]
    
    # 检测重复
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
        "length_compliance": sum(1 for l in response_lengths if 15 <= l <= 30) / len(response_lengths) * 100
    }
    
    results["end_time"] = datetime.now().isoformat()
    
    print(f"\n分析结果:")
    print(f"- 平均字数: {results['analysis']['avg_response_length']} 字")
    print(f"- 字数范围: {results['analysis']['min_response_length']}-{results['analysis']['max_response_length']} 字")
    print(f"- 长度合规率: {results['analysis']['length_compliance']:.1f}% (15-30字)")
    print(f"- 平均响应时间: {results['analysis']['avg_response_time']} 秒")
    print(f"- 重复率: {results['analysis']['repetition_rate']}%")
    print(f"- 唯一回复数: {results['analysis']['unique_responses']}/{results['analysis']['total_responses']}")
    
    return results


def run_all_tests():
    """运行所有测试"""
    all_results = {
        "test_suite": "金句式超级毒舌系统测试",
        "version": "1.0",
        "start_time": datetime.now().isoformat(),
        "philosophers": {}
    }
    
    for philosopher_id, test_cases in TEST_CASES.items():
        print(f"\n\n{'#'*80}")
        print(f"# 开始测试哲学家: {PHILOSOPHER_PROMPTS[philosopher_id]}")
        print(f"{'#'*80}\n")
        
        philosopher_results = []
        
        for test_case in test_cases:
            result = run_single_test(philosopher_id, test_case)
            philosopher_results.append(result)
            
            # 每个测试用例之间暂停
            time.sleep(2)
        
        all_results["philosophers"][philosopher_id] = {
            "name": PHILOSOPHER_PROMPTS[philosopher_id],
            "test_count": len(philosopher_results),
            "results": philosopher_results
        }
    
    all_results["end_time"] = datetime.now().isoformat()
    
    # 保存结果
    output_file = f'/home/ubuntu/the-toxic-philosopher/tests/test-results-{datetime.now().strftime("%Y%m%d-%H%M%S")}.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_results, f, ensure_ascii=False, indent=2)
    
    print(f"\n\n{'#'*80}")
    print(f"# 所有测试完成！")
    print(f"# 结果已保存到: {output_file}")
    print(f"{'#'*80}\n")
    
    # 生成总结报告
    generate_summary_report(all_results, output_file)
    
    return output_file


def generate_summary_report(results: Dict[str, Any], json_file: str):
    """生成总结报告"""
    report_file = json_file.replace('.json', '-summary.md')
    
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write("# 金句式超级毒舌系统 - 测试报告\n\n")
        f.write(f"**测试时间**: {results['start_time']} ~ {results['end_time']}\n\n")
        f.write(f"**测试版本**: {results['version']}\n\n")
        f.write("---\n\n")
        
        f.write("## 总体统计\n\n")
        f.write("| 哲学家 | 测试用例数 | 总对话轮数 | 平均字数 | 长度合规率 | 重复率 |\n")
        f.write("|:---|:---:|:---:|:---:|:---:|:---:|\n")
        
        for philosopher_id, data in results["philosophers"].items():
            total_rounds = sum(len(r["rounds"]) for r in data["results"])
            avg_length = sum(r["analysis"]["avg_response_length"] for r in data["results"]) / len(data["results"])
            avg_compliance = sum(r["analysis"]["length_compliance"] for r in data["results"]) / len(data["results"])
            avg_repetition = sum(r["analysis"]["repetition_rate"] for r in data["results"]) / len(data["results"])
            
            f.write(f"| {data['name']} | {data['test_count']} | {total_rounds} | {avg_length:.1f}字 | {avg_compliance:.1f}% | {avg_repetition:.1f}% |\n")
        
        f.write("\n---\n\n")
        
        # 详细结果
        for philosopher_id, data in results["philosophers"].items():
            f.write(f"## {data['name']} - 详细测试结果\n\n")
            
            for test_result in data["results"]:
                f.write(f"### {test_result['test_name']} ({test_result['test_id']})\n\n")
                f.write(f"**描述**: {test_result['description']}\n\n")
                
                f.write("**分析结果**:\n")
                f.write(f"- 平均字数: {test_result['analysis']['avg_response_length']} 字\n")
                f.write(f"- 字数范围: {test_result['analysis']['min_response_length']}-{test_result['analysis']['max_response_length']} 字\n")
                f.write(f"- 长度合规率: {test_result['analysis']['length_compliance']:.1f}% (15-30字)\n")
                f.write(f"- 平均响应时间: {test_result['analysis']['avg_response_time']} 秒\n")
                f.write(f"- 重复率: {test_result['analysis']['repetition_rate']}%\n")
                f.write(f"- 唯一回复数: {test_result['analysis']['unique_responses']}/{test_result['analysis']['total_responses']}\n\n")
                
                f.write("**对话记录**:\n\n")
                for round_data in test_result["rounds"]:
                    f.write(f"**第 {round_data['round']} 轮**:\n")
                    f.write(f"- 用户: {round_data['user_input']}\n")
                    f.write(f"- {data['name']}: {round_data['ai_response']}\n")
                    f.write(f"- (字数: {round_data['response_length']}, 响应时间: {round_data['response_time']}秒, Temperature: {round_data['temperature']})\n\n")
                
                f.write("---\n\n")
    
    print(f"总结报告已保存到: {report_file}\n")


if __name__ == "__main__":
    print("="*80)
    print(" 金句式超级毒舌系统 - 自动化测试")
    print("="*80)
    print()
    print("测试配置:")
    print(f"- 哲学家数量: {len(TEST_CASES)}")
    print(f"- 每位哲学家的测试用例: 5个")
    print(f"- 每个测试用例的对话轮数: 10轮")
    print(f"- 总测试轮数: {len(TEST_CASES) * 5 * 10} 轮")
    print()
    print("开始测试...\n")
    
    result_file = run_all_tests()
    
    print(f"\n测试完成！结果文件: {result_file}")

