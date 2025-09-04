[app]

# 应用基本信息
title = 健康卡路里计算
package.name = healthcalorie
package.domain = org.healthapp.calorie

# 应用源码路径
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json,txt

# 应用版本
version = 1.0

# 应用需求 - 云端构建优化版本
requirements = python3,kivy==2.1.0,requests==2.31.0,pillow==10.0.0,plyer

# 主程序文件
main.py = final_app.py

# 应用权限
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE,CAMERA

# Android 配置 - 云端构建优化
android.api = 30
android.minapi = 21
android.ndk = 21b
android.accept_sdk_license = True

# Android 架构 - 优化构建时间
android.archs = arm64-v8a

# 包含的包
android.add_python_to_path = True

# Android 入口点
android.entrypoint = org.kivy.android.PythonActivity

# P4A 配置
p4a.branch = master
p4a.bootstrap = sdl2

# 优化构建速度
android.gradle_dependencies = 

[buildozer]

# 构建目录
build_dir = ./.buildozer
bin_dir = ./bin

# 日志级别 - 云端构建使用详细日志
log_level = 2

# 使用颜色输出
warn_on_root = 0