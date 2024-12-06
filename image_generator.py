import os
import requests
import logging
from typing import Optional
import time
import base64
import random
class ImageGenerator:
    def __init__(self, cloudflare_account_id: str, cloudflare_api_token: str, output_directory: str = "generated_images"):
        self.api_url = f"https://api.cloudflare.com/client/v4/accounts/{cloudflare_account_id}/ai/run/@cf/black-forest-labs/flux-1-schnell"
        self.api_token = cloudflare_api_token
        self.output_directory = os.path.abspath(output_directory)
        os.makedirs(self.output_directory, exist_ok=True)

    def generate_image(self, prompt: str, image_number: int) -> Optional[str]:
        """Generate an image with simplified prompt."""
        try:
            
            simplified_prompt = f"Professional product photography: {prompt}"
            simplified_prompt = simplified_prompt[:200]  
            
            payload = {
                "prompt": simplified_prompt,
                "num_steps": 15,
                "width": 1280,
                "height": 720,
                "guidance_scale": 7.5,  
                "seed": random.randint(1, 1000000)  
            }
            
            response = requests.post(
                self.api_url,
                headers={"Authorization": f"Bearer {self.api_token}"},
                verify=False,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                if 'result' in result and 'image' in result['result']:
                    image_data = base64.b64decode(result['result']['image'])
                    image_path = os.path.join(self.output_directory, f"scene_{image_number}.png")
                    
                    with open(image_path, "wb") as f:
                        f.write(image_data)
                    
                    print(f"✓ Image {image_number} generated successfully: {image_path}")
                    return image_path
            else:
                logging.error(f"Image generation failed: {response.status_code} - {response.text}")
                return None
            
        except Exception as e:
            logging.error(f"Error generating image: {e}")
            return None