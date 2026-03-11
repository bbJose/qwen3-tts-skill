#!/usr/bin/env python3
"""
Qwen3-TTS 语音合成脚本
"""
import argparse
import sys
import os
import numpy as np
import soundfile as sf
from pathlib import Path
from qwen_tts import Qwen3TTSModel
import torch

# 默认参数
DEFAULT_MODEL_PATH = "/home/bbjose/.openclaw/workspace/models/Qwen3-TTS-12Hz-1.7B-CustomVoice"
DEFAULT_OUTPUT_DIR = "/home/bbjose/.openclaw/workspace/data"
DEFAULT_SPEAKER = "Uncle_Fu"
DEFAULT_LANGUAGE = "Chinese"
SILENCE_DURATION = 0.5  # 尾部静音时长（秒）

# 全局模型缓存（避免重复加载）
_model_cache = None

def load_model(model_path=DEFAULT_MODEL_PATH, quiet=False):
    """加载模型（带缓存）"""
    global _model_cache
    
    if _model_cache is not None:
        return _model_cache
    
    if not quiet:
        print("正在加载模型...", file=sys.stderr)
    
    _model_cache = Qwen3TTSModel.from_pretrained(
        model_path,
        device_map="cpu",
        dtype=torch.float32,
    )
    
    if not quiet:
        print("✅ 模型加载完成", file=sys.stderr)
    
    return _model_cache

def generate_tts(
    text,
    output_file=None,
    speaker=DEFAULT_SPEAKER,
    language=DEFAULT_LANGUAGE,
    instruct=None,
    add_silence=True,
    quiet=False
):
    """
    生成语音
    
    Args:
        text: 要转换的文本
        output_file: 输出文件路径（默认自动生成）
        speaker: 声音 ID
        language: 语言
        instruct: 情感指令
        add_silence: 是否添加尾部静音
        quiet: 静默模式
    
    Returns:
        输出文件路径
    """
    # 加载模型
    model = load_model(quiet=quiet)
    
    # 生成输出文件名
    if output_file is None:
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = os.path.join(DEFAULT_OUTPUT_DIR, f"tts_{timestamp}.mp3")
    
    # 确保输出目录存在
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    # 生成语音
    if not quiet:
        print(f"生成语音: {text[:50]}...", file=sys.stderr)
    
    wavs, sr = model.generate_custom_voice(
        text=text,
        language=language,
        speaker=speaker,
        instruct=instruct,
        max_new_tokens=2048,
        temperature=0.8,
        top_p=0.95,
        repetition_penalty=1.1,
    )
    
    # 添加尾部静音
    if add_silence:
        silence_samples = int(sr * SILENCE_DURATION)
        silence = np.zeros(silence_samples, dtype=np.float32)
        audio_data = np.concatenate([wavs[0], silence])
    else:
        audio_data = wavs[0]
    
    # 保存文件
    sf.write(output_file, audio_data, sr)
    
    if not quiet:
        duration = len(audio_data) / sr
        print(f"✅ 生成成功", file=sys.stderr)
        print(f"   文件: {output_file}", file=sys.stderr)
        print(f"   时长: {duration:.2f} 秒", file=sys.stderr)
    
    return output_file

def main():
    parser = argparse.ArgumentParser(
        description="Qwen3-TTS 语音合成工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s "静夜思 - 李白。床前明月光，疑是地上霜。举头望明月，低头思故乡。"
  %(prog)s "你的文本" -o output.mp3 -s Vivian -i "用温柔的语气说"
        """
    )
    
    parser.add_argument("text", help="要转换的文本")
    parser.add_argument("-o", "--output", help="输出文件路径（默认自动生成）")
    parser.add_argument("-s", "--speaker", default=DEFAULT_SPEAKER, 
                       help=f"声音 ID（默认：{DEFAULT_SPEAKER}）")
    parser.add_argument("-l", "--language", default=DEFAULT_LANGUAGE,
                       help=f"语言（默认：{DEFAULT_LANGUAGE}）")
    parser.add_argument("-i", "--instruct", help="情感指令（自然语言描述）")
    parser.add_argument("--no-silence", action="store_true", 
                       help="不添加尾部静音")
    parser.add_argument("-q", "--quiet", action="store_true",
                       help="静默模式（只输出文件路径）")
    
    args = parser.parse_args()
    
    # 生成语音
    output_file = generate_tts(
        text=args.text,
        output_file=args.output,
        speaker=args.speaker,
        language=args.language,
        instruct=args.instruct,
        add_silence=not args.no_silence,
        quiet=args.quiet
    )
    
    # 静默模式只输出文件路径
    if args.quiet:
        print(output_file)
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
