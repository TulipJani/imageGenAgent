from typing import List
import requests
import logging
class PromptGenerator:
    def __init__(self, cloudflare_account_id: str, cloudflare_api_token: str):
        self.llama_api_url = f"https://api.cloudflare.com/client/v4/accounts/{cloudflare_account_id}/ai/run/@cf/meta/llama-3-8b-instruct-awq"
        self.api_token = cloudflare_api_token

    def sanitize_prompt(self, prompt: str) -> str:
        """Sanitize prompt to avoid NSFW detection."""
        # Remove potentially problematic words
        words_to_remove = ['dark', 'smoke', 'speed', 'chase', 'blazing', 'rebel', 'edgy']
        sanitized = prompt.lower()
        for word in words_to_remove:
            sanitized = sanitized.replace(word.lower(), '')
        
        # Keep only essential car and scene elements
        if len(sanitized) > 200:
            sanitized = sanitized[:200]
        
        return f"Professional photograph of {sanitized}"

    def generate_scenes(self, title: str) -> List[str]:
        """Generate scenes with simplified prompts."""
        system_prompt = f"""Generate 6 simple, clean photography prompts for '{title}'.
        Format: Scene X: [Brief description focusing on lighting and composition]
        Keep it professional and suitable for commercial photography.
        Each prompt should be under 50 words.
        Focus on natural lighting and clean compositions."""
        
        try:
            response = requests.post(
                self.llama_api_url,
                headers={"Authorization": f"Bearer {self.api_token}"},
                json={
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": f"Generate 6 clean, professional cinematic prompts for: {title}"}
                    ]
                },
                verify=False,
                timeout=30
            )
            
            response.raise_for_status()
            result = response.json()
            
            if 'result' in result and 'response' in result['result']:
                scenes = [scene.strip() for scene in result['result']['response'].strip().splitlines() if scene.strip()]
                # Sanitize each prompt
                sanitized_scenes = [self.sanitize_prompt(scene) for scene in scenes]
                return sanitized_scenes
            
            return self._get_default_scenes(title)
            
        except Exception as e:
            logging.error(f"Scene generation error: {e}")
            return self._get_default_scenes(title)


    def _get_default_scenes(self, title: str) -> List[str]:
        """Fallback scenes if API fails."""
        return [f"Scene {i+1}: {title} with dramatic lighting and composition" for i in range(6)]

    def validate_scenes(self, scenes: List[str], title: str) -> List[str]:
        """Validate each scene to ensure it's relevant to the title."""
        validated_scenes = []
        keywords = set(title.lower().split())
        
        for scene in scenes:
            scene_lower = scene.lower()
            if any(keyword in scene_lower for keyword in keywords):
                validated_scenes.append(scene)
            else:
                new_scene = self.regenerate_scene(title, len(validated_scenes) + 1)
                if new_scene:
                    validated_scenes.append(new_scene)
                    
        return validated_scenes[:6]

    def regenerate_scene(self, title: str, scene_number: int) -> str:
        """Regenerate a single scene with stronger relevance to the title."""
        system_prompt = f"""Generate a single, highly detailed scene for a {title} commercial.
        Scene number: {scene_number}
        
        MUST include these elements:
        1. Direct reference to {title}
        2. Specific camera angles and movements
        3. Detailed lighting setup
        4. Exact composition details
        
        Format: Scene {scene_number}: [Technical description]"""

        try:
            response = requests.post(
                self.llama_api_url,
                headers={"Authorization": f"Bearer {self.api_token}"},
                json={
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": f"Generate scene {scene_number} for {title}"}
                    ]
                },
                verify=False
            )
            
            if response.status_code == 200:
                result = response.json()
                if 'result' in result and 'response' in result['result']:
                    return result['result']['response'].strip()
                    
            return f"Scene {scene_number}: Default scene for {title} with dramatic lighting and composition"
            
        except Exception as e:
            logging.error(f"Scene regeneration error: {e}")
            return f"Scene {scene_number}: Default scene for {title} with dramatic lighting and composition"