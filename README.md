# PyngAutomation
# PyngTest Agent

PyngTest Agent is an AI-based automation tool for testing the web interface of https://pyng.co.in. It enables test execution using LLMs (OpenAI, Gemini, or Anthropic) through predefined flows or natural language instructions. The app is built with Streamlit for an interactive visual experience. Add api key in .env

## Features

- Run natural language UI test instructions  
- Select from reusable predefined test cases  
- LLM model selection (OpenAI, Gemini, Anthropic)  
- Optional vision support for UI element understanding  
- History logs automatically cleaned after execution

  ## Prerequisites

- Python 3.11 or higher

## Clone the Repository

```
git clone https://github.com/Vaishnavi024/PyngAutomation  
cd PyngAutomation
```

## Requirements
Prefer installation instruction.txt and run the commands mentioned in it to set up 

```  
pip install -r requirements.txt
playwright install chromium
pip install langchain-google-genai
pip install langchain
```

## Usage

``` 
streamlit run app.py
```

After launching:

- Enter a custom instruction, or  
- Select predefined tests from the list and run  

## Writing New Tests

To add a new test, open `predefined_tests.py` and add an entry like this:

```
PREDEFINED_TESTS["My Custom Test"] = '''
Step 1: Go to the homepage.  
Step 2: Check for text or element.  
Step 3: Return the result.  
'''
```


## API Key Setup

Create a `.env` file in the root directory with your API keys:
```
dotenv  
OPENAI_API_KEY=your-openai-key  
GOOGLE_API_KEY=your-google-api-key  
ANTHROPIC_API_KEY=your-anthropic-api-key
```
These are loaded and masked in the app sidebar.

## Demo & Screenshots

<!-- Add your screenshots and videos here -->
Here are a few sample test runs demonstrating the PyngTest Agent in action:

- **Homepage Validation Test**  
  Checks page load and visible elements.  
  ✅ Passed.

- **Login Flow Until OTP**  
  Validates login popup, dummy number input, and OTP screen.  
  ✅ Passed.

- **AI Search – Server-Side Failure**  
  Pyng’s search failed due to a backend issue.  
  ❌ Agent correctly identified the failure and returned the right message.

- **AI Search – Success Case**  
  Searches for "Tarot for career" using the AI chat and validates result cards.  
  ✅ Passed.

[Watch working videos in this drive](https://drive.google.com/drive/folders/1RPetfRbVBUQLxkNZPvg-RyLmiuqmp-R4?usp=sharing)

- **Bottom Navigation Search Test**  
  This test uses the search icon in the bottom tab of the Pyng UI.  
  The agent searched for "decorator" and correctly returned a matching result.  
  ✅ Passed.

<h3>Search Tab Screenshot</h3>
<img width="100%" alt="Homepage Test Screenshot" src="https://github.com/user-attachments/assets/0f75d409-a53d-437a-9866-7b2d87c7a975" />


