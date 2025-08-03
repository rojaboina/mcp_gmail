

# MCP Gmail Server (Beginner-Friendly Guide)

---


## 🧩 What is MCP (Model Context Protocol) and Why Use It Here?

### Fundamental Concepts of MCP

- **Tool Discovery:** MCP servers describe their capabilities (endpoints, parameters, descriptions) in a way that LLMs and clients can automatically discover and understand what the server can do.
- **Standardized Endpoints:** MCP encourages clear, consistent endpoint naming and documentation, so any client (human or AI) knows how to interact with your API.
- **Context Passing:** MCP servers are designed to receive and process context (like user queries, previous messages, or data) from LLMs, making them more useful in AI workflows.
- **Interoperability:** MCP makes it easy to plug your server into different LLMs, chatbots, or automation tools, because the protocol is standardized and widely supported.
- **Security and Permissions:** MCP-aware servers can expose only the capabilities you want, and can require authentication or permissions for sensitive actions.
- **Extensibility:** You can add new endpoints or capabilities to your MCP server, and clients will be able to discover and use them without manual updates.

**In short:** MCP is about making your backend "AI-native"—so it can be used as a tool by language models, agents, and other smart clients, with minimal friction and maximum clarity.

**Model Context Protocol (MCP)** is a standard for building AI-powered backend services that can be easily integrated with language models and other AI tools. MCP defines how a server should expose its capabilities (like reading emails, summarizing, etc.) in a way that is discoverable and usable by LLMs and other clients.

**Why use MCP in this project?**
- It makes your backend "AI-ready"—so LLMs (like GPT, Gemini, etc.) can call your endpoints, understand their purpose, and use them as tools.
- It encourages clear, well-documented, and modular API design.
- It helps you build services that can be plugged into larger AI workflows, chatbots, or automation systems.

**How is MCP used here?**
- The project is structured as an MCP server, following conventions for endpoint naming, documentation, and discoverability.
- Endpoints like `/auth/gmail`, `/emails`, and `/summarize` are designed to be easily called by LLMs or other MCP-compatible clients.
- The code and README follow best practices from the [MCP reference SDK](https://github.com/modelcontextprotocol/create-python-server) and [MCP documentation](https://modelcontextprotocol.io/llms-full.txt).

**In summary:**
MCP makes your API more useful, future-proof, and ready for integration with the next generation of AI tools and assistants. This project is a practical example of how to build such a service from scratch.

Welcome! This project is a hands-on, real-world example of a Model Context Protocol (MCP) server that connects to Gmail, fetches emails, and summarizes them using OpenAI. It is designed for computer science beginners and will help you understand modern backend development, APIs, authentication, and AI integration.

---

## 🚀 What Does This Project Do?

- Lets you log in to your Gmail account securely (OAuth2)
- Fetches your emails (with a search filter, e.g., from Spotify)
- Uses OpenAI (GPT) to summarize the content of those emails
- Exposes all this as a web API (using FastAPI)

---

## 🧑‍💻 How to Run This Project

1. **Clone the repo and open in VS Code**
2. **Create a virtual environment**
   ```sh
   python3 -m venv .venv
   source .venv/bin/activate
   ```
3. **Install dependencies**
   ```sh
   pip install -r requirements.txt
   ```
4. **Get your Gmail API credentials**
   - Go to Google Cloud Console, enable Gmail API, create OAuth2 credentials, and download `credentials.json` to the project root.
5. **Set your OpenAI API key**
   ```sh
   export OPENAI_API_KEY=sk-...your-key-here
   ```
6. **Run the server**
   ```sh
   OAUTHLIB_INSECURE_TRANSPORT=1 uvicorn mcp_gmail.main:app --reload --port 8001
   ```
7. **Authenticate with Gmail**
   - Visit [http://localhost:8001/auth/gmail](http://localhost:8001/auth/gmail) and follow the login flow.
8. **Fetch and summarize emails**
   - Visit [http://localhost:8001/summarize](http://localhost:8001/summarize) to get a summary of your Spotify emails.

---

## 🛠️ Key Concepts Used (with Interview-Ready Explanations)

### 1. **FastAPI**
- A modern, fast (high-performance) web framework for building APIs with Python 3.7+.
- Uses Python type hints for data validation and documentation.
- Interview tip: Know how to define endpoints, use decorators (`@app.get`), and return JSON responses.

### 2. **OAuth2 Authentication**
- A secure protocol for authorizing access to user data without sharing passwords.
- Used here to let users log in to Gmail and grant access to their emails.
- Interview tip: Understand the OAuth2 flow (authorization URL, redirect URI, token exchange).

### 3. **Google APIs (Gmail API)**
- RESTful APIs provided by Google to access Gmail, Drive, etc.
- Here, we use the Gmail API to search and fetch emails.
- Interview tip: Know how to use client libraries, authenticate, and make API calls.

### 4. **Environment Variables**
- Used to store sensitive info (like API keys) outside your codebase.
- Interview tip: Know how to set and access environment variables in Python (`os.getenv`).

### 5. **OpenAI API (LLM Integration)**
- Connects to GPT models to generate or summarize text.
- Here, we send email content to OpenAI and get a summary back.
- Interview tip: Know how to call external APIs, handle responses, and manage API keys securely.

### 6. **Virtual Environments**
- Isolate project dependencies from your global Python installation.
- Interview tip: Know how to create, activate, and use `venv`.

### 7. **JSON and REST APIs**
- Data is exchanged in JSON format.
- RESTful endpoints (`/auth/gmail`, `/emails`, `/summarize`) follow standard HTTP methods.
- Interview tip: Know the basics of REST, HTTP verbs, and JSON serialization.

### 8. **Error Handling**
- The project returns clear error messages for missing authentication, invalid credentials, or missing API keys.
- Interview tip: Always handle exceptions and return user-friendly errors in APIs.

### 9. **Base64 Decoding**
- Gmail API returns email bodies encoded in base64.
- We decode them to get the plain text.
- Interview tip: Know how to encode/decode base64 in Python.


- `mcp_gmail/` contains the main code.
- `.github/` for Copilot instructions.
- `.vscode/` for VS Code tasks and settings.
- `requirements.txt` for dependencies.
- `.vscode/mcp.json`: Declares how to launch your MCP server for tools and extensions that support the Model Context Protocol. It specifies the server name, type, and the command/arguments to start your server. This enables MCP-compatible tools (like LLMs, dev tools, or orchestrators) to discover and launch your server automatically.
- `.vscode/tasks.json`: Defines custom tasks for VS Code, such as running your server. It lets you start your server with one click from the VS Code UI, ensuring the right environment and command are used every time.

---

##  Questions You Can Answer After This Project


### 1. How does OAuth2 work and why is it important?
OAuth2 is an industry-standard protocol for authorization. It lets users grant applications access to their data (like Gmail) without sharing their password. The app redirects the user to a Google login page, the user logs in and approves access, and the app receives a token to access the data. This keeps user credentials safe and allows for fine-grained permissions.

### 2. How do you build and document REST APIs in Python?
You can use frameworks like FastAPI or Flask. FastAPI lets you define endpoints using decorators (e.g., `@app.get("/endpoint")`). It automatically generates interactive documentation (Swagger UI) at `/docs` based on your code and type hints, making it easy to test and understand your API.

### 3. How do you securely manage API keys and secrets?
Never hard-code secrets in your code. Store them in environment variables or secret management tools. Access them in Python using `os.getenv("KEY_NAME")`. Add sensitive files (like `.env`, `credentials.json`) to `.gitignore` so they are not pushed to public repositories.

### 4. How do you use the Gmail API to fetch emails?
First, authenticate using OAuth2 to get access tokens. Then, use the Google API Python client to build a Gmail service object. Call `service.users().messages().list(userId='me')` to get message IDs, and `service.users().messages().get(userId='me', id=msg_id)` to fetch email details.

### 5. How do you integrate an LLM (like OpenAI) into a backend service?
Sign up for an API key at OpenAI. Use the OpenAI Python SDK to send a prompt (your email content) to the model and receive a summary or answer. Always keep your API key secure and never expose it in public code.

**Where in this project?**
- File: `mcp_gmail/main.py`
- Endpoint: `/summarize`
- Key lines:
  - `from openai import OpenAI`
  - `OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")`
  - `client = OpenAI(api_key=OPENAI_API_KEY)`
  - `response = client.chat.completions.create(...)`
  - `summary = response.choices[0].message.content.strip()`
This is where the email content is sent to OpenAI and the summary is returned.

**Common Error: 429 - insufficient_quota**

If you see an error like:
```json
{"error":"Error code: 429 - {'error': {'message': 'You exceeded your current quota, please check your plan and billing details. For more information on this error, read the docs: https://platform.openai.com/docs/guides/error-codes/api-errors.', 'type': 'insufficient_quota', 'param': None, 'code': 'insufficient_quota'}}"}
```
It means your OpenAI account has run out of free or paid quota for API usage. You need to check your OpenAI account's usage, plan, and billing details at https://platform.openai.com/account/usage and https://platform.openai.com/account/billing. You can resolve this by upgrading your plan or waiting for your quota to reset.

### 6. What is a virtual environment and why use it?
A virtual environment (`venv`) is an isolated Python environment for a project. It keeps dependencies required by different projects separate, avoiding version conflicts and making your project easier to manage and share.

### 7. How do you handle errors and edge cases in web APIs?
Always check for possible errors (like missing authentication, invalid input, or failed API calls). Use try/except blocks and return clear, user-friendly error messages with appropriate HTTP status codes (e.g., 400 for bad request, 401 for unauthorized).

### 8. How do you decode base64 data in Python?
Use the built-in `base64` module. For example:
```python
import base64
decoded = base64.urlsafe_b64decode(encoded_data).decode('utf-8')
```
This is needed because Gmail API returns email bodies encoded in base64.

### 9. How do you structure a modern Python project for maintainability?
Organize code into logical folders (e.g., `mcp_gmail/` for app code). Use a `requirements.txt` for dependencies, `.gitignore` for sensitive files, and keep configuration (like API keys) outside your code. Write clear documentation and use version control (git) for collaboration and history.

---

## 📝 Further Reading & Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Google Gmail API Python Quickstart](https://developers.google.com/gmail/api/quickstart/python)
- [OpenAI API Reference](https://platform.openai.com/docs/api-reference)
- [OAuth2 Explained](https://oauth.net/2/)
- [Python venv Guide](https://docs.python.org/3/library/venv.html)

---

## 💡 Final Tips

- Practice explaining each concept in your own words.
- Try changing the email filter or prompt to summarize different emails.
- Experiment with adding new endpoints or features.
- Use this project as a portfolio piece and talk about it in interviews!

---

Happy learning and good luck with your interviews!
