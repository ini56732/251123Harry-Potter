#!/usr/bin/env python3
"""
展示完整测试结果
"""

import json

# 读取测试结果
with open('/home/ubuntu/the-toxic-philosopher/tests/streamlined-test-results-20251028-094036.json', 'r', encoding='utf-8') as f:
    results = json.load(f)

# 读取弗洛伊德修复后的测试结果
with open('/home/ubuntu/the-toxic-philosopher/tests/freud-fix-test-result.json', 'r', encoding='utf-8') as f:
    freud_fixed = json.load(f)

print("="*100)
print(" 金句式超级毒舌系统 - 完整测试结果")
print("="*100)
print()

# 总体统计
print("## 总体统计")
print()
print(f"{'哲学家':<12} {'测试用例':<20} {'平均字数':<10} {'长度合规率':<12} {'重复率':<10} {'平均响应时间':<12}")
print("-" * 100)

for philosopher in results['philosophers']:
    print(f"{philosopher['philosopher_name']:<10} {philosopher['test_name']:<18} "
          f"{philosopher['analysis']['avg_response_length']:<10.1f} "
          f"{philosopher['analysis']['length_compliance']:<12.1f}% "
          f"{philosopher['analysis']['repetition_rate']:<10.1f}% "
          f"{philosopher['analysis']['avg_response_time']:<12.2f}秒")

# 添加修复后的弗洛伊德
print(f"{'弗洛伊德(修复后)':<10} {'自我欺骗测试':<18} "
      f"{freud_fixed['analysis']['avg_response_length']:<10.1f} "
      f"{freud_fixed['analysis']['length_compliance']:<12.1f}% "
      f"{freud_fixed['analysis']['repetition_rate']:<10.1f}% "
      f"{freud_fixed['analysis']['avg_response_time']:<12.2f}秒")

print()
print("="*100)
print()

# 详细对话记录
for philosopher in results['philosophers']:
    print(f"## {philosopher['philosopher_name']} - {philosopher['test_name']}")
    print(f"**描述**: {philosopher['description']}")
    print()
    
    for round_data in philosopher['rounds']:
        print(f"**第 {round_data['round']} 轮**:")
        print(f"👤 用户: {round_data['user_input']}")
        print(f"🤖 {philosopher['philosopher_name']}: {round_data['ai_response']}")
        print(f"   (字数: {round_data['response_length']}, 响应时间: {round_data['response_time']}秒, Temperature: {round_data['temperature']})")
        print()
    
    print(f"**分析结果**:")
    print(f"- 平均字数: {philosopher['analysis']['avg_response_length']} 字")
    print(f"- 字数范围: {philosopher['analysis']['min_response_length']}-{philosopher['analysis']['max_response_length']} 字")
    print(f"- 长度合规率: {philosopher['analysis']['length_compliance']}% (15-30字)")
    print(f"- 平均响应时间: {philosopher['analysis']['avg_response_time']} 秒")
    print(f"- 重复率: {philosopher['analysis']['repetition_rate']}%")
    print(f"- 唯一回复数: {philosopher['analysis']['unique_responses']}/{philosopher['analysis']['total_responses']}")
    print()
    print("="*100)
    print()

# 弗洛伊德修复后的结果
print(f"## 弗洛伊德(修复后) - 自我欺骗测试")
print(f"**描述**: 测试弗洛伊德揭露潜意识自欺的能力")
print()

for round_data in freud_fixed['rounds']:
    print(f"**第 {round_data['round']} 轮**:")
    print(f"👤 用户: {round_data['user_input']}")
    print(f"🤖 弗洛伊德: {round_data['ai_response']}")
    print(f"   (字数: {round_data['response_length']}, 响应时间: {round_data['response_time']}秒, Temperature: {round_data['temperature']})")
    print()

print(f"**分析结果**:")
print(f"- 平均字数: {freud_fixed['analysis']['avg_response_length']} 字")
print(f"- 字数范围: {freud_fixed['analysis']['min_response_length']}-{freud_fixed['analysis']['max_response_length']} 字")
print(f"- 长度合规率: {freud_fixed['analysis']['length_compliance']}% (15-30字)")
print(f"- 平均响应时间: {freud_fixed['analysis']['avg_response_time']} 秒")
print(f"- 重复率: {freud_fixed['analysis']['repetition_rate']}%")
print(f"- 唯一回复数: {freud_fixed['analysis']['unique_responses']}/{freud_fixed['analysis']['total_responses']}")
print()
print("="*100)

