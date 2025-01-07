# Sales Template - Quick Start Guide
Welcome to your new sales app template! This template is built with Reflex and integrates OpenAI for enhanced AI-driven features.

## Setup Instructions
Follow these steps to get your app up and running quickly.

## 1. Install Dependencies
First, install all the necessary dependencies:

```shell
pip install -r requirements.txt
```

## 2. Initialize Database

```shell
reflex db init
```

## 3. Set Your OpenAI API Key
To utilize OpenAI in this template, you need to set your OPENAI_API_KEY environment variable. Here’s how you can set it based on your operating system:

### On Linux / macOS:
```shell
export OPENAI_API_KEY=your-openai-api-key
```

### On Windows (Command Prompt):
```shell
set OPENAI_API_KEY=your-openai-api-key
```

### On Windows (PowerShell):
```shell
$env:OPENAI_API_KEY="your-openai-api-key"
```

### 4. Run the App
After setting up your environment variable, you can start the app:

```shell
reflex run
```
This will launch the app locally and you can interact with it in your browser.

### Notes
- Make sure you have your OpenAI API key. If you don’t have one, you can get it by signing up at [OpenAI](https://openai.com/api/).
- You can permanently set the environment variable in your shell configuration (e.g., `.bashrc` or `.zshrc` for Linux/macOS) to avoid setting it every time.
Enjoy building with Reflex and OpenAI!

## Applying Database Schema Changes

If changes are made to the database models after initialization, they can be
applied by running the following commands:

```bash
reflex db makemigrations --message "Brief description of the change"
```

```bash
reflex db migrate
```
