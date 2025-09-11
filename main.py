import argparse
from pathlib import Path
from utils.llm_handler import LLMHandler
from utils.manim_generator import ManimGenerator
from utils.audio_generator import AudioGenerator
from utils.video_combiner import VideoCombiner
from config import OUTPUT_DIR, API_CONFIG
import time

class EducationalVideoGenerator:
    def __init__(self):
        self.llm_handler = LLMHandler()
        self.manim_generator = ManimGenerator()
        self.audio_generator = AudioGenerator()
        self.video_combiner = VideoCombiner()
    
    def generate_video(self, topic):
        print(f"Generating educational video for students about: {topic}")
        
        try:
            # Step 1: Generate content with LLM
            print("Step 1/4: Generating educational content...")
            llm_response = self.llm_handler.generate_content(topic)
            manim_script, transcript = self.llm_handler.parse_response(llm_response)
            
            # Save generated content for debugging
            with open(OUTPUT_DIR / "generated_manim_script.py", "w", encoding='utf-8') as f:
                f.write(manim_script)
            with open(OUTPUT_DIR / "generated_transcript.txt", "w", encoding='utf-8') as f:
                f.write(transcript)
            
            # Step 2: Generate animation with Manim
            print("Step 2/4: Creating educational animations...")
            video_path = self.manim_generator.generate_animation(manim_script)
            
            # Step 3: Generate audio from transcript
            print("Step 3/4: Generating audio explanation...")
            audio_path = self.audio_generator.generate_audio(transcript)
            
            # Step 4: Combine audio and video
            print("Step 4/4: Finalizing educational video...")
            timestamp = int(time.time())
            output_path = self.video_combiner.combine_audio_video(
                video_path, audio_path, f"student_learning_video_{timestamp}"
            )
            
            print(f"Educational video for students completed: {output_path}")
            return output_path
            
        except Exception as e:
            print(f"Error generating educational video: {str(e)}")
            raise e

def main():
    parser = argparse.ArgumentParser(description="Generate educational videos for students")
    parser.add_argument("topic", help="The educational topic to explain to students")
    
    args = parser.parse_args()
    
    # Check if API key is configured
    if not API_CONFIG["api_key"] or API_CONFIG["api_key"] == "your_api_key_here":
        print("Error: Please set your API key in the .env file")
        return
    
    generator = EducationalVideoGenerator()
    output_path = generator.generate_video(args.topic)
    
    print(f"\nEducational video for students created successfully!")
    print(f"Output file: {output_path}")

if __name__ == "__main__":
    main()


