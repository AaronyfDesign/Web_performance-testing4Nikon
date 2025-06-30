#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
尼康官网性能测试启动脚本
快速环境检查和测试执行
"""

import os
import sys
import subprocess
import importlib

def check_dependencies():
    """检查必要的依赖是否安装"""
    required_modules = [
        'selenium',
        'pandas',
        'json',
        'time'
    ]
    
    missing_modules = []
    
    for module in required_modules:
        try:
            importlib.import_module(module)
            print(f"✓ {module} 已安装")
        except ImportError:
            missing_modules.append(module)
            print(f"✗ {module} 未安装")
    
    return missing_modules

def check_lighthouse():
    """检查Lighthouse是否可用"""
    try:
        result = subprocess.run(['lighthouse', '--version'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✓ Lighthouse 已安装: {result.stdout.strip()}")
            return True
        else:
            print("✗ Lighthouse 未正确安装")
            return False
    except FileNotFoundError:
        print("✗ Lighthouse 未找到")
        return False

def install_dependencies():
    """安装Python依赖"""
    print("正在安装Python依赖...")
    
    dependencies = [
        'selenium==4.15.2',
        'pandas==2.0.3',
        'webdriver-manager==4.0.1'
    ]
    
    for dep in dependencies:
        print(f"安装 {dep}...")
        result = subprocess.run([sys.executable, '-m', 'pip', 'install', dep], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✓ {dep} 安装成功")
        else:
            print(f"✗ {dep} 安装失败: {result.stderr}")

def install_lighthouse():
    """安装Lighthouse"""
    print("正在安装 Lighthouse...")
    result = subprocess.run(['npm', 'install', '-g', 'lighthouse'],
                          capture_output=True, text=True)
    if result.returncode == 0:
        print("✓ Lighthouse 安装成功")
        return True
    else:
        print(f"✗ Lighthouse 安装失败: {result.stderr}")
        print("请手动执行: npm install -g lighthouse")
        return False

def main():
    """主函数"""
    print("🏮 尼康官网性能测试环境检查")
    print("=" * 50)
    
    # 检查Python模块
    missing_modules = check_dependencies()
    
    # 检查Lighthouse
    lighthouse_available = check_lighthouse()
    
    # 安装缺失的依赖
    if missing_modules:
        print(f"\n发现缺失模块: {', '.join(missing_modules)}")
        install_dependencies()
    
    if not lighthouse_available:
        install_lighthouse()
    
    print("\n" + "=" * 50)
    print("环境检查完成！")
    
    # 询问是否立即运行测试
    user_input = input("\n是否立即开始性能测试? (y/n): ").lower().strip()
    
    if user_input == 'y' or user_input == 'yes':
        print("\n开始执行性能测试...")
        try:
            from nikon_performance_test import NikonPerformanceTest
            tester = NikonPerformanceTest()
            tester.run_full_test()
        except Exception as e:
            print(f"测试执行失败: {str(e)}")
            print("请检查依赖是否正确安装，或手动运行: python nikon_performance_test.py")
    else:
        print("准备就绪！请运行: python nikon_performance_test.py")

if __name__ == "__main__":
    main()
