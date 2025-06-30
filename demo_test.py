#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
尼康官网性能测试演示脚本
快速演示测试功能
"""

from nikon_performance_test import NikonPerformanceTest

def main():
    """演示测试脚本"""
    print("🎬 尼康官网性能测试演示")
    print("=" * 50)
    
    # 创建测试实例
    tester = NikonPerformanceTest()
    
    print("\n✅ 测试环境配置:")
    print(f"📱 测试网站: {tester.base_url}")
    print(f"🔑 测试账号: {tester.test_user['phone']}")
    print(f"💬 随机评论内容: {tester.random_comments}")
    
    print("\n📊 性能评估标准:")
    print("┌─────────────┬─────────────┬─────────────┐")
    print("│    等级     │  响应时间   │ Lighthouse  │")
    print("├─────────────┼─────────────┼─────────────┤")
    print("│    优秀     │   ≤ 200ms   │    ≥ 90     │")
    print("│    良好     │   ≤ 500ms   │   50-89     │")
    print("│   可接受    │  ≤ 1000ms   │     -       │")
    print("│     差      │  > 1000ms   │   < 50      │")
    print("└─────────────┴─────────────┴─────────────┘")
    
    print("\n🚀 开始完整测试流程...")
    
    try:
        # 运行完整测试
        tester.run_full_test()
        
        print("\n🎉 测试执行完成！")
        print("📄 查看生成的HTML报告了解详细结果")
        
    except KeyboardInterrupt:
        print("\n⚠️  测试已被用户中断")
    except Exception as e:
        print(f"\n❌ 测试执行失败: {str(e)}")
        print("💡 建议检查网络连接和依赖环境")

if __name__ == "__main__":
    main()
