# Phishing Email Detection with Python and OpenAI GPT-3.5-turbo

## Overview

This project aims to identify and contextualize the detection of phishing emails using Python and the OpenAI GPT-3.5-turbo model. Phishing is a common cyber threat, and this solution leverages the power of natural language processing to enhance email security.

## Features

- **Phishing Detection**: Utilize the OpenAI GPT-3.5-turbo model to analyze email content and identify potential phishing attempts.
  
- **Contextual Understanding**: Enhance the detection by contextualizing email content, improving accuracy in distinguishing legitimate emails from phishing attempts.

## Requirements

- Python 3.x
- OpenAI GPT-3.5-turbo API key (Refer to [OpenAI API documentation](https://beta.openai.com/docs/) for obtaining the key)

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/yourusername/phishing-detection.git
    cd phishing-detection
    ```

2. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

## Usage

Run the detection script with the following command:

```bash
python detect_phishing.py --email_path path/to/email/file.eml
