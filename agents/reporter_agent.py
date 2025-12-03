import os
import asyncio
from typing import List, Dict
from google.adk import Agent, Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

class ReporterAgent:
    def __init__(self, model_name: str = "gemini-2.5-flash"):
        self.model_name = model_name
        self.session_service = InMemorySessionService()
        
    async def _create_report_async(self, papers: List[Dict], keywords: str) -> str:
        """Async implementation of report generation."""
        if not papers:
            return "No papers found to report on."

        # Prepare context for the LLM
        papers_context = ""
        for i, p in enumerate(papers, 1):
            papers_context += f"{i}. Title: {p['title']}\n   Authors: {', '.join(p['authors'])}\n   Abstract: {p['abstract']}\n   Source: {p['source']}\n   URL: {p['url']}\n\n"

        instruction = f"""
        You are an academic reporter. Your task is to write a weekly research update email based on the following papers related to "{keywords}".
        
        The email should:
        1. Curate and summarize the research developments from these papers.
        2. Be at most 1 page long.
        3. Include a reference list in APA 7 style at the end containing ALL provided papers, even if not explicitly discussed in the text.
        4. Highlight (bold) key terms related to the topic: '{keywords}' within the text.
        5. End the email with "Search Keywords: {keywords}".
        6. Sign off with "Sincerely,"
        7. Add signature as "ARXIVISION - Your Weekly AI-Powered Academic Intelligence".
        """
        
        try:
            max_retries = 3
            retry_delay = 60
            
            for attempt in range(max_retries):
                try:
                    # Create agent with instruction
                    agent = Agent(
                        name="reporter",
                        model=self.model_name,
                        instruction=instruction
                    )
                    
                    # Create runner
                    runner = Runner(
                        agent=agent,
                        session_service=self.session_service,
                        app_name="agents"
                    )
                    
                    # Create or get session
                    session = self.session_service.create_session_sync(
                        app_name="agents",
                        user_id="arxivision_user"
                    )
                    
                    # Create user message with papers context
                    user_message = types.Content(
                        role="user",
                        parts=[types.Part(text=f"Papers:\n{papers_context}\n\nGenerate the email content now.")]
                    )
                    
                    # Run agent asynchronously
                    response_text = ""
                    async for event in runner.run_async(
                        user_id="arxivision_user",
                        session_id=session.id,
                        new_message=user_message
                    ):
                        if event.content and event.content.parts:
                            for part in event.content.parts:
                                if part.text:
                                    response_text += part.text
                    
                    return response_text
                    
                except Exception as e:
                    error_msg = str(e)
                    if "RESOURCE_EXHAUSTED" in error_msg and attempt < max_retries - 1:
                        print(f"Rate limit hit. Waiting {retry_delay} seconds before retry {attempt + 2}/{max_retries}...")
                        await asyncio.sleep(retry_delay)
                        retry_delay *= 2  # Exponential backoff
                    else:
                        raise  # Re-raise if not rate limit or last attempt
                            
            return response_text
        except Exception as e:
            return f"Error generating report: {e}"

    def create_report(self, papers: List[Dict], keywords: str) -> str:
        print("ReporterAgent: Generating report...")
        return asyncio.run(self._create_report_async(papers, keywords))
