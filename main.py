import os
import sys

# Add the project root directory to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)

from data_processors.arxiv.arxiv import visualize_arxiv_data, extract_random_papers
from data_processors.americanstories.americanstories import extract_american_stories
import logging

def main():
    # Set up logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    
    # Comment out arxiv processing as it's already done
    # visualize_arxiv_data()
    # extract_random_papers()
    
    # Extract American Stories
    extract_american_stories()

if __name__ == "__main__":
    main()