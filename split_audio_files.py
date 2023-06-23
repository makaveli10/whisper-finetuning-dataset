import os
import json
import glob
import csv
from pydub import AudioSegment

def resample_audio(audio, sample_rate):
    return audio.set_frame_rate(sample_rate)

def write_audio_segments_to_csv(audio_segments, csv_file_path):
    with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file, quoting=csv.QUOTE_MINIMAL)
        writer.writerow(['file_name', 'sentence'])
        
        for segment in audio_segments:
            sentence = segment['sentence']
            writer.writerow([segment['path'], sentence])
    
    print(f'Saved CSV file: {csv_file_path}')

def split_audio_by_subtitles(audio_paths, output_dir, json_filename):
    audio_segments = []
    output_dir_train = os.path.join(output_dir, 'data/train')
    output_dir_test = os.path.join(output_dir, 'data/test')
    os.makedirs(output_dir_train, exist_ok=True)
    os.makedirs(output_dir_test, exist_ok=True)
    
    for audio_path in audio_paths:
        audio_filename = os.path.splitext(os.path.basename(audio_path))[0]
        
        vtt_path = audio_path.replace(".mp3", ".vtt")
        with open(vtt_path, 'r') as vtt_file:
            vtt_content = vtt_file.read()
        
        subtitle_entries = vtt_content.strip().split('\n\n')
        
        audio = AudioSegment.from_file(audio_path)
        
        sample_rate = 16000
        audio = resample_audio(audio, sample_rate)
        
        count = 0
        for sub in subtitle_entries:
            if "-->" in sub:
                lines = sub.strip().split('\n')
                
                timestamps = lines[0].split(' --> ')
                start_time = timestamps[0]
                end_time = timestamps[1]
                
                start_time_ms = int(start_time.split(":")[0]) * 60 * 1000 + int(float(start_time.split(":")[1]) * 1000)
                end_time_ms = int(end_time.split(":")[0]) * 60 * 1000 + int(float(end_time.split(":")[1]) * 1000)
                
                subtitle_text = ' '.join(lines[1:])
                
                audio_chunk = audio[start_time_ms:end_time_ms]
                
                output_dir = output_dir_test if audio_filename.startswith("8") else output_dir_train
                output_file = os.path.join(output_dir, f'{audio_filename}_{count}.mp3')
                
                audio_chunk.export(output_file, format='mp3')
                
                segment_data = {
                    'path': output_file,
                    'sentence': subtitle_text.strip(),
                }
                
                audio_segments.append(segment_data)
                
                print(f'Saved audio chunk: {output_file}')
                count += 1
    
    csv_path = os.path.join(output_dir, "metadata.csv")
    write_audio_segments_to_csv(audio_segments, csv_path)
    
    print(f'Saved csv file: {csv_path}')
    print('Audio splitting complete!')

if __name__=="__main__":
    audio_paths = glob.glob('*.mp3')
    output_dir = 'audio_files'
    os.makedirs(output_dir, exist_ok=True)
    json_filename = 'audio_segments.json'

    split_audio_by_subtitles(audio_paths, output_dir, json_filename)
