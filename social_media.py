from typing import List, Optional
import os
import logging
import time
import requests
from py3pin.Pinterest import Pinterest

class SocialMediaManager:
    def __init__(self, pinterest_email: Optional[str] = None, pinterest_password: Optional[str] = None):
        self.pinterest_email = pinterest_email
        self.pinterest_password = pinterest_password
        self.pinterest = None
        if pinterest_email and pinterest_password:
            self.pinterest = Pinterest(email=pinterest_email, password=pinterest_password)
            try:
                self.pinterest.login()
                logging.info("Successfully logged into Pinterest")
            except Exception as e:
                logging.error(f"Failed to login to Pinterest: {e}")
                self.pinterest = None

    def publish_to_pinterest(self, image_paths: List[str], board_name: str = "AI") -> bool:
        """Publish generated images to Pinterest."""
        if not self.pinterest:
            logging.error("Pinterest not initialized. Check credentials.")
            return False

        try:
            # Hardcoded URL to fetch board information
            url = '''https://in.pinterest.com/resource/BoardsResource/get/?source_url=%2Fthetulipjani%2F_created%2F&data=%7B%22options%22%3A%7B%22page_size%22%3A1%2C%22privacy_filter%22%3A%22all%22%2C%22sort%22%3A%22last_pinned_to%22%2C%22username%22%3A%22thetulipjani%22%7D%2C%22context%22%3A%7B%7D%7D&_=1733307913382'''
            
            response = requests.get(url)
            if response.status_code != 200:
                logging.error(f"Failed to fetch board information: {response.status_code}")
                return False

            board_data = response.json()
            board_id = None
            for board in board_data['resource_response']['data']:
                if board['name'] == board_name:
                    board_id = board['id']
                    break

            if not board_id:
                logging.error(f"Board '{board_name}' not found in the response.")
                return False

            successful_uploads = 0

            for image_path in image_paths:
                try:
                    # Generate metadata for the pin
                    scene_number = os.path.basename(image_path).split('_')[1].split('.')[0]
                    pin_title = f"AI Generated Concept Art - Scene {scene_number}"
                    pin_description = f"AI generated concept art showcasing unique perspectives and creative compositions. Scene {scene_number}"
                    pin_hashtags = "#AIArt #ConceptArt #DigitalArt #ArtificialIntelligence #CreativeAI #GenerativeArt"

                    # Log upload attempt
                    logging.info(f"Attempting to upload: {image_path}")
                    logging.info(f"Title: {pin_title}")
                    logging.info(f"Description: {pin_description}")

                    # Ensure image path is absolute
                    abs_image_path = os.path.abspath(image_path)
                    if not os.path.exists(abs_image_path):
                        logging.error(f"Image file not found: {abs_image_path}")
                        continue

                    # Use upload_pin instead of pin method
                    response = self.pinterest.upload_pin(
                        board_id=board_id,
                        image_file=abs_image_path,
                        description=f"{pin_description}\n\n{pin_hashtags}",
                        title=pin_title
                    )

                    if response:
                        logging.info(f"Successfully uploaded {image_path} to Pinterest.")
                        successful_uploads += 1
                    else:
                        logging.error(f"Failed to upload {image_path}.")

                    time.sleep(3)  # Delay between uploads to avoid rate limiting

                except Exception as e:
                    logging.error(f"Error uploading {image_path}: {e}")
                    continue

            if successful_uploads == len(image_paths):
                logging.info("All images uploaded successfully.")
                return True
            else:
                logging.warning(f"Uploaded {successful_uploads} out of {len(image_paths)} images.")
                return False

        except Exception as e:
            logging.error(f"Pinterest publishing error: {e}")
            return False