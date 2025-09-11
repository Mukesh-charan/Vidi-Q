from openai import OpenAI
import re
from pathlib import Path
from config import PROMPTS_DIR, API_CONFIG

class LLMHandler:
    def __init__(self):
        # Configure OpenAI client with generic API settings
        self.client = OpenAI(
            api_key=API_CONFIG["api_key"],
            base_url=API_CONFIG["base_url"]
        )
        
        # Load system prompt
        self.system_prompt = self._load_system_prompt()
    
    def _load_system_prompt(self):
        prompt_path = PROMPTS_DIR / "system_prompt.md"
        with open(prompt_path, 'r', encoding='utf-8') as f:
            return f.read()
    
    def generate_content(self, topic):
        enhanced_prompt = f"""
        Topic: {topic}
        
        Please generate a Manim script and transcript for this topic that is suitable for students.
        """
        
        try:
            response = self.client.chat.completions.create(
                model=API_CONFIG["model"],
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": enhanced_prompt}
                ],
                temperature=API_CONFIG["temperature"],
                max_tokens=API_CONFIG["max_tokens"]
            )
            return response.choices[0].message.content
        
        except Exception as e:
            raise Exception(f"API error: {str(e)}")
    
    def parse_response(self, response):
        # Extract Manim script
        manim_match = re.search(r'MANIM_SCRIPT:\s*```python\s*(.*?)\s*```', response, re.DOTALL)
        if not manim_match:
            manim_match = re.search(r'MANIM_SCRIPT:\s*(.*?)(?=TRANSCRIPT:|$)', response, re.DOTALL)
        
        # Extract transcript
        transcript_match = re.search(r'TRANSCRIPT:\s*(.*?)(?=MANIM_SCRIPT:|$)', response, re.DOTALL | re.IGNORECASE)
        if not transcript_match:
            transcript_match = re.search(r'TRANSCRIPT:\s*(.*)', response, re.DOTALL | re.IGNORECASE)
        
        manim_script = manim_match.group(1).strip() if manim_match else None
        transcript = transcript_match.group(1).strip() if transcript_match else None
        
        if not manim_script or not transcript:
            raise ValueError("Could not parse Manim script or transcript from API response")
        
        return manim_script, transcript


