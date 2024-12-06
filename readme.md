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
  - Pinterest Email and Password
- **Environment Variables Setup**: Properly set up the environment variables for Cloudflare and Pinterest.
- **Packages**: Install the required packages using:

```bash
  pip install -r requirements.txt
```

## Installation

- Clone the repository:

```bash
git clone https://your-repository-url.git
cd your-repository-directory
```

- Install the required packages:

```bash
pip install -r requirements.txt
```

- Set up environment variables in a .env file:

```text
CLOUDFLARE_ACCOUNT_ID=your_cloudflare_account_id
CLOUDFLARE_API_TOKEN=your_cloudflare_api_token
PINTEREST_EMAIL=your_pinterest_email
PINTEREST_PASSWORD=your_pinterest_password
```

## Usage

- Run the application:

```bash
python main.py
```
- **user_input**: The title or theme provided by the user to guide the scene and image generation process.  
- **max_iterations**: The maximum number of times the system will loop through the generation and refinement process.  
- **score_threshold**: The minimum quality score an image must achieve to be considered acceptable and move forward.  
- **max_retries**: The maximum number of attempts allowed to refine and regenerate an image if it doesn't meet the quality threshold.  