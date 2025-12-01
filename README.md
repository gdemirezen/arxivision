# ARXIVISION - AI-Powered Academic Intelligence Multi-Agent System

This system uses a team of AI agents to search for recent academic papers, summarize them, and email a report to the user.

## Features
- **OpenAlex Search**: Finds papers from the last week using the OpenAlex API.
- **Arxiv Search**: Finds papers from the last week using the Arxiv API.
- **Parallel Execution**: Searches run concurrently for improved performance.
- **Merging**: Merges results from multiple sources and limits to the top 10 most relevant papers.
- **AI Reporting**: Generates a concise 1-page summary with APA 7 references using Google Gemini.
- **Email Delivery**: Sends the curated report directly to your inbox via SMTP (with fallback to mock console output).

## Agents
1. **OpenAlexAgent**: Interfaces with OpenAlex API.
2. **ArxivAgent**: Interfaces with Arxiv API.
3. **MergerAgent**: Merges and limits data.
4. **ReporterAgent**: Uses LLM to write the report.
5. **EmailAgent**: Handles delivery via SMTP.

## Setup

1. **Clone the repository**
2. **Create Virtual Environment (Python 3.12+)**:
   ```bash
   python3.12 -m venv .venv
   source .venv/bin/activate
   ```
3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
4. **Environment Variables**:
   Create a `.env` file in the root directory and add your Google API Key and optional Email credentials:
   ```
   GOOGLE_API_KEY=your_api_key_here
   
   # Optional: For real email sending
   SMTP_SERVER=smtp.gmail.com
   SMTP_PORT=587
   SMTP_EMAIL=your_email@gmail.com
   SMTP_PASSWORD=your_app_password
   ```

   You can use env.example as a template to create your .env file.
   ```
   cp .env.example .env
   ```

## Usage

Run the agent interactively:
```bash
python main.py
```
You will be prompted to enter:
1. **Keywords**: The research topic you want to search for (e.g., "Large Language Models", "Quantum Computing").
2. **Email**: The recipient email address for the report.

Or pass arguments directly via the command line:
```bash
python main.py "Large Language Models" "user@example.com"
```
- **Argument 1**: Search keywords.
- **Argument 2**: Recipient email address.

## Structure
- `main.py`: Entry point and orchestration.
- `tools/`: Low-level tool implementations.
- `agents/`: Agent classes wrapping tools.
