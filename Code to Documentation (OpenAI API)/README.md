# Flask Web App with OpenAI API

This project is a simple Flask web application that lets you:
1. Generate documentation from code.
2. Add comments to code.
3. Optimize code to make it faster.

**IMPORTANT:** You need your own OpenAI API key to use this app. Follow the steps below to set it up.

---

## How to Set Up the Project

### 1. Get Your OpenAI API Key
1. Go to [https://platform.openai.com/signup/](https://platform.openai.com/signup/).
2. Sign up for an account (you'll get free credits to start).
3. Once signed in, visit [API Keys](https://platform.openai.com/account/api-keys) and create a new API key.
4. Copy the key (it will look like `sk-abc123456...`).

---

### 2. Set Up the API Key
1. Create a file named `.env` in the same folder as the project.
2. Add the following line to the `.env` file:
   ```plaintext
   API_KEY=your_openai_api_key