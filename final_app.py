#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
健康卡路里计算APP - 云端构建优化版本
简化依赖，确保成功打包
"""

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.metrics import dp, sp
from kivy.graphics import Color, Rectangle
from kivy.core.window import Window
import json
import os
from datetime import datetime

# 设置窗口背景色为白色
Window.clearcolor = (1, 1, 1, 1)

class HealthApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.daily_foods = []
        self.daily_calories = 0
        self.goal_calories = 2000
        
        # 简化的食物数据库
        self.food_database = {
            '苹果': {'calories_per_100g': 52, 'default_serving': 150},
            '香蕉': {'calories_per_100g': 89, 'default_serving': 120},
            '米饭': {'calories_per_100g': 130, 'default_serving': 150},
            '鸡肉': {'calories_per_100g': 165, 'default_serving': 100},
            '牛奶': {'calories_per_100g': 42, 'default_serving': 250},
            '面包': {'calories_per_100g': 265, 'default_serving': 50},
            '鸡蛋': {'calories_per_100g': 155, 'default_serving': 50},
            '西红柿': {'calories_per_100g': 18, 'default_serving': 100},
            '土豆': {'calories_per_100g': 77, 'default_serving': 150},
            '胡萝卜': {'calories_per_100g': 41, 'default_serving': 80}
        }
    
    def build(self):
        """构建主界面"""
        self.screen_manager = ScreenManager()
        
        # 创建主屏幕
        main_screen = self.create_main_screen()
        self.screen_manager.add_widget(main_screen)
        
        # 创建添加食物屏幕
        add_food_screen = self.create_add_food_screen()
        self.screen_manager.add_widget(add_food_screen)
        
        # 创建历史记录屏幕
        history_screen = self.create_history_screen()
        self.screen_manager.add_widget(history_screen)
        
        # 创建拍照屏幕
        photo_screen = self.create_photo_screen()
        self.screen_manager.add_widget(photo_screen)
        
        return self.screen_manager
    
    def create_main_screen(self):
        """创建主屏幕"""
        screen = Screen(name='main')
        main_layout = BoxLayout(orientation='vertical', padding=20, spacing=20)
        
        # 白色背景
        with main_layout.canvas.before:
            Color(1, 1, 1, 1)
            main_layout.bg = Rectangle(size=main_layout.size, pos=main_layout.pos)
        main_layout.bind(size=self._update_bg, pos=self._update_bg)
        
        # 标题
        title = Label(
            text='健康卡路里计算',
            font_size=sp(28),
            color=(0.1, 0.6, 0.1, 1),
            size_hint_y=None,
            height=dp(60)
        )
        
        # 今日统计
        self.stats_label = Label(
            text=f'今日摄入: {self.daily_calories} / {self.goal_calories} 卡路里',
            font_size=sp(18),
            color=(0.2, 0.2, 0.2, 1),
            size_hint_y=None,
            height=dp(40)
        )
        
        # 功能按钮
        button_layout = BoxLayout(orientation='vertical', spacing=15)
        
        # 添加食物按钮
        add_food_btn = Button(
            text='📝 添加食物',
            font_size=sp(18),
            size_hint_y=None,
            height=dp(60),
            background_color=(0.2, 0.7, 0.2, 1)
        )
        add_food_btn.bind(on_press=self.go_to_add_food)
        
        # 拍照识别按钮
        photo_btn = Button(
            text='📷 拍照识别',
            font_size=sp(18),
            size_hint_y=None,
            height=dp(60),
            background_color=(0.6, 0.2, 0.8, 1)
        )
        photo_btn.bind(on_press=self.go_to_photo)
        
        # 历史记录按钮
        history_btn = Button(
            text='📋 历史记录',
            font_size=sp(18),
            size_hint_y=None,
            height=dp(60),
            background_color=(0.2, 0.4, 0.8, 1)
        )
        history_btn.bind(on_press=self.go_to_history)
        
        button_layout.add_widget(add_food_btn)
        button_layout.add_widget(photo_btn)
        button_layout.add_widget(history_btn)
        
        main_layout.add_widget(title)
        main_layout.add_widget(self.stats_label)
        main_layout.add_widget(button_layout)
        
        screen.add_widget(main_layout)
        return screen
    
    def create_add_food_screen(self):
        """创建添加食物屏幕"""
        screen = Screen(name='add_food')
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        # 白色背景
        with layout.canvas.before:
            Color(1, 1, 1, 1)
            layout.bg = Rectangle(size=layout.size, pos=layout.pos)
        layout.bind(size=self._update_bg, pos=self._update_bg)
        
        # 标题和返回按钮
        header = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(50))
        
        back_btn = Button(
            text='< 返回',
            size_hint_x=None,
            width=dp(80),
            background_color=(0.6, 0.6, 0.6, 1)
        )
        back_btn.bind(on_press=self.go_to_main)
        
        title = Label(
            text='添加食物',
            font_size=sp(20),
            color=(0.1, 0.6, 0.1, 1)
        )
        
        header.add_widget(back_btn)
        header.add_widget(title)
        
        # 食物输入
        food_label = Label(
            text='食物名称:',
            font_size=sp(16),
            color=(0.2, 0.2, 0.2, 1),
            size_hint_y=None,
            height=dp(30)
        )
        
        self.food_input = TextInput(
            hint_text='例如: 苹果, 米饭, 鸡肉',
            font_size=sp(16),
            size_hint_y=None,
            height=dp(40)
        )
        
        # 重量输入
        weight_label = Label(
            text='重量(克):',
            font_size=sp(16),
            color=(0.2, 0.2, 0.2, 1),
            size_hint_y=None,
            height=dp(30)
        )
        
        self.weight_input = TextInput(
            hint_text='例如: 100',
            font_size=sp(16),
            size_hint_y=None,
            height=dp(40)
        )
        
        # 添加按钮
        add_btn = Button(
            text='添加到今日摄入',
            font_size=sp(18),
            size_hint_y=None,
            height=dp(50),
            background_color=(0.2, 0.7, 0.2, 1)
        )
        add_btn.bind(on_press=self.add_food_to_daily)
        
        # 食物列表
        food_list_label = Label(
            text='常用食物:',
            font_size=sp(16),
            color=(0.2, 0.2, 0.2, 1),
            size_hint_y=None,
            height=dp(30)
        )
        
        # 滚动视图显示食物列表
        scroll = ScrollView()
        food_list_layout = BoxLayout(orientation='vertical', size_hint_y=None, spacing=5)
        food_list_layout.bind(minimum_height=food_list_layout.setter('height'))
        
        for food_name, info in self.food_database.items():
            food_btn = Button(
                text=f'{food_name} ({info["calories_per_100g"]}卡/100g)',
                size_hint_y=None,
                height=dp(40),
                font_size=sp(14),
                background_color=(0.9, 0.9, 0.9, 1),
                color=(0.2, 0.2, 0.2, 1)
            )
            food_btn.bind(on_press=lambda x, food=food_name: self.select_food(food))
            food_list_layout.add_widget(food_btn)
        
        scroll.add_widget(food_list_layout)
        
        layout.add_widget(header)
        layout.add_widget(food_label)
        layout.add_widget(self.food_input)
        layout.add_widget(weight_label)
        layout.add_widget(self.weight_input)
        layout.add_widget(add_btn)
        layout.add_widget(food_list_label)
        layout.add_widget(scroll)
        
        screen.add_widget(layout)
        return screen
    
    def create_history_screen(self):
        """创建历史记录屏幕"""
        screen = Screen(name='history')
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        # 白色背景
        with layout.canvas.before:
            Color(1, 1, 1, 1)
            layout.bg = Rectangle(size=layout.size, pos=layout.pos)
        layout.bind(size=self._update_bg, pos=self._update_bg)
        
        # 标题和返回按钮
        header = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(50))
        
        back_btn = Button(
            text='< 返回',
            size_hint_x=None,
            width=dp(80),
            background_color=(0.6, 0.6, 0.6, 1)
        )
        back_btn.bind(on_press=self.go_to_main)
        
        title = Label(
            text='历史记录',
            font_size=sp(20),
            color=(0.1, 0.6, 0.1, 1)
        )
        
        header.add_widget(back_btn)
        header.add_widget(title)
        
        # 历史记录列表
        scroll = ScrollView()
        self.history_layout = BoxLayout(orientation='vertical', size_hint_y=None, spacing=5)
        self.history_layout.bind(minimum_height=self.history_layout.setter('height'))
        
        # 显示今日记录
        self.update_history_display()
        
        scroll.add_widget(self.history_layout)
        
        layout.add_widget(header)
        layout.add_widget(scroll)
        
        screen.add_widget(layout)
        return screen
    
    def create_photo_screen(self):
        """创建拍照识别屏幕"""
        screen = Screen(name='photo')
        layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        # 白色背景
        with layout.canvas.before:
            Color(1, 1, 1, 1)
            layout.bg = Rectangle(size=layout.size, pos=layout.pos)
        layout.bind(size=self._update_bg, pos=self._update_bg)
        
        # 标题和返回按钮
        header = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(50))
        
        back_btn = Button(
            text='< 返回',
            size_hint_x=None,
            width=dp(80),
            background_color=(0.6, 0.6, 0.6, 1)
        )
        back_btn.bind(on_press=self.go_to_main)
        
        title = Label(
            text='拍照识别食物',
            font_size=sp(20),
            color=(0.1, 0.6, 0.1, 1)
        )
        
        header.add_widget(back_btn)
        header.add_widget(title)
        
        # 拍照按钮
        photo_btn = Button(
            text='📷 拍照识别 (演示模式)',
            font_size=sp(18),
            size_hint_y=None,
            height=dp(60),
            background_color=(0.2, 0.7, 0.2, 1)
        )
        photo_btn.bind(on_press=self.simulate_photo_recognition)
        
        # 说明文字
        info_label = Label(
            text='拍照功能在Android设备上可以调用真实相机\n当前为演示模式，点击按钮体验AI识别效果',
            font_size=sp(14),
            color=(0.4, 0.4, 0.4, 1),
            size_hint_y=None,
            height=dp(60)
        )
        
        # 识别结果区域
        results_label = Label(
            text='识别结果:',
            font_size=sp(16),
            color=(0.2, 0.2, 0.2, 1),
            size_hint_y=None,
            height=dp(30)
        )
        
        scroll = ScrollView()
        self.photo_results_layout = BoxLayout(orientation='vertical', size_hint_y=None, spacing=5)
        self.photo_results_layout.bind(minimum_height=self.photo_results_layout.setter('height'))
        scroll.add_widget(self.photo_results_layout)
        
        layout.add_widget(header)
        layout.add_widget(photo_btn)
        layout.add_widget(info_label)
        layout.add_widget(results_label)
        layout.add_widget(scroll)
        
        screen.add_widget(layout)
        return screen
    
    def _update_bg(self, instance, value):
        """更新背景"""
        instance.bg.size = instance.size
        instance.bg.pos = instance.pos
    
    def select_food(self, food_name):
        """选择食物"""
        self.food_input.text = food_name
        if food_name in self.food_database:
            default_weight = self.food_database[food_name]['default_serving']
            self.weight_input.text = str(default_weight)
    
    def add_food_to_daily(self, instance):
        """添加食物到每日摄入"""
        food_name = self.food_input.text.strip()
        weight_text = self.weight_input.text.strip()
        
        if not food_name or not weight_text:
            return
        
        try:
            weight = float(weight_text)
        except ValueError:
            return
        
        # 计算卡路里
        if food_name in self.food_database:
            calories_per_100g = self.food_database[food_name]['calories_per_100g']
            total_calories = (calories_per_100g * weight) / 100
        else:
            # 默认估算值
            total_calories = weight * 1.5
        
        # 添加到今日记录
        food_record = {
            'name': food_name,
            'weight': weight,
            'calories': total_calories,
            'time': datetime.now().strftime('%H:%M')
        }
        
        self.daily_foods.append(food_record)
        self.daily_calories += total_calories
        
        # 更新显示
        self.update_stats_display()
        
        # 清空输入
        self.food_input.text = ''
        self.weight_input.text = ''
        
        # 返回主页
        self.go_to_main(instance)
    
    def simulate_photo_recognition(self, instance):
        """模拟拍照识别"""
        import random
        
        # 清空之前的结果
        self.photo_results_layout.clear_widgets()
        
        # 模拟识别结果
        sample_foods = [
            ('苹果', 150, 78),
            ('香蕉', 120, 107),
            ('米饭', 180, 234)
        ]
        
        # 随机选择1-3种食物
        recognized_foods = random.sample(sample_foods, random.randint(1, 3))
        
        total_calories = 0
        
        for food_name, weight, calories in recognized_foods:
            total_calories += calories
            
            # 创建识别结果项
            result_item = BoxLayout(
                orientation='horizontal',
                size_hint_y=None,
                height=dp(60),
                spacing=10
            )
            
            # 食物信息
            info_label = Label(
                text=f'{food_name} {weight}g - {calories:.0f}卡',
                font_size=sp(14),
                color=(0.2, 0.2, 0.2, 1)
            )
            
            # 添加按钮
            add_btn = Button(
                text='添加',
                size_hint_x=None,
                width=dp(60),
                font_size=sp(12),
                background_color=(0.2, 0.7, 0.2, 1)
            )
            add_btn.bind(on_press=lambda x, f=food_name, w=weight, c=calories: self.add_recognized_food(f, w, c))
            
            result_item.add_widget(info_label)
            result_item.add_widget(add_btn)
            
            self.photo_results_layout.add_widget(result_item)
        
        # 总计信息
        if recognized_foods:
            total_label = Label(
                text=f'识别到 {len(recognized_foods)} 种食物，总计 {total_calories:.0f} 卡路里',
                font_size=sp(16),
                color=(0.1, 0.6, 0.1, 1),
                size_hint_y=None,
                height=dp(40)
            )
            
            # 全部添加按钮
            add_all_btn = Button(
                text='添加所有食物',
                font_size=sp(14),
                size_hint_y=None,
                height=dp(50),
                background_color=(0.6, 0.2, 0.8, 1)
            )
            add_all_btn.bind(on_press=lambda x: self.add_all_recognized_foods(recognized_foods))
            
            self.photo_results_layout.add_widget(total_label)
            self.photo_results_layout.add_widget(add_all_btn)
    
    def add_recognized_food(self, food_name, weight, calories):
        """添加识别的食物"""
        food_record = {
            'name': food_name,
            'weight': weight,
            'calories': calories,
            'time': datetime.now().strftime('%H:%M')
        }
        
        self.daily_foods.append(food_record)
        self.daily_calories += calories
        self.update_stats_display()
    
    def add_all_recognized_foods(self, recognized_foods):
        """添加所有识别的食物"""
        for food_name, weight, calories in recognized_foods:
            self.add_recognized_food(food_name, weight, calories)
        
        # 返回主页
        self.go_to_main(None)
    
    def update_stats_display(self):
        """更新统计显示"""
        self.stats_label.text = f'今日摄入: {self.daily_calories:.0f} / {self.goal_calories} 卡路里'
    
    def update_history_display(self):
        """更新历史记录显示"""
        self.history_layout.clear_widgets()
        
        if not self.daily_foods:
            no_record = Label(
                text='今日暂无记录',
                font_size=sp(16),
                color=(0.5, 0.5, 0.5, 1),
                size_hint_y=None,
                height=dp(40)
            )
            self.history_layout.add_widget(no_record)
            return
        
        for food in self.daily_foods:
            item = Label(
                text=f'{food["time"]} - {food["name"]} {food["weight"]:.0f}g ({food["calories"]:.0f}卡)',
                font_size=sp(14),
                color=(0.2, 0.2, 0.2, 1),
                size_hint_y=None,
                height=dp(40)
            )
            self.history_layout.add_widget(item)
    
    # 导航方法
    def go_to_main(self, instance):
        self.screen_manager.current = 'main'
        self.update_stats_display()
    
    def go_to_add_food(self, instance):
        self.screen_manager.current = 'add_food'
    
    def go_to_history(self, instance):
        self.screen_manager.current = 'history'
        self.update_history_display()
    
    def go_to_photo(self, instance):
        self.screen_manager.current = 'photo'

if __name__ == '__main__':
    HealthApp().run()