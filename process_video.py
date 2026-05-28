#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
访谈视频特效处理主程序
Interview Video Effects Processor - Main Script
"""

import json
import os
import sys
from pathlib import Path
from moviepy.editor import VideoFileClip, CompositeVideoClip
from effects import (
    create_floating_particles,
    create_edge_glow,
    create_corner_decoration,
    create_star_burst,
    create_pulse_glow
)


def load_config(config_file="config.json"):
    """加载配置文件"""
    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"❌ 找不到配置文件: {config_file}")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"❌ 配置文件格式错误: {config_file}")
        sys.exit(1)


def load_keywords(keywords_file="keywords.json"):
    """加载关键词和时间段配置"""
    try:
        with open(keywords_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"⚠️  找不到关键词文件: {keywords_file}，使用默认配置")
        return {}


def check_video_file(video_path):
    """检查视频文件是否存在"""
    if not os.path.exists(video_path):
        print(f"❌ 视频文件不存在: {video_path}")
        return False
    
    print(f"✅ 找到视频文件: {video_path}")
    return True


def process_video(config, keywords_data):
    """处理视频并添加效果"""
    
    input_path = config["input_video"]
    output_path = config["output_video"]
    effect_preset_name = config.get("effect_preset", "light")
    
    # 检查视频文件
    if not check_video_file(input_path):
        return False
    
    print(f"\n📹 加载视频...")
    try:
        video = VideoFileClip(input_path)
        print(f"✅ 视频已加载")
        print(f"   分辨率: {video.size}")
        print(f"   时长: {video.duration:.2f} 秒 ({int(video.duration // 60)}m {int(video.duration % 60)}s)")
        print(f"   FPS: {video.fps}")
    except Exception as e:
        print(f"❌ 无法加载视频: {e}")
        return False
    
    # 获取效果预设
    effect_preset = keywords_data.get("effect_presets", {}).get(effect_preset_name, {})
    print(f"\n🎨 使用效果预设: {effect_preset_name}")
    
    # 获取时间段配置
    segments = keywords_data.get("segments", [])
    
    if not segments:
        print(f"⚠️  没有定义时间段，使用原视频")
        try:
            video.write_videofile(
                output_path,
                fps=config.get("fps", 24),
                codec=config.get("codec", "libx264"),
                audio_codec=config.get("audio_codec", "aac"),
                verbose=config.get("processing", {}).get("verbose", True)
            )
            print(f"✅ 视频已保存: {output_path}")
            return True
        except Exception as e:
            print(f"❌ 保存视频失败: {e}")
            return False
    
    # 处理各个时间段
    print(f"\n⚙️  处理 {len(segments)} 个时间段...")
    
    # 创建效果层列表
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
        
        print(f"\n  ➜ {segment.get('name', 'Unnamed')}")
        print(f"     时间: {start}s - {end}s")
        print(f"     效果: {', '.join(effects_list)}")
        
        for effect in effects_list:
            if effect == "particles":
                clip = create_floating_particles(
                    duration=duration,
                    color=primary_color,
                    opacity=effect_preset.get("particle_opacity", 0.2),
                    particle_count=effect_preset.get("particle_count", 12)
                ).set_start(start)
                effect_clips.append(clip)
            
            elif effect == "sparkle_particles":
                clip = create_floating_particles(
                    duration=duration,
                    color=secondary_color,
                    opacity=effect_preset.get("particle_opacity", 0.25),
                    particle_count=effect_preset.get("particle_count", 15)
                ).set_start(start)
                effect_clips.append(clip)
            
            elif effect == "edge_glow":
                clip = create_edge_glow(
                    duration=duration,
                    color=secondary_color,
                    opacity=effect_preset.get("edge_glow_opacity", 0.15)
                ).set_start(start)
                effect_clips.append(clip)
            
            elif effect == "corner_vine":
                for corner in ["top_left", "bottom_right"]:
                    clip = create_corner_decoration(
                        duration=duration,
                        corner=corner,
                        decoration_type="vine",
                        color=primary_color
                    ).set_start(start)
                    effect_clips.append(clip)
            
            elif effect == "star_burst":
                clip = create_star_burst(
                    duration=2,
                    color=primary_color
                ).set_start(start + duration / 2)
                effect_clips.append(clip)
            
            elif effect == "pulse_glow":
                clip = create_pulse_glow(
                    duration=duration,
                    color=primary_color,
                    opacity=opacity * 0.7
                ).set_start(start)
                effect_clips.append(clip)
    
    # 合成：原视频 + 所有效果层
    print(f"\n🔗 合并效果层...")
    try:
        final_video = CompositeVideoClip([video] + effect_clips, size=video.size)
        final_video = final_video.set_audio(video.audio)
    except Exception as e:
        print(f"❌ 合并视频失败: {e}")
        return False
    
    # 导出最终视频
    print(f"\n💾 导出视频...")
    try:
        final_video.write_videofile(
            output_path,
            fps=config.get("fps", 24),
            codec=config.get("codec", "libx264"),
            audio_codec=config.get("audio_codec", "aac"),
            verbose=config.get("processing", {}).get("verbose", True),
            threads=config.get("processing", {}).get("threads", 4)
        )
        print(f"✅ 视频已成功保存: {output_path}")
        return True
    except Exception as e:
        print(f"❌ 导出视频失败: {e}")
        return False


def main():
    """主函数"""
    print("=" * 60)
    print("🎬 访谈视频特效处理系统")
    print("   Interview Video Effects Processor")
    print("=" * 60)
    
    # 加载配置
    print("\n📋 加载配置...")
    config = load_config("config.json")
    keywords_data = load_keywords("keywords.json")
    
    # 处理视频
    success = process_video(config, keywords_data)
    
    if success:
        print("\n" + "=" * 60)
        print("✨ 处理完成！享受你的视频吧 ✨")
        print("=" * 60)
    else:
        print("\n" + "=" * 60)
        print("❌ 处理失败，请检查错误信息")
        print("=" * 60)
        sys.exit(1)


if __name__ == "__main__":
    main()
