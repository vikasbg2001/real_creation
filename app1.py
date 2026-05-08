import streamlit as st
import os
import glob

# Updated imports to include vfx for transitions
try:
    from moviepy.editor import ImageClip, concatenate_videoclips, AudioFileClip, vfx
except ImportError:
    from moviepy import ImageClip, concatenate_videoclips, AudioFileClip, vfx

import yt_dlp

# ... (Keep cleanup_temp_files, download_youtube_audio, and handle_youtube_download as they are) ...

def create_video(image_files, duplicate_count, fps, audio_path):
    """Processes images with Crossfade transitions and merges with audio."""
    clips = []
    duration_per_image = duplicate_count / fps
    transition_duration = 0.5  # Half-second fade effect
    target_resolution = (1280, 720) 

    for idx, img_file in enumerate(image_files):
        temp_img_path = f"temp_img_{idx}.png"
        with open(temp_img_path, "wb") as f:
            f.write(img_file.getbuffer())
        
        # Create the clip
        clip = ImageClip(temp_img_path).set_duration(duration_per_image)
        clip = clip.resize(target_resolution) 
        
        # Add Crossfade Effect
        # Note: crossfadein requires the clips to overlap slightly in the concatenation
        if idx > 0:
            clip = clip.crossfadein(transition_duration)
            
        clips.append(clip)
    
    # method="compose" is required for transparency/fade effects to work
    final_video = concatenate_videoclips(clips, method="compose", padding=-transition_duration)
    final_video = final_video.set_fps(fps)
    
    # Audio Handling
    audio_clip = AudioFileClip(audio_path)
    if audio_clip.duration > final_video.duration:
        audio_clip = audio_clip.subclip(0, final_video.duration)

    final_clip = final_video.set_audio(audio_clip)
    
    output_filename = "output_video.mp4"
    final_clip.write_videofile(output_filename, codec="libx264", audio_codec="aac")
    return output_filename

# ... (Keep the rest of your Streamlit UI Logic the same) ...
