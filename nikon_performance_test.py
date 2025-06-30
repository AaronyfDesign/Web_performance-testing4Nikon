#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
尼康官网自动化性能测试脚本
使用 Lighthouse 和 Selenium 进行性能测试
"""

import json
import time
import random
import subprocess
import threading
from datetime import datetime
from typing import Dict, List, Tuple
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
import pandas as pd
from pathlib import Path

class NikonPerformanceTest:
    def __init__(self):
        """初始化测试环境"""
        self.base_url = "https://my.nikon.com.cn"
        self.test_user = {
            "phone": "18727560912",
            "password": "Nk123456"
        }
        
        # Lighthouse 性能阈值
        self.performance_thresholds = {
            "good": {"min": 90, "max": 100},
            "needs_improvement": {"min": 50, "max": 89},
            "poor": {"min": 0, "max": 49}
        }
        
        # 响应时间阈值（毫秒）
        self.response_time_thresholds = {
            "excellent": 200,
            "good": 500,
            "acceptable": 1000,
            "poor": 3000
        }
        
        self.test_results = []
        self.interaction_results = []
        self.random_comments = ["赞", "好看"]
        
    def setup_driver(self) -> webdriver.Chrome:
        """设置Chrome驱动"""
        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        
        driver = webdriver.Chrome(options=chrome_options)
        driver.implicitly_wait(10)
        return driver
    
    def run_lighthouse_audit(self, url: str) -> Dict:
        """运行Lighthouse性能审计"""
        try:
            # 构建lighthouse命令
            cmd = [
                "lighthouse",
                url,
                "--only-categories=performance",
                "--output=json",
                "--output-path=temp_lighthouse.json",
                "--chrome-flags=--headless --no-sandbox",
                "--quiet"
            ]
            
            # 执行命令并等待完成
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
            
            if result.returncode == 0:
                # 读取结果文件
                with open("temp_lighthouse.json", "r", encoding="utf-8") as f:
                    lighthouse_data = json.load(f)
                
                # 提取关键指标
                audits = lighthouse_data.get("audits", {})
                categories = lighthouse_data.get("categories", {})
                
                performance_metrics = {
                    "url": url,
                    "performance_score": categories.get("performance", {}).get("score", 0) * 100,
                    "fcp": audits.get("first-contentful-paint", {}).get("numericValue", 0),
                    "lcp": audits.get("largest-contentful-paint", {}).get("numericValue", 0),
                    "cls": audits.get("cumulative-layout-shift", {}).get("numericValue", 0),
                    "fid": audits.get("max-potential-fid", {}).get("numericValue", 0),
                    "speed_index": audits.get("speed-index", {}).get("numericValue", 0),
                    "total_blocking_time": audits.get("total-blocking-time", {}).get("numericValue", 0)
                }
                
                # 清理临时文件
                Path("temp_lighthouse.json").unlink(missing_ok=True)
                
                return performance_metrics
            else:
                print(f"Lighthouse执行失败: {result.stderr}")
                return None
                
        except Exception as e:
            print(f"Lighthouse审计失败: {str(e)}")
            return None
    
    def measure_response_time(self, driver: webdriver.Chrome, action_func) -> float:
        """测量响应时间"""
        start_time = time.time()
        try:
            action_func()
            WebDriverWait(driver, 10).until(
                lambda d: d.execute_script("return document.readyState") == "complete"
            )
        except Exception as e:
            print(f"操作执行失败: {str(e)}")
        end_time = time.time()
        return (end_time - start_time) * 1000  # 转换为毫秒
    
    def categorize_response_time(self, response_time: float) -> str:
        """根据响应时间分类性能等级"""
        if response_time <= self.response_time_thresholds["excellent"]:
            return "优秀"
        elif response_time <= self.response_time_thresholds["good"]:
            return "良好"
        elif response_time <= self.response_time_thresholds["acceptable"]:
            return "可接受"
        else:
            return "差"
    
    def login(self, driver: webdriver.Chrome) -> bool:
        """用户登录"""
        try:
            # 访问登录页面
            driver.get(f"{self.base_url}/account/login/phone")
            time.sleep(2)
            
            # 添加调试信息
            print(f"当前页面URL: {driver.current_url}")
            print(f"页面标题: {driver.title}")
            
            # 更安全的元素定位方式
            try:
                # 等待页面完全加载
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.TAG_NAME, "body"))
                )
                
                # 输入手机号 - 使用多种定位方式
                phone_selectors = [
                    "//input[@placeholder='请输入手机号']",
                    "//input[@type='tel']",
                    "//input[contains(@class, 'phone')]",
                    "//input[@name='phone']"
                ]
                
                phone_input = None
                for selector in phone_selectors:
                    try:
                        phone_input = WebDriverWait(driver, 5).until(
                            EC.presence_of_element_located((By.XPATH, selector))
                        )
                        print(f"找到手机号输入框: {selector}")
                        break
                    except:
                        continue
                
                if not phone_input:
                    print("未找到手机号输入框")
                    return False
                    
                phone_input.send_keys(self.test_user["phone"])
                
                # 输入密码 - 使用多种定位方式
                password_selectors = [
                    "//input[@type='password']",
                    "//input[@placeholder='请输入密码']",
                    "//input[contains(@class, 'password')]",
                    "//input[@name='password']"
                ]
                
                password_input = None
                for selector in password_selectors:
                    try:
                        password_input = driver.find_element(By.XPATH, selector)
                        print(f"找到密码输入框: {selector}")
                        break
                    except:
                        continue
                        
                if not password_input:
                    print("未找到密码输入框")
                    return False
                    
                password_input.send_keys(self.test_user["password"])
                
                # 点击登录按钮 - 使用多种定位方式
                login_selectors = [
                    "//button[contains(text(), '登录')]",
                    "//button[contains(text(), '登錄')]",
                    "//input[@type='submit']",
                    "//button[@type='submit']",
                    "//a[contains(text(), '登录')]"
                ]
                
                login_button = None
                for selector in login_selectors:
                    try:
                        login_button = driver.find_element(By.XPATH, selector)
                        print(f"找到登录按钮: {selector}")
                        break
                    except:
                        continue
                        
                if not login_button:
                    print("未找到登录按钮")
                    return False
                    
                login_button.click()
                
                # 等待登录完成 - 修改等待条件
                WebDriverWait(driver, 15).until(
                    lambda d: "/account/login" not in d.current_url
                )
                
                print("登录成功")
                return True
                
            except Exception as e:
                print(f"元素定位失败: {str(e)}")
                # 保存页面截图用于调试
                driver.save_screenshot(f"login_error_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
                return False
                
        except Exception as e:
            print(f"登录失败: {str(e)}")
            return False
    
    def test_page_performance(self, url: str, page_name: str):
        """测试页面性能"""
        print(f"\n正在测试 {page_name} 页面性能...")
        
        # 运行Lighthouse审计
        lighthouse_result = self.run_lighthouse_audit(url)
        
        if lighthouse_result:
            result = {
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "page_name": page_name,
                "url": url,
                **lighthouse_result
            }
            
            # 评估性能等级
            score = lighthouse_result["performance_score"]
            if score >= 90:
                performance_grade = "优秀"
            elif score >= 50:
                performance_grade = "中等"
            else:
                performance_grade = "差"
            
            result["performance_grade"] = performance_grade
            self.test_results.append(result)
            
            print(f"{page_name} 页面性能评分: {score:.1f} ({performance_grade})")
        else:
            print(f"{page_name} 页面性能测试失败")
    
    def test_basic_operations(self, driver: webdriver.Chrome):
        """测试基本操作响应时间"""
        operations = [
            {
                "name": "首页加载",
                "action": lambda: driver.get(self.base_url)
            },
            {
                "name": "照片页面跳转", 
                "action": lambda: driver.get(f"{self.base_url}/post/photo")
            },
            {
                "name": "学习讨论页面跳转",
                "action": lambda: driver.get(f"{self.base_url}/article")
            },
            {
                "name": "摄影圈页面跳转",
                "action": lambda: driver.get(f"{self.base_url}/circle")
            }
        ]
        
        print("\n正在测试基本操作响应时间...")
        
        for operation in operations:
            response_time = self.measure_response_time(driver, operation["action"])
            grade = self.categorize_response_time(response_time)
            
            interaction_result = {
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "operation": operation["name"],
                "response_time_ms": response_time,
                "grade": grade
            }
            
            self.interaction_results.append(interaction_result)
            print(f"{operation['name']}: {response_time:.0f}ms ({grade})")
            
            time.sleep(1)  # 避免请求过快
    
    def find_interactive_posts(self, driver: webdriver.Chrome) -> List[str]:
        """查找可以交互的帖子链接"""
        posts = []
        try:
            # 先尝试在照片页面找帖子
            driver.get(f"{self.base_url}/post/photo")
            time.sleep(3)
            
            # 查找图片帖子
            post_elements = driver.find_elements(By.XPATH, "//a[contains(@href, '/post/detail/')]")
            
            for element in post_elements[:5]:  # 限制数量
                href = element.get_attribute("href")
                if href and "/post/detail/" in href:
                    posts.append(href)
                    print(f"找到帖子: {href}")
            
            # 再尝试在学习讨论页面找帖子
            driver.get(f"{self.base_url}/article")
            time.sleep(3)
            
            article_elements = driver.find_elements(By.XPATH, "//a[contains(@href, '/post/detail/')]")
            
            for element in article_elements[:3]:  # 限制数量
                href = element.get_attribute("href")
                if href and "/post/detail/" in href and href not in posts:
                    posts.append(href)
                    print(f"找到文章: {href}")
                    
        except Exception as e:
            print(f"查找帖子失败: {str(e)}")
        
        return posts
    
    def test_interaction_response(self, driver: webdriver.Chrome, post_url: str):
        """测试交互响应时间"""
        try:
            print(f"\n测试交互响应 - 帖子: {post_url}")
            
            # 访问帖子页面
            load_time = self.measure_response_time(
                driver, 
                lambda: driver.get(post_url)
            )
            
            self.interaction_results.append({
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "operation": "帖子页面加载",
                "response_time_ms": load_time,
                "grade": self.categorize_response_time(load_time),
                "url": post_url
            })
            
            time.sleep(2)
            
            # 测试点赞响应
            try:
                like_buttons = driver.find_elements(By.XPATH, "//button[contains(@class, 'like') or contains(text(), '赞') or contains(@class, 'praise')]")
                if like_buttons:
                    like_time = self.measure_response_time(
                        driver,
                        lambda: like_buttons[0].click()
                    )
                    
                    self.interaction_results.append({
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "operation": "点赞操作",
                        "response_time_ms": like_time,
                        "grade": self.categorize_response_time(like_time),
                        "url": post_url
                    })
                    print(f"点赞响应时间: {like_time:.0f}ms")
                    
                    time.sleep(1)
                    
            except Exception as e:
                print(f"点赞操作失败: {str(e)}")
            
            # 测试评论响应
            try:
                # 查找评论输入框
                comment_inputs = driver.find_elements(By.XPATH, "//textarea[@placeholder='说点什么吧' or @placeholder='请输入评论' or contains(@class, 'comment')]")
                
                if comment_inputs:
                    comment_text = random.choice(self.random_comments)
                    print(f"📝 正在对帖子发表评论")
                    print(f"📱 评论帖子链接: {post_url}")
                    print(f"💬 评论内容: {comment_text}")
                    
                    comment_time = self.measure_response_time(
                        driver,
                        lambda: self._submit_comment(driver, comment_inputs[0], comment_text)
                    )
                    
                    self.interaction_results.append({
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "operation": "评论操作",
                        "response_time_ms": comment_time,
                        "grade": self.categorize_response_time(comment_time),
                        "url": post_url,
                        "comment": comment_text
                    })
                    print(f"✅ 评论响应时间: {comment_time:.0f}ms (内容: {comment_text})")
                    
                    time.sleep(2)  # 避免过于频繁的评论
                    
            except Exception as e:
                print(f"评论操作失败: {str(e)}")
                
        except Exception as e:
            print(f"交互测试失败: {str(e)}")
    
    def _submit_comment(self, driver: webdriver.Chrome, input_element, comment_text: str):
        """提交评论"""
        input_element.clear()
        input_element.send_keys(comment_text)
        
        # 查找并点击发送按钮
        submit_buttons = driver.find_elements(By.XPATH, "//button[contains(text(), '发送') or contains(text(), '发表') or contains(text(), '提交')]")
        
        if submit_buttons:
            submit_buttons[0].click()
        else:
            # 如果没有找到按钮，尝试按回车
            input_element.send_keys(u'\ue007')  # Enter key
    
    def run_full_test(self):
        """运行完整测试套件"""
        print("开始尼康官网自动化性能测试")
        print("=" * 50)
        
        # 定义要测试的页面
        test_pages = [
            {"url": self.base_url, "name": "首页"},
            {"url": f"{self.base_url}/post/photo", "name": "照片页面"},
            {"url": f"{self.base_url}/article", "name": "学习讨论页面"},
            {"url": f"{self.base_url}/circle", "name": "摄影圈页面"},
            {"url": f"{self.base_url}/more/onlinegallery", "name": "直营店画廊页面"}
        ]
        
        # 1. 页面性能测试
        print("\n第一阶段: 页面性能测试")
        print("-" * 30)
        
        for page in test_pages:
            self.test_page_performance(page["url"], page["name"])
            time.sleep(2)
        
        # 2. 基本操作响应时间测试
        print("\n第二阶段: 基本操作响应时间测试")
        print("-" * 30)
        
        driver = self.setup_driver()
        try:
            self.test_basic_operations(driver)
            
            # 3. 用户交互测试（需要登录）
            print("\n第三阶段: 用户交互测试")
            print("-" * 30)
            
            if self.login(driver):
                # 查找可交互的帖子
                posts = self.find_interactive_posts(driver)
                
                if posts:
                    # 限制交互测试的帖子数量，避免过度评论
                    test_posts = posts[:3]  # 最多测试3个帖子
                    
                    for i, post_url in enumerate(test_posts):
                        if i < 2:  # 只对前2个帖子进行完整交互测试
                            self.test_interaction_response(driver, post_url)
                            time.sleep(5)  # 增加间隔时间
                        else:
                            # 最后一个只测试页面加载
                            load_time = self.measure_response_time(
                                driver,
                                lambda: driver.get(post_url)
                            )
                            self.interaction_results.append({
                                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                "operation": "帖子页面加载",
                                "response_time_ms": load_time,
                                "grade": self.categorize_response_time(load_time),
                                "url": post_url
                            })
                else:
                    print("未找到可测试的帖子")
            else:
                print("跳过交互测试（登录失败）")
                
        finally:
            driver.quit()
        
        # 4. 生成测试报告
        self.generate_report()
    
    def generate_report(self):
        """生成测试报告"""
        print("\n" + "=" * 50)
        print("生成测试报告")
        print("=" * 50)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # 生成HTML报告
        html_report = self.generate_html_report(timestamp)
        report_path = f"nikon_performance_report_{timestamp}.html"
        
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(html_report)
        
        # 保存原始数据
        if self.test_results:
            df_performance = pd.DataFrame(self.test_results)
            df_performance.to_csv(f"nikon_performance_data_{timestamp}.csv", index=False, encoding="utf-8-sig")
        
        if self.interaction_results:
            df_interaction = pd.DataFrame(self.interaction_results)
            df_interaction.to_csv(f"nikon_interaction_data_{timestamp}.csv", index=False, encoding="utf-8-sig")
        
        print(f"\n测试报告已生成: {report_path}")
        print(f"性能测试数据: nikon_performance_data_{timestamp}.csv")
        print(f"交互测试数据: nikon_interaction_data_{timestamp}.csv")
        
        # 打印摘要
        self.print_summary()
    
    def generate_html_report(self, timestamp: str) -> str:
        """生成HTML格式的测试报告"""
        html = f"""
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>尼康官网自动化性能测试报告</title>
    <style>
        body {{ font-family: 'Microsoft YaHei', sans-serif; margin: 20px; }}
        .header {{ background-color: #f8f9fa; padding: 20px; border-radius: 8px; margin-bottom: 20px; }}
        .summary {{ background-color: #e9ecef; padding: 15px; border-radius: 6px; margin-bottom: 20px; }}
        table {{ border-collapse: collapse; width: 100%; margin-bottom: 20px; }}
        th, td {{ border: 1px solid #ddd; padding: 12px; text-align: left; }}
        th {{ background-color: #f2f2f2; font-weight: bold; }}
        .excellent {{ color: #28a745; font-weight: bold; }}
        .good {{ color: #17a2b8; font-weight: bold; }}
        .acceptable {{ color: #ffc107; font-weight: bold; }}
        .poor {{ color: #dc3545; font-weight: bold; }}
        .metric {{ background-color: #f8f9fa; padding: 10px; border-radius: 4px; margin: 5px 0; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🏮 尼康官网自动化性能测试报告</h1>
        <p><strong>测试时间:</strong> {timestamp.replace('_', ' ')}</p>
        <p><strong>测试网站:</strong> https://my.nikon.com.cn</p>
        <p><strong>测试类型:</strong> 页面性能测试 + 交互响应测试</p>
    </div>
    
    <div class="summary">
        <h2>📊 测试概览</h2>
        <div class="metric">页面性能测试数量: {len(self.test_results)}</div>
        <div class="metric">交互操作测试数量: {len(self.interaction_results)}</div>
    </div>
"""
        
        # 页面性能测试结果
        if self.test_results:
            html += """
    <h2>🚀 页面性能测试结果</h2>
    <table>
        <tr>
            <th>页面名称</th>
            <th>性能评分</th>
            <th>性能等级</th>
            <th>首次内容绘制 (ms)</th>
            <th>最大内容绘制 (ms)</th>
            <th>速度指数</th>
            <th>累计布局偏移</th>
        </tr>
"""
            
            for result in self.test_results:
                grade_class = self.get_grade_class(result.get("performance_grade", ""))
                html += f"""
        <tr>
            <td>{result['page_name']}</td>
            <td>{result['performance_score']:.1f}</td>
            <td class="{grade_class}">{result.get('performance_grade', 'N/A')}</td>
            <td>{result.get('fcp', 0):.0f}</td>
            <td>{result.get('lcp', 0):.0f}</td>
            <td>{result.get('speed_index', 0):.0f}</td>
            <td>{result.get('cls', 0):.3f}</td>
        </tr>
"""
            
            html += "    </table>"
        
        # 交互响应测试结果
        if self.interaction_results:
            html += """
    <h2>⚡ 交互响应测试结果</h2>
    <table>
        <tr>
            <th>操作类型</th>
            <th>响应时间 (ms)</th>
            <th>性能等级</th>
            <th>测试时间</th>
            <th>备注</th>
        </tr>
"""
            
            for result in self.interaction_results:
                grade_class = self.get_grade_class(result['grade'])
                comment_info = result.get('comment', '')
                url_info = result.get('url', '')
                
                note = ""
                if comment_info:
                    note += f"评论内容: {comment_info}"
                if url_info:
                    note += f" | URL: {url_info}"
                
                html += f"""
        <tr>
            <td>{result['operation']}</td>
            <td>{result['response_time_ms']:.0f}</td>
            <td class="{grade_class}">{result['grade']}</td>
            <td>{result['timestamp']}</td>
            <td>{note}</td>
        </tr>
"""
            
            html += "    </table>"
        
        html += """
    <div class="summary">
        <h2>📈 性能评级标准</h2>
        <div class="metric"><span class="excellent">优秀:</span> 响应时间 ≤ 200ms, Lighthouse评分 ≥ 90</div>
        <div class="metric"><span class="good">良好:</span> 响应时间 ≤ 500ms, Lighthouse评分 50-89</div>
        <div class="metric"><span class="acceptable">可接受:</span> 响应时间 ≤ 1000ms</div>
        <div class="metric"><span class="poor">差:</span> 响应时间 > 1000ms, Lighthouse评分 < 50</div>
    </div>
    
    <footer style="margin-top: 40px; padding: 20px; background-color: #f8f9fa; border-radius: 8px;">
        <p>🔧 测试工具: Python + Selenium + Lighthouse</p>
        <p>📝 报告生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    </footer>
</body>
</html>
"""
        return html
    
    def get_grade_class(self, grade: str) -> str:
        """根据性能等级获取CSS类名"""
        grade_map = {
            "优秀": "excellent",
            "良好": "good", 
            "中等": "good",
            "可接受": "acceptable",
            "差": "poor"
        }
        return grade_map.get(grade, "")
    
    def print_summary(self):
        """打印测试摘要"""
        print("\n" + "📊 测试摘要")
        print("-" * 30)
        
        if self.test_results:
            avg_score = sum(r['performance_score'] for r in self.test_results) / len(self.test_results)
            print(f"页面性能平均评分: {avg_score:.1f}")
            
            excellent_pages = [r for r in self.test_results if r.get('performance_grade') == '优秀']
            print(f"优秀页面数量: {len(excellent_pages)}/{len(self.test_results)}")
        
        if self.interaction_results:
            avg_response = sum(r['response_time_ms'] for r in self.interaction_results) / len(self.interaction_results)
            print(f"平均响应时间: {avg_response:.0f}ms")
            
            excellent_ops = [r for r in self.interaction_results if r['grade'] == '优秀']
            print(f"优秀操作数量: {len(excellent_ops)}/{len(self.interaction_results)}")


if __name__ == "__main__":
    # 运行测试
    tester = NikonPerformanceTest()
    tester.run_full_test()
