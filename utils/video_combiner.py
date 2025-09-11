from moviepy.editor import VideoFileClip, AudioFileClip
from pathlib import Path
from config import OUTPUT_DIR

class VideoCombiner:
    def __init__(self):
        pass
    
    def combine_audio_video(self, video_path, audio_path, output_filename="student_educational_video"):
        try:
            # Load video and audio
            video = VideoFileClip(str(video_path))
            audio = AudioFileClip(str(audio_path))
            
            # Align durations: trim or loop audio to match video
            if audio.duration > video.duration:
                audio = audio.subclip(0, video.duration)
            elif audio.duration < video.duration:
                # simple extension: freeze last frame of audio by repeating silence is non-trivial; keep as-is
                pass
            
            # Add audio to video
            final_video = video.set_audio(audio)
            
            # Generate output path
            output_path = OUTPUT_DIR / f"{output_filename}.mp4"
            
            # Write the final video
            final_video.write_videofile(
                str(output_path),
                codec='libx264',
                audio_codec='aac',
                threads=4,
                verbose=False,
                logger=None
            )
            
            # Close the clips
            video.close()
            audio.close()
            final_video.close()
            
            return output_path
            
        except Exception as e:
            raise Exception(f"Failed to combine audio and video: {str(e)}")


