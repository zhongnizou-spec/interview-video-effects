## 🎬 访谈视频特效处理系统
### Interview Video Effects Processor

根据访谈内容自动添加星露谷风格的视觉效果！

---

## 📺 项目说明

这个项目为 Mark 的矿业&葡萄酒访谈视频添加**轻盈、生动的星露谷画风视觉效果**，包括：

- ✨ 灵动的粒子效果
- 🌟 柔和的发光边框
- 🍇 角落装饰（藤蔓、叶子等）
- 📝 关键词指示器
- 🎨 根据内容智能调整色调

**核心特点：不遮挡原视频内容和字幕！**

---

## 🎯 视频内容结构

根据提供的信息：

| 时间段 | 内容 | 视觉效果 |
|------|------|--------|
| 0:00-1:00 | 开场：葡萄酒（农业）& 矿都有前景，缺人 | 🍇⛏️ 温暖色调粒子 |
| 1:00-2:40 | 这些职业都实践性很强，不能纸上谈兵 | 💪 强调效果 |
| 2:40+ | "天生我才必有用" - 激励主题 | ⭐ 星星爆裂效果 |

---

## 💻 使用方法

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置视频

编辑 `config.json`：

```json
{
  "input_video": "C:\\Users\\zoez\\OneDrive\\Desktop\\1.1 Mark's traineeship\\mark 采访\\5月27日(1).mp4",
  "output_video": "output_enhanced.mp4",
  "effect_preset": "light"
}
```

### 3. 运行脚本

```bash
python process_video.py
```

### 4. 享受结果！

输出文件：`output_enhanced.mp4`

---

## 📁 项目结构

```
interview-video-effects/
├── README.md                 # 本文件
├── requirements.txt          # 依赖
├── config.json              # 配置文件
├── process_video.py         # 主处理脚本
├── effects.py               # 效果模块
└── keywords.json            # 关键词映射表
```

---

## 🎨 视觉效果详解

### 葡萄酒主题（0:00-1:00）
- 颜色：紫色 (128, 0, 128) + 绿色 (100, 150, 100)
- 效果：柔和粒子 + 角落藤蔓
- 不透明度：15-25%

### 矿业主题（1:00+）
- 颜色：银灰色 (192, 192, 192)
- 效果：闪烁粒子 + 金色边框
- 不透明度：20-30%

### 激励主题（2:40+）
- 颜色：金色 (255, 215, 0)
- 效果：星星爆裂 + 脉冲发光
- 不透明度：25-35%

---

## ⚙️ 高级配置

编辑 `keywords.json` 自定义效果：

```json
{
  "segments": [
    {
      "start": 0,
      "end": 60,
      "theme": "wine_agriculture",
      "primary_color": [128, 0, 128],
      "secondary_color": [100, 150, 100],
      "effects": ["particles", "corner_vine"],
      "opacity": 0.2
    }
  ]
}
```

---

## 📊 性能说明

- **处理时间**：取决于视频长度和电脑配置
  - 10分钟视频：约 5-15 分钟
  - 30分钟视频：约 15-45 分钟
  
- **输出质量**：1080p 或原分辨率（默认 24fps）

- **所需空间**：约为原视频的 1.5-2 倍

---

## 🐛 故障排除

### 问题：找不到视频文件
- 检查 `config.json` 中的路径是否正确
- Windows 路径使用反斜杠 `\\` 或双斜杠 `/`

### 问题：处理速度很慢
- 降低分辨率：编辑 `process_video.py` 中的 `fps` 参数
- 关闭其他应用释放内存

### 问题：输出视频没有音频
- 确保原视频有音频轨道
- 检查是否启用了音频编码（`codec='aac'`）

---

## 📝 License

MIT License - 自由使用和修改

---

## 👨‍💻 关于

由 GitHub Copilot 为 Mark 的访谈项目创建

**需要调整？**
- 编辑 `config.json` 来自定义效果
- 修改 `keywords.json` 来调整时间段
- 调整 `effects.py` 来创建新效果