# Qwen3-TTS Skill

## 📝 简介

Qwen3-TTS 是阿里开源的高质量文本转语音模型，支持情感控制和语音克隆。

## ✨ 功能特点

- 🎨 **情感控制**：用自然语言描述想要的语气（"沉稳男声"、"温柔女声"等）
- 🎤 **语音克隆**：仅需极短参考音频即可复刻音色
- 🌍 **多语言支持**：10 种主要语言
- 💾 **完全离线**：无需网络，数据隐私有保障
- ⚡ **性能良好**：CPU 版本 10-15 秒生成

## 🚀 快速开始

### 基本用法

```bash
# 生成语音（默认 Uncle_Fu 沉稳男声）
qwen-tts "静夜思 - 李白。床前明月光，疑是地上霜。举头望明月，低头思故乡。"

# 指定输出文件
qwen-tts "你的文本" -o output.mp3

# 指定声音
qwen-tts "你的文本" -s Vivian

# 指定情感
qwen-tts "你的文本" -i "用温柔的语气说"
```

### 可用声音

| 声音 ID | 描述 | 适用场景 |
|--------|------|---------|
| `Uncle_Fu` | 沉稳男声 | 古诗朗读、正式场合 |
| `Vivian` | 女声 | 日常对话、故事讲述 |
| `Michelle` | 女声（温柔） | 哄睡、安慰 |
| `Eric` | 男声（年轻） | 活泼场景 |

### 参数说明

```
-q, --quiet      静默模式（不输出日志）
-o, --output     输出文件路径（默认：data/tts_output.mp3）
-s, --speaker    声音 ID（默认：Uncle_Fu）
-i, --instruct   情感指令（自然语言描述）
-l, --language   语言（默认：Chinese）
--no-silence     不添加尾部静音
```

## 📊 性能对比

| 方案 | 生成时间 | 质量 | 情感控制 | 推荐度 |
|-----|---------|------|---------|--------|
| **Edge-TTS** | 2-3 秒 | ⭐⭐⭐⭐ | ❌ 有限 | ⭐⭐⭐⭐⭐ |
| **Qwen3-TTS (CPU)** | 10-15 秒 | ⭐⭐⭐⭐⭐ | ✅ **最强** | ⭐⭐⭐⭐ |

## 💡 使用场景

### 1. 古诗朗读
```bash
qwen-tts "静夜思 - 李白。床前明月光，疑是地上霜。举头望明月，低头思故乡。" -s Uncle_Fu -i "用沉稳、富有感情的语气朗读古诗"
```

### 2. 故事讲述
```bash
qwen-tts "从前有座山，山里有座庙..." -s Vivian -i "用讲故事给小孩听的语气"
```

### 3. 通知播报
```bash
qwen-tts "今天天气晴朗，温度25度，适合外出。" -s Michelle
```

## ⚙️ 技术细节

### 模型信息
- **模型**：Qwen3-TTS-12Hz-1.7B-CustomVoice
- **大小**：3.6GB
- **路径**：`~/.openclaw/workspace/models/Qwen3-TTS-12Hz-1.7B-CustomVoice`
- **运行方式**：PyTorch CPU

### 优化说明
- ✅ **自动添加 0.5 秒尾部静音**（避免最后一个字截断）
- ✅ **预设优化参数**（temperature=0.8, repetition_penalty=1.1）
- ✅ **统一输出路径**（data/tts_*.mp3）

### 已测试但失败的优化
- ❌ **OpenVINO 优化**：52 秒（比 PyTorch 更慢）
- 💡 **未来优化**：GPU、ONNX Runtime、INT8 量化

## 📂 文件结构

```
skills/qwen3-tts/
├── SKILL.md              # 本文档
├── scripts/
│   ├── tts.py           # 主脚本
│   └── qwen-tts         # 便捷调用脚本
└── references/
    └── voices.md        # 声音列表和参数
```

## 🔗 相关链接

- [Qwen3-TTS GitHub](https://github.com/QwenLM/Qwen3-TTS)
- [ModelScope 模型](https://modelscope.cn/collections/Qwen/Qwen3-TTS)
- [Hugging Face 模型](https://huggingface.co/Qwen/Qwen3-TTS-12Hz-1.7B-CustomVoice)

---

*最后更新：2026-03-11*
