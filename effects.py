"""
星露谷风格视觉效果模块
Stardew Valley Style Visual Effects Module
"""

import numpy as np
import math
from moviepy.editor import VideoClip, ImageClip
from PIL import Image, ImageDraw


def create_floating_particles(duration=3, particle_type="sparkle", 
                             color=(255, 215, 0), opacity=0.3, 
                             avoid_center=True, particle_count=12):
    """
    创建轻盈的飘浮粒子效果
    Create floating particle effects that don't obstruct content
    
    Args:
        duration: 效果持续时间（秒）
        particle_type: 粒子类型 ("sparkle", "star", "leaf")
        color: RGB 颜色元组
        opacity: 不透明度 (0-1)
        avoid_center: 是否避免中心区域
        particle_count: 粒子数量
    """
    
    def make_frame(t):
        frame = np.zeros((720, 1280, 4), dtype=np.uint8)
        
        for i in range(particle_count):
            # 计算粒子位置
            if avoid_center:
                # 边缘位置
                edge_choice = i % 4
                if edge_choice == 0:  # 上方
                    x = 200 + i * 80 + 50 * math.sin(t * 2 + i)
                    y = 50 + 30 * math.sin(t * 1.5 + i * 0.5)
                elif edge_choice == 1:  # 下方
                    x = 200 + i * 80 + 50 * math.sin(t * 2 + i)
                    y = 650 + 30 * math.sin(t * 1.5 + i * 0.5)
                elif edge_choice == 2:  # 左方
                    x = 50 + 30 * math.sin(t * 1.5 + i * 0.5)
                    y = 150 + i * 60 + 50 * math.sin(t * 2 + i)
                else:  # 右方
                    x = 1230 + 30 * math.sin(t * 1.5 + i * 0.5)
                    y = 150 + i * 60 + 50 * math.sin(t * 2 + i)
            else:
                x = 640 + 400 * math.sin(t * 2 + i)
                y = 360 + 200 * math.cos(t * 1.5 + i)
            
            # 粒子大小随时间变化
            size = 2 + 2 * math.sin(t * 3 + i)
            
            # 防止越界
            if 0 <= int(x) < 1280 and 0 <= int(y) < 720:
                y_min = max(0, int(y) - int(size))
                y_max = min(720, int(y) + int(size))
                x_min = max(0, int(x) - int(size))
                x_max = min(1280, int(x) + int(size))
                
                # 绘制半透明粒子
                alpha = int(200 * opacity)
                frame[y_min:y_max, x_min:x_max] = list(color) + [alpha]
        
        return frame
    
    return VideoClip(make_frame, duration=duration)


def create_edge_glow(duration=3, color=(255, 215, 0), opacity=0.2, thickness=20):
    """
    创建边框柔和发光效果
    Create edge glow effect that frames the video
    
    Args:
        duration: 效果持续时间（秒）
        color: RGB 颜色
        opacity: 不透明度
        thickness: 边框厚度
    """
    
    def make_frame(t):
        frame = np.zeros((720, 1280, 4), dtype=np.uint8)
        
        # 脉冲效果：随时间变化的强度
        glow_intensity = int(200 * (0.5 + 0.5 * math.sin(t * 2)))
        alpha = int(glow_intensity * opacity)
        
        # 绘制四个边框
        frame[0:thickness, :] = list(color) + [alpha]  # 上
        frame[720-thickness:720, :] = list(color) + [alpha]  # 下
        frame[:, 0:thickness] = list(color) + [alpha]  # 左
        frame[:, 1280-thickness:1280] = list(color) + [alpha]  # 右
        
        return frame
    
    return VideoClip(make_frame, duration=duration)


def create_corner_decoration(duration=3, corner="top_left", 
                            decoration_type="vine", color=(100, 150, 100)):
    """
    在角落添加轻盈装饰
    Add decorative elements in corners
    
    Args:
        duration: 持续时间
        corner: 角落位置 ("top_left", "top_right", "bottom_left", "bottom_right")
        decoration_type: 装饰类型 ("vine", "leaves", "flowers")
        color: RGB 颜色
    """
    
    def make_frame(t):
        frame = np.zeros((720, 1280, 4), dtype=np.uint8)
        
        if decoration_type == "vine":
            # 绘制藤蔓效果
            points = []
            for i in range(25):
                y = i * 25
                x = 30 + 15 * math.sin(t * 0.5 + i * 0.3)
                points.append([x, y])
            
            # 根据角落位置调整
            if corner == "top_left":
                for j in range(len(points) - 1):
                    x1, y1 = points[j]
                    x2, y2 = points[j + 1]
                    if 0 <= int(y2) < 720 and 0 <= int(x2) < 100:
                        frame[int(y2)-1:int(y2)+2, int(x2)-1:int(x2)+2] = list(color) + [120]
            
            elif corner == "top_right":
                for j in range(len(points) - 1):
                    x2 = 1280 - 30 - 15 * math.sin(t * 0.5 + j * 0.3)
                    y2 = j * 25
                    if 0 <= int(y2) < 720 and 1180 <= int(x2) < 1280:
                        frame[int(y2)-1:int(y2)+2, int(x2)-1:int(x2)+2] = list(color) + [120]
            
            elif corner == "bottom_left":
                for j in range(len(points) - 1):
                    x1, y1 = points[j]
                    y2 = 720 - j * 25
                    if 0 <= int(y2) < 720 and 0 <= int(x1) < 100:
                        frame[int(y2)-1:int(y2)+2, int(x1)-1:int(x1)+2] = list(color) + [120]
            
            elif corner == "bottom_right":
                for j in range(len(points) - 1):
                    x2 = 1280 - 30 - 15 * math.sin(t * 0.5 + j * 0.3)
                    y2 = 720 - j * 25
                    if 0 <= int(y2) < 720 and 1180 <= int(x2) < 1280:
                        frame[int(y2)-1:int(y2)+2, int(x2)-1:int(x2)+2] = list(color) + [120]
        
        return frame
    
    return VideoClip(make_frame, duration=duration)


def create_star_burst(duration=2, color=(255, 215, 0), center=(640, 360)):
    """
    创建星星爆裂效果（激励时刻）
    Create star burst effect for inspiring moments
    
    Args:
        duration: 持续时间
        color: RGB 颜色
        center: 爆裂中心位置
    """
    
    def make_frame(t):
        frame = np.zeros((720, 1280, 4), dtype=np.uint8)
        
        num_stars = 20
        for i in range(num_stars):
            # 星星从中心向外扩散
            angle = (i / num_stars) * 2 * math.pi
            distance = 50 + t * 200  # 随时间增加距离
            
            x = center[0] + distance * math.cos(angle)
            y = center[1] + distance * math.sin(angle)
            
            # 星星大小随时间递减
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
    """
    创建脉冲发光效果
    Create pulsing glow effect
    
    Args:
        duration: 持续时间
        color: RGB 颜色
        opacity: 基础不透明度
        intensity: 强度倍数
    """
    
    def make_frame(t):
        frame = np.zeros((720, 1280, 4), dtype=np.uint8)
        
        # 脉冲强度
        pulse = 0.5 + 0.5 * math.sin(t * 3)
        
        # 填充整个帧（很淡的层）
        alpha = int(150 * opacity * pulse * intensity)
        frame[:, :] = list(color) + [alpha]
        
        return frame
    
    return VideoClip(make_frame, duration=duration)


def create_subtle_indicator(duration=2, position="bottom_center", 
                           color=(255, 215, 0), text="✨"):
    """
    创建微妙的指示器
    Create subtle text indicator
    
    Args:
        duration: 持续时间
        position: 位置
        color: RGB 颜色
        text: 显示文字
    """
    
    # 创建文字图像
    img = Image.new('RGBA', (1280, 100), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    text_color = tuple(list(color) + [150])
    
    if position == "bottom_center":
        draw.text((600, 40), text, fill=text_color)
    elif position == "top_right":
        draw.text((1100, 20), text, fill=text_color)
    
    def make_frame(t):
        frame = np.array(img)
        # 脉冲效果
        alpha = frame[:, :, 3].astype(float) * (0.5 + 0.5 * math.sin(t * 3))
        frame[:, :, 3] = alpha.astype(np.uint8)
        return frame
    
    clip = VideoClip(make_frame, duration=duration)
    
    if position == "bottom_center":
        clip = clip.set_position(("center", "bottom"))
    elif position == "top_right":
        clip = clip.set_position(("right", "top"))
    
    return clip
