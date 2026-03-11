# Qwen3-TTS Skill

**高质量中文 TTS，支持情感控制**

[![GitHub](https://img.shields.io/badge/GitHub-bbJose%2Fqwen3--tts--skill-blue)](https://github.com/bbJose/qwen3-tts-skill)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

---

## 📖 目录

- [特性](#特性)
- [性能对比](#性能对比)
- [完整部署指南](#完整部署指南)
- [踩坑记录](#踩坑记录)
- [使用方法](#使用方法)
- [声音列表](#声音列表)
- [常见问题](#常见问题)

---

## 特性

- ✅ **高质量中文语音**：标准普通话，无口音
- ✅ **情感控制**：通过自然语言描述控制语气
- ✅ **模型缓存**：首次加载后自动缓存，加快后续速度
- ✅ **便捷命令**：全局可用 `qwen-tts` 命令
- ✅ **CPU 友好**：无需 GPU，10-15 秒生成

---

## 性能对比

| 方案 | 速度 | 质量 | 情感控制 | 成本 | 推荐度 |
|-----|------|------|---------|------|--------|
| **Edge-TTS** | 2-3 秒 | ⭐⭐⭐⭐ | ❌ 有限 | 免费 | ⭐⭐⭐⭐⭐（快速）|
| **Qwen3-TTS (PyTorch CPU)** | 10-15 秒 | ⭐⭐⭐⭐⭐ | ✅ **最强** | 免费 | ⭐⭐⭐⭐（高质量）|
| **Qwen3-TTS (OpenVINO CPU)** | 52 秒 | ⭐⭐⭐⭐⭐ | ✅ 最强 | 免费 | ❌ **不推荐** |
| **Kokoro TTS** | 5-10 秒 | ⭐⭐⭐ | ❌ 有限 | 免费 | ⭐⭐（有口音）|

**结论**：
- 快速需求 → **Edge-TTS**
- 高质量需求 → **Qwen3-TTS (PyTorch CPU)**
- ❌ **不要用 OpenVINO**（性能下降 3-5 倍）

---

## 完整部署指南

### 1️⃣ 环境要求

**硬件：**
- CPU：任意（推荐 4 核以上）
- 内存：至少 8GB（模型加载需要 ~4GB）
- 硬盘：至少 5GB（模型 3.6GB + 依赖）
- GPU：**不需要**

**软件：**
- Python 3.8+
- pip

---

### 2️⃣ 安装依赖

```bash
# 创建虚拟环境（可选）
python3 -m venv qwen-tts-env
source qwen-tts-env/bin/activate

# 安装核心依赖
pip install torch torchaudio --index-url https://download.pytorch.org/whl/cpu
pip install qwen-tts
pip install soundfile numpy

# 验证安装
python3 -c "from qwen_tts import Qwen3TTSModel; print('✅ 安装成功')"
```

**⚠️ 注意：**
- 如果看到 `flash-attn is not installed` 警告，**可以忽略**
- CPU 版本不需要 flash-attn（只用于 GPU 加速）

---

### 3️⃣ 下载模型

**方式 1：自动下载（推荐）**

首次运行时自动下载（约 3.6GB，需要 1-2 分钟）：

```bash
python3 scripts/tts.py "测试文本"
```

**方式 2：手动下载**

```bash
# 使用 huggingface-cli
pip install huggingface-hub
huggingface-cli download Qwen/Qwen3-TTS-12Hz-1.7B-CustomVoice \
  --local-dir ~/.openclaw/workspace/models/Qwen3-TTS-12Hz-1.7B-CustomVoice
```

**模型位置：**
- 默认：`~/.openclaw/workspace/models/Qwen3-TTS-12Hz-1.7B-CustomVoice`
- 可在 `scripts/tts.py` 中修改 `DEFAULT_MODEL_PATH`

---

### 4️⃣ 安装 Skill

```bash
# 克隆仓库
git clone https://github.com/bbJose/qwen3-tts-skill.git
cd qwen3-tts-skill

# 添加全局命令（可选）
sudo ln -s $(pwd)/scripts/qwen-tts /usr/local/bin/qwen-tts

# 验证
qwen-tts --help
```

---

### 5️⃣ 测试运行

```bash
# 基本测试
qwen-tts "静夜思 - 李白。床前明月光，疑是地上霜。举头望明月，低头思故乡。"

# 查看生成的文件
ls -lh ~/.openclaw/workspace/data/tts_*.mp3
```

**预期输出：**
```
正在加载模型...
✅ 模型加载完成
生成语音: 静夜思 - 李白。床前明月光，疑是地上霜...
✅ 生成成功
   文件: /home/bbjose/.openclaw/workspace/data/tts_20260311_163000.mp3
   时长: 8.52 秒
```

---

## 踩坑记录

### ❌ 坑 1：OpenVINO 优化失败

**问题：**
- 转换 OpenVINO 后，性能**下降 3-5 倍**（52 秒 vs 10-15 秒）
- 模型大小增加（3.6GB → 4.0GB）

**原因：**
- OpenVINO 对 Qwen3-TTS 优化不足
- 某些操作不支持，回退到慢速实现

**解决方案：**
- ✅ **继续使用 PyTorch CPU 版本**（10-15 秒）
- ❌ **放弃 OpenVINO 优化**

**教训：**
- ⚠️ 优化框架不总是有效，需要实际测试
- ⚠️ CPU 场景下，PyTorch 可能已经足够好

---

### ❌ 坑 2：最后一个字被截断

**问题：**
- 生成的音频最后一个字会突然停止
- 听起来不完整

**原因：**
- 模型生成时没有预留尾部缓冲
- 音频波形在末尾直接截断

**解决方案：**
- ✅ 添加 0.5 秒尾部静音（已在脚本中实现）
- 参数：`SILENCE_DURATION = 0.5`

**代码：**
```python
# scripts/tts.py 第 68-72 行
if add_silence:
    silence_samples = int(sr * SILENCE_DURATION)
    silence = np.zeros(silence_samples, dtype=np.float32)
    audio_data = np.concatenate([wavs[0], silence])
```

---

### ⚠️ 坑 3：flash-attn 警告

**问题：**
```
Warning: flash-attn is not installed. Will only run the manual PyTorch version.
```

**原因：**
- flash-attn 是 GPU 加速库
- CPU 环境无法安装

**解决方案：**
- ✅ **可以忽略**（CPU 版本不需要）
- ✅ PyTorch CPU 版本已经足够快（10-15 秒）

---

### ⚠️ 坑 4：模型路径配置

**问题：**
- 默认模型路径硬编码在脚本中
- 不同用户路径不同

**解决方案：**
- ✅ 使用环境变量（推荐）
- ✅ 或直接修改 `scripts/tts.py` 中的 `DEFAULT_MODEL_PATH`

**代码：**
```python
# 方式 1：环境变量
export QWEN_TTS_MODEL_PATH="/path/to/your/model"

# 方式 2：修改脚本
DEFAULT_MODEL_PATH = os.environ.get(
    "QWEN_TTS_MODEL_PATH",
    "/home/bbjose/.openclaw/workspace/models/Qwen3-TTS-12Hz-1.7B-CustomVoice"
)
```

---

### ⚠️ 坑 5：内存占用

**问题：**
- 模型加载后占用 ~4GB 内存
- 低内存机器可能卡顿

**解决方案：**
- ✅ 确保至少 8GB 内存
- ✅ 关闭其他占用内存的程序
- 💡 未来：考虑量化模型（INT8）

---

## 使用方法

### 基本用法

```bash
# 最简单的方式
qwen-tts "你的文本"

# 指定输出文件
qwen-tts "你的文本" -o output.mp3

# 指定声音
qwen-tts "你的文本" -s Vivian

# 添加情感控制
qwen-tts "你的文本" -i "用温柔的语气说"
```

### 高级用法

```bash
# 古诗朗读（推荐配置）
qwen-tts "静夜思 - 李白。床前明月光，疑是地上霜。举头望明月，低头思故乡。" \
  -s Uncle_Fu \
  -i "用沉稳、富有感情的语气朗读古诗"

# 故事讲述
qwen-tts "从前有座山，山里有座庙..." \
  -s Vivian \
  -i "用讲故事给小孩听的语气"

# 新闻播报
qwen-tts "今日股市大涨..." \
  -s Uncle_Fu \
  -i "用专业的新闻播报语气"
```

### 参数说明

| 参数 | 说明 | 默认值 |
|-----|------|--------|
| `text` | 要转换的文本 | （必填）|
| `-o, --output` | 输出文件路径 | 自动生成 |
| `-s, --speaker` | 声音 ID | Uncle_Fu |
| `-l, --language` | 语言 | Chinese |
| `-i, --instruct` | 情感指令 | 无 |
| `--no-silence` | 不添加尾部静音 | 添加 |
| `-q, --quiet` | 静默模式 | 关闭 |

---

## 声音列表

**男声：**
- `Uncle_Fu` - 成熟稳重（推荐古诗、新闻）
- `Jerry` - 年轻活力

**女声：**
- `Vivian` - 温柔甜美（推荐故事）
- `Stella` - 活泼可爱

**完整列表：**
```bash
cat references/voices.md
```

---

## 常见问题

### Q1: 为什么不用 GPU？

**A:** 
- 大多数服务器没有 GPU
- CPU 版本已经够快（10-15 秒）
- 如果有 GPU，速度可达 2-3 秒

### Q2: 能否进一步优化速度？

**A:**
- ✅ 使用 GPU（最快）
- 💡 尝试 ONNX Runtime（待测试）
- 💡 模型量化 INT8（待测试）
- ❌ OpenVINO（已验证失败）

### Q3: 为什么不用 Edge-TTS？

**A:**
- Edge-TTS 质量好，速度快
- 但 **情感控制有限**
- Qwen3-TTS 可以通过自然语言控制情感

### Q4: 如何选择声音？

**A:**
- 古诗、新闻 → `Uncle_Fu`（成熟稳重）
- 故事、童话 → `Vivian`（温柔甜美）
- 其他场景 → 自行测试

---

## 许可证

MIT License - 详见 [LICENSE](LICENSE)

---

## 贡献

欢迎提交 Issue 和 Pull Request！

**GitHub**: https://github.com/bbJose/qwen3-tts-skill

---

## 更新日志

### v1.0.0 (2026-03-11)
- ✅ 初始发布
- ✅ PyTorch CPU 版本部署
- ✅ 添加尾部静音（0.5 秒）
- ✅ 模型缓存优化
- ✅ 完整文档

---

**部署时间**：2026-03-11 16:30
**测试状态**：✅ 通过
**性能**：10-15 秒（CPU）

🎤 开始使用吧！
