"""
Google Colab 版本 - 访谈视频特效处理
Interview Video Effects Processor for Google Colab
无需本地 Python，在云端运行！
"""

# ============================================================
# 【第1步】安装依赖（Colab 会自动运行）
# ============================================================

import subprocess
import sys

print("📦 安装依赖中...")
subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", 
                       "moviepy", "opencv-python", "Pillow", "numpy", "imageio", "imageio-ffmpeg"])
print("✅ 依赖安装完成！\n")

# ============================================================
# 【第2步】导入库
# ============================================================

import json
import os
import math
import numpy as np
from pathlib import Path
from moviepy.editor import VideoFileClip, CompositeVideoClip, VideoClip
from PIL import Image, ImageDraw

print("✅ 库导入完成！\n")

# ============================================================
# 【第3步】连接 Google Drive（可选但推荐）
# ============================================================

from google.colab import drive
from google.colab import files

print("=" * 60)
print("📁 连接 Google Drive")
print("=" * 60)
print("\n选择上传方式:")
print("1️⃣  上传到 Google Drive（推荐）")
print("2️⃣  直接上传到 Colab（适合小文件）")
print("\n如果选择 1️⃣ ，请先运行这个命令：")
print("drive.mount('/content/drive')")
print("\n或者直接运行下面的代码上传视频...\n")

# ============================================================
# 【第4步】上传视频文件
# ============================================================

print("=" * 60)
print("🎬 上传视频文件")
print("=" * 60)
print("\n点击下面的【选择文件】按钮上传你的视频：\n")

uploaded = files.upload()

if uploaded:
    video_file = list(uploaded.keys())[0]
    video_path = f"/content/{video_file}"
    print(f"\n✅ 视频已上传: {video_file}")
    print(f"   路径: {video_path}")
else:
    print("❌ 没有上传文件")
    exit()

# ============================================================
# 【第5步】定义视觉效果函数
# ============================================================

print("\n" + "=" * 60)
print("🎨 定义视觉效果")
print("=" * 60 + "\n")

def create_floating_particles(duration=3, color=(255, 215, 0), opacity=0.3, 
                             avoid_center=True, particle_count=12):
    """创建浮动粒子效果"""
    def make_frame(t):
        frame = np.zeros((720, 1280, 4), dtype=np.uint8)
        
        for i in range(particle_count):
            if avoid_center:
                edge_choice = i % 4
                if edge_choice == 0:
                    x = 200 + i * 80 + 50 * math.sin(t * 2 + i)
                    y = 50 + 30 * math.sin(t * 1.5 + i * 0.5)
                elif edge_choice == 1:
                    x = 200 + i * 80 + 50 * math.sin(t * 2 + i)
                    y = 650 + 30 * math.sin(t * 1.5 + i * 0.5)
                elif edge_choice == 2:
                    x = 50 + 30 * math.sin(t * 1.5 + i * 0.5)
                    y = 150 + i * 60 + 50 * math.sin(t * 2 + i)
                else:
                    x = 1230 + 30 * math.sin(t * 1.5 + i * 0.5)
                    y = 150 + i * 60 + 50 * math.sin(t * 2 + i)
            else:
                x = 640 + 400 * math.sin(t * 2 + i)
                y = 360 + 200 * math.cos(t * 1.5 + i)
            
            size = 2 + 2 * math.sin(t * 3 + i)
            
            if 0 <= int(x) < 1280 and 0 <= int(y) < 720:
                y_min = max(0, int(y) - int(size))
                y_max = min(720, int(y) + int(size))
                x_min = max(0, int(x) - int(size))
                x_max = min(1280, int(x) + int(size))
                
                alpha = int(200 * opacity)
                frame[y_min:y_max, x_min:x_max] = list(color) + [alpha]
        
        return frame
    
    return VideoClip(make_frame, duration=duration)


def create_edge_glow(duration=3, color=(255, 215, 0), opacity=0.2, thickness=20):
    """创建边框发光效果"""
    def make_frame(t):
        frame = np.zeros((720, 1280, 4), dtype=np.uint8)
        glow_intensity = int(200 * (0.5 + 0.5 * math.sin(t * 2)))
        alpha = int(glow_intensity * opacity)
        
        frame[0:thickness, :] = list(color) + [alpha]
        frame[720-thickness:720, :] = list(color) + [alpha]
        frame[:, 0:thickness] = list(color) + [alpha]
        frame[:, 1280-thickness:1280] = list(color) + [alpha]
        
        return frame
    
    return VideoClip(make_frame, duration=duration)


def create_corner_decoration(duration=3, corner="top_left", color=(100, 150, 100)):
    """创建角落装饰"""
    def make_frame(t):
        frame = np.zeros((720, 1280, 4), dtype=np.uint8)
        
        points = []
        for i in range(25):
            y = i * 25
            x = 30 + 15 * math.sin(t * 0.5 + i * 0.3)
            points.append([x, y])
        
        if corner == "top_left":
            for j in range(len(points) - 1):
                x1, y1 = points[j]
                x2, y2 = points[j + 1]
                if 0 <= int(y2) < 720 and 0 <= int(x2) < 100:
                    frame[int(y2)-1:int(y2)+2, int(x2)-1:int(x2)+2] = list(color) + [120]
        
        return frame
    
    return VideoClip(make_frame, duration=duration)


def create_star_burst(duration=2, color=(255, 215, 0), center=(640, 360)):
    """创建星星爆裂效果"""
    def make_frame(t):
        frame = np.zeros((720, 1280, 4), dtype=np.uint8)
        
        num_stars = 20
        for i in range(num_stars):
            angle = (i / num_stars) * 2 * math.pi
            distance = 50 + t * 200
            
            x = center[0] + distance * math.cos(angle)
            y = center[1] + distance * math.sin(angle)
            
            size = 3 * (1 - t / duration)
            
            if 0 <= int(x) < 1280 and 0 <= int(y) < 720 and t < duration:
                y_min = max(0, int(y) - int(size))
                y_max = min(720, int(y) + int(size))
                x_min = max(0, int(x) - int(size))
                x_max = min(1280, int(x) + int(size))
                
                alpha = int(200 * (1 - t / duration))
                frame[y_min:y_max, x_min:x_max] = list(color) + [alpha]
        
        return frame
    
    return VideoClip(make_frame, duration=duration)


def create_pulse_glow(duration=3, color=(255, 215, 0), opacity=0.2, intensity=1.0):
    """创建脉冲发光效果"""
    def make_frame(t):
        frame = np.zeros((720, 1280, 4), dtype=np.uint8)
        pulse = 0.5 + 0.5 * math.sin(t * 3)
        alpha = int(150 * opacity * pulse * intensity)
        frame[:, :] = list(color) + [alpha]
        return frame
    
    return VideoClip(make_frame, duration=duration)

print("✅ 视觉效果函数定义完成！")

# ============================================================
# 【第6步】配置参数
# ============================================================

print("\n" + "=" * 60)
print("⚙️  配置参数")
print("=" * 60 + "\n")

# 时间段和效果配置
segments = [
    {
        "start": 0,
        "end": 60,
        "name": "开场：葡萄酒与矿业前景",
        "primary_color": [128, 0, 128],
        "secondary_color": [100, 150, 100],
        "effects": ["particles", "corner_vine", "edge_glow"],
        "opacity": 0.2
    },
    {
        "start": 60,
        "end": 160,
        "name": "实践性很强，不能纸上谈兵",
        "primary_color": [192, 192, 192],
        "secondary_color": [255, 215, 0],
        "effects": ["sparkle_particles", "edge_glow"],
        "opacity": 0.25
    },
    {
        "start": 160,
        "end": -1,
        "name": "天生我才必有用 - 激励主题",
        "primary_color": [255, 215, 0],
        "secondary_color": [255, 255, 150],
        "effects": ["star_burst", "pulse_glow", "particles"],
        "opacity": 0.3
    }
]

effect_preset = {
    "particle_opacity": 0.15,
    "edge_glow_opacity": 0.1,
    "particle_count": 12
}

print(f"✅ 配置完成！共 {len(segments)} 个时间段")

# ============================================================
# 【第7步】加载并处理视频
# ============================================================

print("\n" + "=" * 60)
print("🎬 处理视频中...")
print("=" * 60 + "\n")

try:
    print(f"📹 加载视频: {video_path}")
    video = VideoFileClip(video_path)
    print(f"✅ 视频已加载")
    print(f"   分辨率: {video.size}")
    print(f"   时长: {video.duration:.2f} 秒")
    print(f"   FPS: {video.fps}\n")
    
    # 创建效果层
    effect_clips = []
    
    for segment in segments:
        start = segment.get("start", 0)
        end = segment.get("end", video.duration)
        if end == -1 or end > video.duration:
            end = video.duration
        
        duration = end - start
        effects_list = segment.get("effects", [])
        primary_color = tuple(segment.get("primary_color", [255, 215, 0]))
        secondary_color = tuple(segment.get("secondary_color", [255, 255, 150]))
        opacity = segment.get("opacity", 0.25)
        
        print(f"  ➜ {segment.get('name')}")
        print(f"     时间: {start}s - {end}s")
        
        for effect in effects_list:
            if effect == "particles":
                clip = create_floating_particles(
                    duration=duration,
                    color=primary_color,
                    opacity=effect_preset.get("particle_opacity", 0.2),
                    particle_count=effect_preset.get("particle_count", 12)
                ).set_start(start)
                effect_clips.append(clip)
                print(f"     ✓ 粒子效果")
            
            elif effect == "sparkle_particles":
                clip = create_floating_particles(
                    duration=duration,
                    color=secondary_color,
                    opacity=effect_preset.get("particle_opacity", 0.25),
                    particle_count=effect_preset.get("particle_count", 15)
                ).set_start(start)
                effect_clips.append(clip)
                print(f"     ✓ 闪烁粒子")
            
            elif effect == "edge_glow":
                clip = create_edge_glow(
                    duration=duration,
                    color=secondary_color,
                    opacity=effect_preset.get("edge_glow_opacity", 0.15)
                ).set_start(start)
                effect_clips.append(clip)
                print(f"     ✓ 发光边框")
            
            elif effect == "corner_vine":
                clip = create_corner_decoration(
                    duration=duration,
                    corner="top_left",
                    color=primary_color
                ).set_start(start)
                effect_clips.append(clip)
                print(f"     ✓ 角落装饰")
            
            elif effect == "star_burst":
                clip = create_star_burst(
                    duration=2,
                    color=primary_color
                ).set_start(start + duration / 2)
                effect_clips.append(clip)
                print(f"     ✓ 星爆效果")
            
            elif effect == "pulse_glow":
                clip = create_pulse_glow(
                    duration=duration,
                    color=primary_color,
                    opacity=opacity * 0.7
                ).set_start(start)
                effect_clips.append(clip)
                print(f"     ✓ 脉冲效果")
        
        print()
    
    # 合成视频
    print("🔗 合并效果层...")
    final_video = CompositeVideoClip([video] + effect_clips, size=video.size)
    final_video = final_video.set_audio(video.audio)
    print("✅ 合并完成！\n")
    
    # 导出视频
    print("💾 导出视频中（这可能需要几分钟）...")
    output_path = "/content/output_enhanced.mp4"
    
    final_video.write_videofile(
        output_path,
        fps=24,
        codec="libx264",
        audio_codec="aac",
        verbose=False,
        logger=None
    )
    
    print(f"\n✅ 视频已成功保存！")
    print(f"   输出文件: {output_path}")
    
except Exception as e:
    print(f"\n❌ 处理失败: {e}")
    import traceback
    traceback.print_exc()

# ============================================================
# 【第8步】下载处理好的视频
# ============================================================

print("\n" + "=" * 60)
print("📥 下载处理后的视频")
print("=" * 60 + "\n")

print("点击下面的链接或按钮下载你的视频：\n")

try:
    files.download('/content/output_enhanced.mp4')
    print("\n✅ 下载开始！")
except:
    print("\n💡 如果下载没有自动开始，运行这个命令：")
    print("files.download('/content/output_enhanced.mp4')")

print("\n" + "=" * 60)
print("✨ 处理完成！享受你的视频吧 ✨")
print("=" * 60)
