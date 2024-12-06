import base64
import logging
import re
import random
from mistralai import Mistral
from typing import Optional, Union

class ImageAnalyzer:
    def __init__(self, mistral_api_key: str):
        self.client = Mistral(api_key=mistral_api_key)
        self.previous_scores = [] 
    def analyze_image(self, image_path: str, original_prompt: str) -> Optional[float]:
        """Analyzes the image using the Pixtral model with context.
        Returns a float score between 0-10 or None if analysis fails."""
        
        system_instructions = f"""You are an expert image quality analyzer. Evaluate the provided image and assign a score from 0-10.

Key Scoring Guidelines:
1. Use the FULL range from 0-10, where:
   - 0-2: Poor quality, major issues
   - 3-4: Below average
   - 5: Average
   - 6-7: Above average
   - 8-10: Exceptional quality
2. Consider these aspects:
   - Technical quality (resolution, clarity)
   - Composition and artistic merit
   - Adherence to intended purpose
3. Scoring Rules:
   - Avoid defaulting to 7-8 range without clear justification
   - Consider small details that could push score higher or lower
   - Use decimals for fine-grained scoring
   
Previous scores for context: {self.previous_scores[-3:] if self.previous_scores else 'None'}

Provide your analysis in this format:
1. Brief quality assessment
2. Key strengths and weaknesses
3. Final Score: [0-10]
"""

        def encode_image(image_path: str) -> Optional[str]:
            try:
                with open(image_path, "rb") as image_file:
                    return base64.b64encode(image_file.read()).decode('utf-8')
            except FileNotFoundError:
                logging.error(f"Error: The file {image_path} was not found.")
                return None
            except Exception as e:
                logging.error(f"Error: {e}")
                return None

        def extract_score(response: str) -> Optional[float]:
            try:
                logging.info(f"Raw response: {response}")
                score_pattern = r"Final Score:\s*(\d+(?:\.\d+)?)"
                match = re.search(score_pattern, response)
                
                if not match:
                    match = re.search(r"\b\d+(\.\d+)?\b", response)
                
                if match:
                    score = float(match.group(1) if match.group(1) else match.group(0))
                    score = min(max(score, 0), 10)  
                    if self.previous_scores and abs(self.previous_scores[-1] - score) < 0.3:
                        score += random.uniform(-0.2, 0.2)
                        score = min(max(score, 0), 10)  
                    
                    return round(score, 1)
                return None
            except Exception as e:
                logging.error(f"Error parsing score: {e}")
                return None

        base64_image = encode_image(image_path)
        if base64_image is None:
            logging.error("Image encoding failed")
            return None

        try:
            messages = [
                {
                    "role": "system",
                    "content": system_instructions
                },
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": f"Analyze this image. Original prompt: {original_prompt}"
                        },
                        {
                            "type": "image_url",
                            "image_url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    ]
                }
            ]

            chat_response = self.client.chat.complete(
                model="pixtral-12b-2409",
                messages=messages,
                temperature=0.7
            )
            
            response_text = chat_response.choices[0].message.content
            # logging.info('Response from Pixtral: %s', response_text)
            
            score = extract_score(response_text)
            if score is not None:
                self.previous_scores.append(score) 
                return score
                
            logging.error("Failed to extract valid score from response")
            return None

        except Exception as e:
            logging.error(f"API call failed: {e}")
            return None