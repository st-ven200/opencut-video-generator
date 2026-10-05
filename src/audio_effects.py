import wave
import math
import struct
import os

def generate_sfx_pop(output_path):
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    sample_rate = 44100
    duration = 0.12
    n_samples = int(sample_rate * duration)
    with wave.open(output_path, 'w') as wav_file:
        wav_file.setnchannels(2)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        for i in range(n_samples):
            t = i / sample_rate
            freq = 900 - (t / duration) * 500
            env = math.exp(-t * 25)
            sample = int(32767 * env * 0.6 * math.sin(2 * math.pi * freq * t))
            wav_file.writeframes(struct.pack('<hh', sample, sample))
    return output_path

def generate_sfx_whoosh(output_path):
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    sample_rate = 44100
    duration = 0.35
    n_samples = int(sample_rate * duration)
    with wave.open(output_path, 'w') as wav_file:
        wav_file.setnchannels(2)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        for i in range(n_samples):
            t = i / sample_rate
            freq = 180 + math.sin(t / duration * math.pi) * 850
            env = math.sin(t / duration * math.pi)
            sample = int(32767 * env * 0.5 * math.sin(2 * math.pi * freq * t))
            wav_file.writeframes(struct.pack('<hh', sample, sample))
    return output_path

def generate_sfx_ding(output_path):
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    sample_rate = 44100
    duration = 0.5
    n_samples = int(sample_rate * duration)
    with wave.open(output_path, 'w') as wav_file:
        wav_file.setnchannels(2)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        for i in range(n_samples):
            t = i / sample_rate
            freq = 1200
            env = math.exp(-t * 8)
            sample = int(32767 * env * 0.4 * (math.sin(2 * math.pi * freq * t) + 0.5 * math.sin(2 * math.pi * freq * 1.5 * t)))
            wav_file.writeframes(struct.pack('<hh', sample, sample))
    return output_path

def generate_bgm_ambient(output_path, duration=300):
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    sample_rate = 44100
    n_samples = int(sample_rate * duration)
    chords = [220.0, 277.18, 329.63, 440.0, 554.37] # A Major 9th tech ambient pad
    with wave.open(output_path, 'w') as wav_file:
        wav_file.setnchannels(2)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        for i in range(n_samples):
            t = i / sample_rate
            lfo = 0.5 + 0.5 * math.sin(2 * math.pi * 0.15 * t)
            lfo2 = 0.5 + 0.5 * math.cos(2 * math.pi * 0.08 * t)
            s = sum(math.sin(2 * math.pi * freq * t) for freq in chords) / len(chords)
            sample_l = int(32767 * 0.12 * lfo * s)
            sample_r = int(32767 * 0.12 * lfo2 * s)
            wav_file.writeframes(struct.pack('<hh', sample_l, sample_r))
    return output_path
