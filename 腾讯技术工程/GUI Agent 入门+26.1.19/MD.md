# 原文逐页转写

文本来自本次 PDF 文本层；不补写图片、截断内容或代码。图片和布局请打开每页 PDF 链接核对。AI 解释另见学习笔记。

## PDF 第 1 页

[原页](RAW.pdf#page=1)

````text
有⼿就⾏，教你从 0 到 1 快速⼿搓搭建个 GUI  Agent
腾讯程序员 Jan  19 , 2026 , 1 : 36  AM⼴东原创 腾讯技术⼯程 1539  listened
作者： zishanshi
⼀、前⾔
什么是 GUI Agent ？简单来说，就是⼀个能够 " 看懂 " 屏幕（ mobile/pc/web ）并进⾏⾃动操作
的 AI Agent 。⽐如⽤户发送指令 “ 整理⽂件 ” ， PC GUI Agent 就可以基于纯 GUI 界⾯理解页⾯内
容，进⾏逐步决策 & 操作，直到完成⽤户任务。
随着 GUI Agent 的应⽤前景逐渐明朗， GUI Agent 在 25 年的发展很迅猛，其中⼀个⽐较明显的
新趋势是，通⽤⼤模型也在训练 GUI 上的能⼒：
随着通⽤⼤模型向着 agentic 以及 GUI 理解增强的⽅向发展，现在 Gemini 3 Flash 等通⽤⼤
模型已经可以直接⽤来搭建⼀个效果还不错的 GUI Agent ，并且实践难度⼤幅降低，半⼩
时左右就可以从 0 到 1 ⼿搓出来。本⽂详细介绍如何逐步搭建⼀个 GUI Agent ，从实践中也
可快速了解 GUI Agent 的原理。
````

## PDF 第 2 页

[原页](RAW.pdf#page=2)

````text
因此，搭建⼀个好⽤的 GUI Agent 变得越来越简单。本⽂介绍如何使⽤通⽤⼤模型 API ，快速
从 0 到 1 搭建⼀个可⽤性强的 PC GUI Agent ，可以⽤于⾃动完成 PC 任务操作。
前置准备说明 : 我使⽤的是 Gemini 3 Flash ，先看效果：
⼆、 GUI Agent 基础原理介绍
⼀个 GUI Agent 通常包含以下⼏个部分：
````

## PDF 第 3 页

[原页](RAW.pdf#page=3)

````text
1. 设备环境（ Environment ）：⽐如⼿机、电脑这些⽤来操作的设备，是交互的  “ 载体 “ ，本⽂
仅以电脑为⽰例。
2. 感知系统（ Preceptor ）：负责  “ 接收信息 “ ，这主要是针对 GUI 能⼒较弱的通⽤⼤模型。⽽
Gemini 3 Flash 这样本⾝具备较强 GUI 页⾯理解能⼒的⼤模型通常不再需要单独设计感知系
统。
3. ⼤模型（决策器）：相当于  “ ⼤脑 ”—— 结合知识系统⾥存的信息，分析感知到的界⾯内
容，决定要完成任务，下⼀步应该如何操作。
4. 交互系统（ Operator ）：相当于 “ ⼿脚 ” —— 把⼤模型的决策结果（操作动作 + 坐标），转化
为具体的操作与设备进⾏交互。
为了完成⼀个完整的任务，通常需要进⾏  “ 感知 -> 决策 -> 执⾏ ” 的多次循环，直到任务完
成。下⽂具体介绍 PC GUI Agent 的搭建⽅式。
三、逐步搭建 GUI Agent
1. 最简单的模型对话
在开始构建复杂的 Agent 之前，我们先实现最基础的功能：让 AI 看懂⼀张图⽚。
# utils/model.py
import os
import base64
from openai import OpenAI
from typing import List, Dict, Any
API_KEY = os.getenv("OPENAI_API_KEY")
BASE_URL = os.getenv("OPENAI_BASE_URL")
class LVMChat:
    """ 多模态⼤模型聊天类 """
    
    def __init__(self, api_key: str = API_KEY, base_url: str = BASE_URL, 
                 model: str = "gemini-3-flash-preview"):
        self.client = OpenAI(api_key=api_key, base_url=base_url)
        self.model = model
    
    def _encode_image(self, image_path: str) -> str:
        """ 将图⽚编码为 base64"""
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    
````

## PDF 第 4 页

[原页](RAW.pdf#page=4)

````text
    def get_multimodal_response(self, text: str, image_paths: str) -> str:
        """
        最简单的图⽂对话
        
        Args:
            text: 你的问题
            image_paths: 图⽚路径
        
        Returns:
            模型的回答
        """
        # 1. 加载图⽚
        base64_image = self._encode_image(image_paths)
        
        # 2. 构建消息
        messages = [{
            "role": "user",
            "content": [
                {"type": "image_url", 
                 "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}},
                {"type": "text", "text": text}
            ]
        }]
        
        # 3. 调⽤ API
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages
        )
        
        return response.choices[0].message.content
测试⼀下：
chat = LVMChat()
response = chat.get_multimodal_response(
    text=" 这张图⽚⾥输⼊框坐标？ ",
    image_paths="image.png"
)
print(response)
注意看这⾥！模型本⾝是有定位能⼒的（也就是说可以直接输出操作对象的坐标位置），所以
不需要格外的感知器来锚定具体 UI 元素。
````

## PDF 第 5 页

[原页](RAW.pdf#page=5)

````text
2. 加⼊记忆  - 让 AI 记住上下⽂
上⾯的代码有个问题： AI 每次都是 " 失忆 " 的，不记得之前说过什么。对于 GUI Agent 来说，这
是很致命的。举个简单的例⼦，任务 “ 在输⼊框输⼊ ‘ 你好 ’” ，如果 Agent 没有记忆，那么后序执
⾏不记得⾃⼰已经决策过输⼊操作，就会陷⼊输⼊的循环，在输⼊框中多次输⼊ ‘ 你好 ’ ⽽不会
停⽌。相反，有上⽂记忆的 Agent ，知道⾃⼰前⼀次已经决策了输⼊操作，结合当前页⾯内
容，判断本次应为 “ﬁnish” 指令，就不会陷⼊输⼊循环。
为此，我们需要升级  LVMChat 类：
class LVMChat:
    """ ⽀持会话记忆的多模态聊天类 """
    
    def __init__(self, api_key: str = API_KEY, base_url: str = BASE_URL, 
                 model: str = "gemini-3-flash-preview"):
        self.client = OpenAI(api_key=api_key, base_url=base_url)
        self.model = model
        # 🔥  核⼼改动：添加会话历史记录
        self.conversation_history: List[Dict[str, Any]] = []
    
    def get_multimodal_response(self, text: str, image_paths: str, 
                                use_history: bool = False) -> str:
        """
        ⽀持记忆的图⽂对话
        
        Args:
            text: 你的问题
            image_paths: 图⽚路径
            use_history: 是否使⽤会话历史（记住之前的对话）
        """
        # 1. 加载图⽚并构建当前消息
        base64_image = self._encode_image(image_paths)
````

## PDF 第 6 页

[原页](RAW.pdf#page=6)

````text
        current_message = {
            "role": "user",
            "content": [
                {"type": "image_url", 
                 "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}},
                {"type": "text", "text": text}
            ]
        }
        
        # 2. 🔥  关键：如果启⽤历史，把之前的对话也带上
        if use_history:
            messages = self.conversation_history + [current_message]
            print(f" 📚  使⽤历史上下⽂，共  {len(self.conversation_history)}  条 ")
        else:
            messages = [current_message]
        
        # 3. 调⽤ API
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages
        )
        
        result = response.choices[0].message.content
        
        # 4. 🔥  更新历史记录
        if use_history:
            self.conversation_history.append(current_message)
            self.conversation_history.append({
                "role": "assistant", 
                "content": result
            })
        
        return result
    
    def clear_history(self):
        """ 清空记忆 """
        self.conversation_history = []
记忆的原理：
# 第⼀轮对话
conversation_history = [
    {"role": "user", "content": [ 图⽚1, " 在输⼊框输⼊ ‘ 你好 ’"]},
    {"role": "assistant", "content": "{'Thought' ：  ' 输⼊框在⻚⾯中间位置，我需要输⼊⽂案 ', 'Act
]
````

## PDF 第 7 页

[原页](RAW.pdf#page=7)

````text
# 第⼆轮对话时，把历史也带上
messages = conversation_history + [
    {"role": "user", "content": [ 图⽚2, " 在输⼊框输⼊ ‘ 你好 ’"]}
]
# 现在 AI 能看到完整的对话链，知道⾃⼰做过什么决策。在第⼆轮返回 :
{'Thought'：  ' 上⼀轮已经完成输⼊操作并且⽂案已经正确显示在输⼊框，任务已经完成 ', 'Action': 'finishe
3. 搭建 Agent 框架
现在组装成⼀个完整的 Agent ，我们使⽤ LangGraph 来构建⼯作流。
（ 1 ） Agent 的核⼼循环
⼀个 GUI Agent 的⼯作流程是这样的：
（ 2 ）执⾏器 Operator
⾸先，我们需要⼀个能够真正控制⿏标键盘的⼯具类。在这⾥强烈推荐pyautogui, 模拟键⿏操
作，⾮常简单易⽤。但是有⼀个坑需要注意，输⼊操作需要⽤复制粘贴操作⽽不是打字，因为
pyautogui.write() 不⽀持中⽂！⽽⽤剪贴板粘贴可以完美⽀持中英⽂、特殊字符
# operator/execute.py - 
import pyautogui
import pyperclip
import mss
import time
# 允许⿏标移动到屏幕⻆落（默认会触发 fail-safe ）
pyautogui.FAILSAFE = False
class Operation:
    """GUI 操作⼯具类 """
    
````

## PDF 第 8 页

[原页](RAW.pdf#page=8)

````text
    def click(self, x: int, y: int):
        """ 点击指定坐标 """
        print(f" 🖱    点击坐标  ({x}, {y})")
        pyautogui.click(x=x, y=y)
    
    def input(self, text: str):
        """ 输⼊⽂本（使⽤粘贴⽅式，⽀持中⽂） """
        print(f" ⌨    输⼊ : {text}")
        pyperclip.copy(text)  # 复制到剪贴板
        pyautogui.hotkey('command', 'v')  # Mac ⽤ command ， Windows ⽤ ctrl
    
    def screenshot(self, save_path: str):
        """ 截图并保存 """
        with mss.mss() as sct:
            sct.shot(output=save_path)
        print(f" 📸  截图已保存 : {save_path}")
    
    def hotkey(self, *keys):
        """ 按下组合键（如 ctrl+c ） """
        print(f" ⌨    按下组合键 : {' + '.join(keys)}")
        pyautogui.hotkey(*keys)
    
    def wait(self, seconds: float = 1.0):
        """ 等待指定时间 """
        print(f" ⏱    等待  {seconds}  秒 ...")
        time.sleep(seconds)
（ 3 ） Prompt
GUI Agent 的提⽰词告诉 AI 应该如何 " 思考 " 和 " ⾏动 " 的规则，需要定义好操作空间和输出格
式，我在UI-TARS 官⽅ Prompt的基础上做了很⼩的改动（增加了 Output Example ，因为我发
现 Gemini 3 Flash 使⽤ UI-TARS 的 prompt 输出格式不是很稳定）。
# utils/prompts.py
COMPUTER_USE_UITARS = """You are a GUI agent. You are given a task and your action histor
## Action Space
click(point='<point>x1 y1</point>')
left_double(point='<point>x1 y1</point>')
right_single(point='<point>x1 y1</point>')
drag(start_point='<point>x1 y1</point>', end_point='<point>x2 y2</point>')
hotkey(key='ctrl c') # Split keys with a space and use lowercase. Also, do not use more t
type(content='xxx') # Use escape characters \\', \\\", and \\n in content part to ensure 
scroll(point='<point>x1 y1</point>', direction='down or up or right or left') # Show more 
wait() #Sleep for 5s and take a screenshot to check for any changes.
finished(content='xxx') # Use escape characters \\', \\", and \\n in content part to ensu
````

## PDF 第 9 页

[原页](RAW.pdf#page=9)

````text
## Note
- Use Chinese in `Thought` part.
- Write a small plan and finally summarize your next action (with its target element) in 
- One action per turn.
## Output Example
{{
    "Thought": "...",
    "Action": "..."
}}
## User Instruction
{instruction}
"""
（ 4 ）坐标归⼀化
不同电脑屏幕分辨率不同（ 1920x1080 、 2560x1440 等）， GUI Agent 往往会采⽤千归⼀化坐
标的策略进⾏处理。因此，拿到⼤模型的返回之后，需要将归⼀化坐标  (0-1000 范围 ) 还原成
实际像素坐标：
# AI 返回归⼀化坐标 : (500, 500) - 表示屏幕中⼼
# 在 1920x1080 屏幕上 : (500, 500) -> (960, 540)
# 在 2560x1440 屏幕上 : (500, 500) -> (1280, 720)
def normalize_coords(self, x: int, y: int) -> tuple[int, int]:
    """ 将归⼀化坐标 (0-1000) 转换为实际像素坐标 """
    actual_x = int(x / 1000.0 * self.screen_width)
    actual_y = int(y / 1000.0 * self.screen_height)
    return actual_x, actual_y
（ 5 ） LangGraph
LangGraph 是⼀个⽤于构建 Agent ⼯作流的框架，图 (Graph)的⽅式定义 Agent 的执⾏逻辑。
# 传统⽅式（硬编码）
def run_agent():
    whilenot finished:
        screenshot()
        decision = model_decide()
        execute(decision)
        if check_finished():
            break
````

## PDF 第 10 页

[原页](RAW.pdf#page=10)

````text
# LangGraph ⽅式（声明式）
workflow = StateGraph(AgentState)
workflow.add_node("screenshot", take_screenshot)
workflow.add_node("decide", model_decide)
workflow.add_node("execute", execute_action)
workflow.add_edge("screenshot", "decide")
workflow.add_edge("decide", "execute")
workflow.add_conditional_edges("execute", should_continue, {...})
优势： ✅  逻辑清晰：可视化⼯作流  ✅  易于修改：添加节点 / 改变流程很简单  ✅  状态管理：
⾃动在节点间传递状态。
AgentState 是整个⼯作流的 " 记忆载体 " ，在各个节点间传递：
# Step 1: 截图节点
state = {
    "instruction": " 打开浏览器 ",
    "screenshot_path": "s/step_1.png",
    "step": 1,
    "finished": False
}
# Step 2: 决策节点（接收 state ，更新后返回）
state = {
    **state,  # 保留之前的数据
    "thought": " 需要点击 Chrome 图标 ",
    "action": "click(point='<point>100 200</point>')"
}
# Step 3: 执⾏节点
state = {
    **state,  # 继续保留
    # 执⾏点击操作 ...
}
（ 6 ） Agent 主程序
现在把所有模块组装起来：
````

## PDF 第 11 页

[原页](RAW.pdf#page=11)

````text
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GUI Agent - ⾃动化 GUI 测试 Agent
截图  -> 模型决策  -> 解析 Action -> 执⾏  -> 循环，直到 finished
"""
import re
import json
from datetime import datetime
from typing import TypedDict
from pathlib import Path
from langgraph.graph import StateGraph, END
from operator.execute import Operation
from utils.model import LVMChat, Model
from utils.prompts import COMPUTER_USE_UITARS
# 定义 State
class AgentState(TypedDict):
    instruction: str  # ⽤户指令
    screenshot_path: str  # 当前截图路径
    step: int  # 当前步骤
    thought: str  # 模型思考
    action: str  # 模型输出的动作
    finished: bool  # 是否完成
class GUIAgent:
    """GUI ⾃动化 Agent"""
    
    def __init__(self, instruction: str, model_name: str = Model.GOOGLE_GEMINI_3_FLASH_PR
        self.instruction = instruction
        self.operation = Operation()
        self.lvm_chat = LVMChat(model=model_name)
        self.s_dir = Path("s")
        self.s_dir.mkdir(exist_ok=True)
        
        # 获取屏幕尺⼨⽤于坐标映射
        import pyautogui
        self.screen_width, self.screen_height = pyautogui.size()
        print(f" 🖥    屏幕尺⼨ : {self.screen_width}x{self.screen_height}")
    
    def normalize_coords(self, x: int, y: int) -> tuple[int, int]:
        """ 将归⼀化坐标 (0-1000) 转换为实际像素坐标 """
        actual_x = int(x / 1000.0 * self.screen_width)
````

## PDF 第 12 页

[原页](RAW.pdf#page=12)

````text
        actual_y = int(y / 1000.0 * self.screen_height)
        print(f"   归⼀化坐标  ({x}, {y}) -> 实际坐标  ({actual_x}, {actual_y})")
        return actual_x, actual_y
        
    def take_screenshot(self, state: AgentState) -> AgentState:
        """ 步骤 1: 截图并保存 """
        step = state.get("step", 0) + 1
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        screenshot_path = str(self.s_dir / f"step_{step}_{timestamp}.png")
        
        self.operation.screenshot(screenshot_path)
        
        return {
            **state,
            "instruction": self.instruction,
            "screenshot_path": screenshot_path,
            "step": step,
            "finished": False
        }
    
    def model_decide(self, state: AgentState) -> AgentState:
        """ 步骤 2: 模型决策（⾃动使⽤会话历史） """
        prompt = COMPUTER_USE_UITARS.format(instruction=state["instruction"])
        
        # 调⽤多模态模型（ use_history=True ⾃动保留上下⽂）
        response = self.lvm_chat.get_multimodal_response(
            text=prompt,
            image_paths=state["screenshot_path"],
            res_format="json",
            use_history=True# 启⽤会话历史，模型会记住之前的所有交互
        )
        
        print(f"\n 📸  Step {state['step']} - 模型响应 :\n{response}\n")
        
        # 解析 JSON 响应
        try:
            result = json.loads(response)
            thought = result.get("Thought", "")
            action = result.get("Action", "")
        except json.JSONDecodeError:
            # 如果不是 JSON 格式，尝试正则提取
            thought_match = re.search(r'"Thought":\s*"([^"]*)"', response)
            action_match = re.search(r'"Action":\s*"([^"]*)"', response)
            thought = thought_match.group(1) if thought_match else""
            action = action_match.group(1) if action_match else""
        
        return {
````

## PDF 第 13 页

[原页](RAW.pdf#page=13)

````text
            **state,
            "thought": thought,
            "action": action
        }
    
    def execute_action(self, state: AgentState) -> AgentState:
        """ 步骤 3: 解析并执⾏动作 """
        action = state["action"]
        
        ifnot action:
            print(" ⚠  没有可执⾏的动作 ")
            return {**state, "finished": True}
        
        # 检查是否完成
        if action.startswith("finished("):
            content_match = re.search(r"finished\(content='([^']*)'\)", action)
            content = content_match.group(1) if content_match else" 任务完成 "
            print(f" ✅  任务完成 : {content}")
            return {**state, "finished": True}
        
        # 解析并执⾏动作
        try:
            self._parse_and_execute(action)
        except Exception as e:
            print(f" ❌  执⾏动作失败 : {e}")
            print(f"   动作 : {action}")
        
        return state
    
    def _parse_and_execute(self, action: str):
        """ 解析动作字符串并执⾏ """
        print(f" 🔧  执⾏动作 : {action}")
        
        # click(point='<point>x y</point>') 或  click(point='x y')
        if action.startswith("click("):
            # 尝试带标签的格式
            point_match = re.search(r"<point>(\d+)\s+(\d+)</point>", action)
            ifnot point_match:
                # 尝试不带标签的格式
                point_match = re.search(r"point=['\"](\d+)\s+(\d+)['\"]", action)
            
            if point_match:
                x, y = int(point_match.group(1)), int(point_match.group(2))
                actual_x, actual_y = self.normalize_coords(x, y)
                self.operation.click(actual_x, actual_y)
            else:
                print(f" ⚠  ⽆法解析点击坐标 : {action}")
````

## PDF 第 14 页

[原页](RAW.pdf#page=14)

````text
        
        # left_double(point='<point>x y</point>') 或  double_click(point='x y')
        elif action.startswith("left_double("):
            # 尝试带标签的格式
            point_match = re.search(r"<point>(\d+)\s+(\d+)</point>", action)
            ifnot point_match:
                # 尝试不带标签的格式
                point_match = re.search(r"point=['\"](\d+)\s+(\d+)['\"]", action)
            
            if point_match:
                x, y = int(point_match.group(1)), int(point_match.group(2))
                actual_x, actual_y = self.normalize_coords(x, y)
                self.operation.double_click(actual_x, actual_y)
            else:
                print(f" ⚠  ⽆法解析双击坐标 : {action}")
        
        # type(content='xxx')
        elif action.startswith("type("):
            content_match = re.search(r"content=['\"]([^'\"]*)['\"]", action)
            if content_match:
                text = content_match.group(1)
                # 处理转义字符
                text = text.replace(r"\'", "'").replace(r'\"', '"').replace(r"\n", "\n")
                self.operation.input(text)
        
        # hotkey(key='ctrl c')
        elif action.startswith("hotkey("):
            key_match = re.search(r"key=['\"]([^'\"]*)['\"]", action)
            if key_match:
                keys = key_match.group(1).split()
                self.operation.hotkey(*keys)
        
        # scroll(point='<point>x y</point>', direction='down') 或  scroll(point='x y', dire
        elif action.startswith("scroll("):
            # 尝试带标签的格式
            point_match = re.search(r"<point>(\d+)\s+(\d+)</point>", action)
            ifnot point_match:
                # 尝试不带标签的格式
                point_match = re.search(r"point=['\"](\d+)\s+(\d+)['\"]", action)
            
            direction_match = re.search(r"direction=['\"]([^'\"]*)['\"]", action)
            if point_match and direction_match:
                x, y = int(point_match.group(1)), int(point_match.group(2))
                actual_x, actual_y = self.normalize_coords(x, y)
                direction = direction_match.group(1)
                # 移动到位置并滚动
                import pyautogui
````

## PDF 第 15 页

[原页](RAW.pdf#page=15)

````text
                pyautogui.moveTo(actual_x, actual_y)
                scroll_amount = 3if direction in ["up", "left"] else-3
                pyautogui.scroll(scroll_amount)
        
        # wait()
        elif action.startswith("wait("):
            self.operation.wait(seconds=5)
        
        # drag(start_point='<point>x1 y1</point>', end_point='<point>x2 y2</point>')
        elif action.startswith("drag("):
            # 尝试带标签的格式
            start_match = re.search(r"start_point=['\"]<point>(\d+)\s+(\d+)</point>['\"]"
            end_match = re.search(r"end_point=['\"]<point>(\d+)\s+(\d+)</point>['\"]", ac
            
            ifnot start_match:
                # 尝试不带标签的格式
                start_match = re.search(r"start_point=['\"](\d+)\s+(\d+)['\"]", action)
                end_match = re.search(r"end_point=['\"](\d+)\s+(\d+)['\"]", action)
            
            if start_match and end_match:
                x1, y1 = int(start_match.group(1)), int(start_match.group(2))
                x2, y2 = int(end_match.group(1)), int(end_match.group(2))
                actual_x1, actual_y1 = self.normalize_coords(x1, y1)
                actual_x2, actual_y2 = self.normalize_coords(x2, y2)
                import pyautogui
                pyautogui.moveTo(actual_x1, actual_y1)
                pyautogui.drag(actual_x2 - actual_x1, actual_y2 - actual_y1, duration=0.5
        
        # 等待⼀下让界⾯响应
        self.operation.wait(seconds=1)
    
    def should_continue(self, state: AgentState) -> str:
        """ 判断是否继续循环 """
        return"end"if state.get("finished", False) else"continue"
    
    def run(self):
        """ 运⾏ Agent"""
        # 构建 graph
        workflow = StateGraph(AgentState)
        
        # 添加节点
        workflow.add_node("screenshot", self.take_screenshot)
        workflow.add_node("decide", self.model_decide)
        workflow.add_node("execute", self.execute_action)
        
        # 添加边
        workflow.set_entry_point("screenshot")
````

## PDF 第 16 页

[原页](RAW.pdf#page=16)

````text
        workflow.add_edge("screenshot", "decide")
        workflow.add_edge("decide", "execute")
        workflow.add_conditional_edges(
            "execute",
            self.should_continue,
            {
                "continue": "screenshot",
                "end": END
            }
        )
        
        # 编译并运⾏
        app = workflow.compile()
        
        print(f" 🚀  开始执⾏任务 : {self.instruction}\n")
        
        # 设置递归限制为 100 步
        config = {"recursion_limit": 100}
        final_state = app.invoke(
            {"instruction": self.instruction, "step": 0},
            config=config
        )
        
        print(f"\n 🎉  任务完成 ! 共执⾏  {final_state['step']}  步 ")
        return final_state
if __name__ == "__main__":
    agent = GUIAgent(instruction=""" 打开浏览器查询 GUI, 找到 wikipedia 的介绍⻚⾯进⾏查看 """)
    agent.run()
4. 执⾏效果
⽂章前⾔部分的 demo, 模型的部分决策内容如下 :
````

## PDF 第 17 页

[原页](RAW.pdf#page=17)

````text
对于中间步骤，模型会利⽤到上⽂的内容，与当前页⾯状态⼀起作为决策依据：
最后，如果模型判断任务完成，会输出 ﬁnished 指令，程序停⽌
````

## PDF 第 18 页

[原页](RAW.pdf#page=18)

````text
四、总结
本⽂采⽤简洁易⽤的⽅案搭建了⼀个  PC 端的  GUI Agent ，该  Agent 不仅能在  Windows 和
macOS 系统上直接运⾏，还可操作  Web 应⽤。得益于以  pyautogui （键⿏模拟）作为核⼼执
⾏器，该  Agent 能够实现跨应⽤的操作能⼒。未来可通过补充滑动、拖拽等更多样的交互⽅
式，并结合知识库的构建，进⼀步强化其针对特定业务场景的适配性，打造功能更强⼤的  GUI
Agent 。
腾讯技术官⽅号。腾讯技术创新、前沿领域发布解读平台。
688 篇原创内容
腾讯技术⼯程
公众号
````

## PDF 第 19 页

[原页](RAW.pdf#page=19)

````text
阅读 1 . 1 万
留⾔
还没有留⾔，来写⾸评
写留⾔
````

## 采集与转写核验记录（非原文）

以下说明由本次核验添加；上方逐页文本保持文本层原样，图片与布局以PDF为准。

- PDF物理页 11,12,13,14,15：代码段在 PDF/提取文本中有省略、缺行和 OCR 错误；无法确认完整依赖或语法，本文未补写也未执行。示例禁用 fail-safe，但未讨论由此产生的风险。
