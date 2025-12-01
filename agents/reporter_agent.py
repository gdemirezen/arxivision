import os
import google.generativeai as genai
from typing import List, Dict

class ReporterAgent:
    def __init__(self, model_name: str = "gemini-2.5-flash"):
        api_key = os.environ.get("GOOGLE_API_KEY")
        if not api_key:
            print("Warning: GOOGLE_API_KEY not found in environment variables.")
        else:
            genai.configure(api_key=api_key)
            
        self.model = genai.GenerativeModel(model_name)

    def create_report(self, papers: List[Dict], keywords: str) -> str:
        print("ReporterAgent: Generating report...")
        
        if not papers:
            return "No papers found to report on."

        # Prepare context for the LLM
        papers_context = ""
        for i, p in enumerate(papers, 1):
            papers_context += f"{i}. Title: {p['title']}\n   Authors: {', '.join(p['authors'])}\n   Abstract: {p['abstract']}\n   Source: {p['source']}\n   URL: {p['url']}\n\n"

        prompt = f"""
        You are an academic reporter. Your task is to write a weekly research update email based on the following papers related to "{keywords}".
        
        The email should:
        1. Curate and summarize the research developments from these papers.
        2. Be at most 1 page long.
        3. Include a reference list in APA 7 style at the end containing ALL provided papers, even if not explicitly discussed in the text.
        4. Highlight (bold) key terms related to the topic: '{keywords}' within the text.
        5. End the email with "Search Keywords: {keywords}".
        6. Sign off with "Sincerely,"
        7. Add signature as "ARXIVISION - Your Weekly AI-Powered Academic Intelligence".
        
        Generate the email content now.
        """
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error generating report: {e}"
