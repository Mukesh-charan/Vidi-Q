import subprocess
from pathlib import Path
from config import MANIM_SCRIPTS_DIR, VIDEO_FILES_DIR, MANIM_CONFIG

class ManimGenerator:
    def __init__(self):
        self.quality_flag = self._get_quality_flag()
    
    def _get_quality_flag(self):
        quality_map = {
            "low_quality": "-ql",
            "medium_quality": "-qm",
            "high_quality": "-qh",
            "production_quality": "-qk"
        }
        return quality_map.get(MANIM_CONFIG["quality"], "-qh")
    
    def generate_animation(self, manim_script, scene_name="StudentExplanationScene"):
        # Create a temporary Python file with the Manim script
        script_filename = f"manim_script.py"
        script_path = MANIM_SCRIPTS_DIR / script_filename
        
        with open(script_path, 'w', encoding='utf-8') as f:
            f.write(manim_script)
        
        # Run Manim to generate the animation
        try:
            result = subprocess.run([
                "manim", 
                self.quality_flag,
                "-o", scene_name,
                str(script_path),
                scene_name
            ], capture_output=True, text=True, cwd=VIDEO_FILES_DIR, timeout=300)  # 5 minute timeout
            
            if result.returncode != 0:
                raise Exception(f"Manim error: {result.stderr}")
            
            # Find the generated video file (search recursively under VIDEO_FILES_DIR)
            video_ext = MANIM_CONFIG["format"]
            candidates = list(VIDEO_FILES_DIR.rglob(f"*{scene_name}*.{video_ext}"))
            if not candidates:
                # Also search default Manim media directories created relative to cwd
                media_dir = VIDEO_FILES_DIR / "media"
                candidates = list(media_dir.rglob(f"*{scene_name}*.{video_ext}"))
            if not candidates:
                raise FileNotFoundError(f"Generated video not found for scene '{scene_name}'")
            # Pick the most recently modified file
            video_path = max(candidates, key=lambda p: p.stat().st_mtime)
            
            return video_path
            
        except subprocess.TimeoutExpired:
            raise Exception("Manim rendering timed out after 5 minutes")
        except Exception as e:
            raise Exception(f"Failed to generate animation: {str(e)}")
        
        finally:
            # Clean up the script file
            if script_path.exists():
                script_path.unlink()


