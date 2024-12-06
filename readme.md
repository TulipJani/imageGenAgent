# MoodboardAgent

## Overview

The MoodboardAgent is a sophisticated tool designed to create detailed concept art scenes based on a high-level description provided by the user. Leveraging advanced AI models, it generates scene descriptions and images, manages these images using PureRef, and optionally publishes them to Pinterest.

---

## Features

- **Scene Description Generation**: Creates 6 detailed scene descriptions based on the provided high-level description.
- **Image Generation**: Utilizes AI to generate images from the scene descriptions.
- **Image Analysis**: Analyzes the generated images for quality and relevance.
- **Iterative Improvement**: Refines scene descriptions and images based on analysis scores.
- **Image Management in PureRef**: Arranges generated images for review.
- **Pinterest Publication**: Publishes the final images to a Pinterest board.

---

## Requirements

- **Python**: 3.8 or higher
- **API Credentials**:
  - Cloudflare API Token
  - Cloudflare Account ID
  - Mistral API Key
  - Pinterest Email and Password
- **Environment Variables Setup**: Properly set up the environment variables for Cloudflare and Pinterest.

---

## Installation

1. **Create a virtual environment**:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

2. **Install the required packages**:

   ```bash
   pip install -r requirements.txt
   ```

3. **Create a `.env` file** and add the following keys:

   ```text
   CLOUDFLARE_ACCOUNT_ID=your_cloudflare_account_id
   CLOUDFLARE_API_TOKEN=your_cloudflare_api_token
   MISTRAL_API_KEY=your_mistral_api_key
   PINTEREST_EMAIL=your_pinterest_email
   PINTEREST_PASSWORD=your_pinterest_password
   ```

4. **Create a JSON file for Pinterest credentials**:

   Create a file at `pinterest_credentials/{email}.json` with your Pinterest credentials.

5. **Run the application**:

   ```bash
   python app.py
   ```

---

## Usage

- **user_input**: The title or theme provided by the user to guide the scene and image generation process.
- **max_iterations**: The maximum number of times the system will loop through the generation and refinement process.
- **score_threshold**: The minimum quality score an image must achieve to be considered acceptable and move forward.
- **max_retries**: The maximum number of attempts allowed to refine and regenerate an image if it doesn't meet the quality threshold.
