import logging
from datasets import load_dataset
from pathlib import Path
import json
import random
import os
from huggingface_hub import login

class AmericanStoriesExtractor:
    def __init__(self):
        self._authenticate()
        self.periods = {
            "pre-1800": ["1774", "1799", "1800"],
            "1800-1850": ["1805", "1815", "1825", "1835", "1845"],
            "1850-1900": ["1855", "1865", "1875", "1885", "1895"],
            "1900-1950": ["1905", "1915", "1925", "1935", "1945"],
            "1950+": ["1955", "1960", "1963"]
        }
        self.stories_by_period = {period: [] for period in self.periods.keys()}
        self.output_dir = Path(__file__).parent / 'selected_stories'
    
    def _authenticate(self):
        """Authenticate with Hugging Face using token from environment variable."""
        token = os.getenv('HUGGINGFACE_TOKEN')
        if not token:
            raise ValueError("HUGGINGFACE_TOKEN environment variable not set")
        try:
            login(token)
            logging.info("Successfully authenticated with Hugging Face")
        except Exception as e:
            raise RuntimeError(f"Failed to authenticate with Hugging Face: {str(e)}")
        
    def process_stories(self):
        for period, years in self.periods.items():
            logging.info(f"Processing period {period} with years {years}")
            try:
                dataset = load_dataset("dell-research-harvard/AmericanStories",
                                     "subset_years",
                                     year_list=years)
                
                for year in years:
                    if year in dataset:
                        for story in dataset[year]:
                            story_info = {
                                'article_id': story['article_id'],
                                'newspaper_name': story['newspaper_name'],
                                'date': story['date'],
                                'headline': story['headline'],
                                'article': story['article'],
                                'year': year
                            }
                            self.stories_by_period[period].append(story_info)
                            
                logging.info(f"Collected {len(self.stories_by_period[period])} stories for period {period}")
            except Exception as e:
                logging.error(f"Error processing period {period}: {str(e)}")

    def save_selected_stories(self):
        self.output_dir.mkdir(exist_ok=True)
        
        for period, stories in self.stories_by_period.items():
            selected = stories if len(stories) <= 100 else random.sample(stories, 100)
            output_file = self.output_dir / f'stories_{period.replace("+", "plus")}.json'
            
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(selected, f, indent=2, ensure_ascii=False)
            logging.info(f"Saved {len(selected)} stories for period {period} to {output_file}")

def extract_american_stories():
    try:
        extractor = AmericanStoriesExtractor()
        extractor.process_stories()
        extractor.save_selected_stories()
        logging.info("Successfully extracted American stories from different time periods")
    except Exception as e:
        logging.error(f"Error extracting stories: {str(e)}")