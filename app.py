import os
import logging
from typing import Optional
from dotenv import load_dotenv
import time
from prompt_generator import PromptGenerator
from image_generator import ImageGenerator
from image_analyzer import ImageAnalyzer
from social_media import SocialMediaManager

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s: %(message)s',
    handlers=[
        logging.FileHandler('scene_image_generator.log'),
        logging.StreamHandler()
    ]
)

class SceneImageGenerator:
    def __init__(self, cloudflare_account_id: str, cloudflare_api_token: str, 
                 pinterest_email: str = None, pinterest_password: str = None, mistral_api_key:str=None):
        self.prompt_generator = PromptGenerator(cloudflare_account_id, cloudflare_api_token)
        self.image_generator = ImageGenerator(cloudflare_account_id, cloudflare_api_token)
        self.image_analyzer = ImageAnalyzer(mistral_api_key=mistral_api_key)
        self.social_media = SocialMediaManager(pinterest_email, pinterest_password) if pinterest_email and pinterest_password else None
        self.generated_images = []
        
    def process_title(self, title: str, max_iterations: int = 2, score_threshold: float = 8.39, max_retries: int = 3):
        """Main process to generate and refine scenes."""
        print(f"\nGenerating concept art for: {title}")
        
        try:
            scenes = self.prompt_generator.generate_scenes(title)
            if not scenes or len(scenes) < 6:
                logging.error("Failed to generate valid scenes")
                return False

            best_versions = {}
            
            for i, prompt in enumerate(scenes):
                success = False
                retry_count = 0
                current_prompt = prompt
                
                while retry_count < max_retries and not success:
                    print(f"\nGenerating image for scene {i + 1} (Attempt {retry_count + 1}/{max_retries})...")
                    image_path = self.image_generator.generate_image(current_prompt, i + 1)
                    
                    if image_path and os.path.exists(image_path):
                        self.generated_images.append(image_path)  
                        score = self.image_analyzer.analyze_image(image_path, current_prompt)
                        
                        if score is not None:
                            print(f"Scene {i + 1} score: {score}")
                            
                            if score >= score_threshold:
                                best_versions[i] = (score, image_path, current_prompt)
                                print(f"✓ Scene {i + 1} generated successfully with score: {score}")
                                success = True
                            else:
                                print(f"× Score too low ({score}). Generating new prompt...")
                                current_prompt = self.prompt_generator.regenerate_scene(title, i + 1)
                                retry_count += 1
                        else:
                            print("× Failed to get valid score. Retrying...")
                            retry_count += 1
                    else:
                        print("× Failed to generate image. Retrying...")
                        retry_count += 1
                    
                    if not success and retry_count < max_retries:
                        time.sleep(2)

            if self.social_media and self.generated_images:
                print("\nPublishing to Pinterest...")
                if self.social_media.publish_to_pinterest(self.generated_images):
                    logging.info("Successfully published to Pinterest")
                else:
                    logging.error("Failed to publish to Pinterest")
            
            return len(best_versions) > 0

        except Exception as e:
            logging.error(f"Error in process_title: {e}")
            return False

def main():
    try:
        load_dotenv()
        user_input = input("Enter a high-level description for your scenes: ").strip()
        cloudflare_account_id = os.getenv('CLOUDFLARE_ACCOUNT_ID')
        cloudflare_api_token = os.getenv('CLOUDFLARE_API_TOKEN')
        pinterest_email = os.getenv('PINTEREST_EMAIL')
        pinterest_password = os.getenv('PINTEREST_PASSWORD')
        mistral_api_key = os.getenv('MISTRAL_API_KEY')
        generator = SceneImageGenerator(
            cloudflare_account_id=cloudflare_account_id,
            cloudflare_api_token=cloudflare_api_token,
            pinterest_email=pinterest_email,
            pinterest_password=pinterest_password,
            mistral_api_key=mistral_api_key
        )
        
        success = generator.process_title(user_input)
        
        if success:
            logging.info("Scene generation and publishing completed successfully")
        else:
            logging.error("Failed to complete the process")
            
    except Exception as e:
        logging.error(f"Unexpected error in main process: {e}")

if __name__ == "__main__":
    main()