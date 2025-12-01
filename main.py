import os
import sys
import concurrent.futures
from dotenv import load_dotenv
from agents.openalex_agent import OpenAlexAgent
from agents.arxiv_agent import ArxivAgent
from agents.merger_agent import MergerAgent
from agents.reporter_agent import ReporterAgent
from agents.email_agent import EmailAgent

def main():
    # Load environment variables
    load_dotenv()
    
    print("Welcome to ARXIVISION - AI-Powered Academic Intelligence Multi-Agent System")
    print("---------------------------------------------------")
    
    # Get user input
    if len(sys.argv) > 1:
        keywords = sys.argv[1]
        email = sys.argv[2] if len(sys.argv) > 2 else "test@example.com"
    else:
        keywords = input("Enter keywords to search for: ")
        email = input("Enter your email address: ")
        
    print(f"\nStarting research on: '{keywords}'")
    print(f"Report will be sent to: {email}\n")
    
    # Initialize Agents
    openalex_agent = OpenAlexAgent()
    arxiv_agent = ArxivAgent()
    merger_agent = MergerAgent()
    reporter_agent = ReporterAgent()
    email_agent = EmailAgent()
    
    # 1. Search in Parallel
    print("Starting parallel search...")
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_openalex = executor.submit(openalex_agent.search, keywords)
        future_arxiv = executor.submit(arxiv_agent.search, keywords)
        
        openalex_results = future_openalex.result()
        arxiv_results = future_arxiv.result()
    
    # 2. Merge
    merged_results = merger_agent.merge(openalex_results, arxiv_results, limit=10)
    
    if not merged_results:
        print("No papers found matching the criteria.")
        return

    # Print Merged Papers List: Title (Year) [Source]
    print("\nMerged Papers List:")
    for paper in merged_results:
        year = paper.get('date', 'Unknown')[:4] if paper.get('date') else 'Unknown'
        source = paper.get('source', 'Unknown')
        print(f"- {paper['title']} ({year}) [{source}]")
    print("\n")

    # 3. Generate Report
    report_content = reporter_agent.create_report(merged_results, keywords)
    
    # 4. Send Report via Email
    email_agent.send_report(email, report_content)
    
    print("\nWorkflow completed successfully.")

if __name__ == "__main__":
    main()
