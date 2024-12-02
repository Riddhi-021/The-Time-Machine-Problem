# british.py

import logging
from datasets import load_dataset
from pathlib import Path
import json
import random

class BritishLibraryExtractor:
    def __init__(self):
        self.periods = {
            "1500-1550": (1500, 1550),
            "1551-1600": (1551, 1600),
            "1601-1650": (1601, 1650),
            "1651-1700": (1651, 1700),
            "1701-1750": (1701, 1750),
            "1751-1800": (1751, 1800),
            "1801-1850": (1801, 1850),
            "1851-1900": (1851, 1900)
        }
        self.articles_by_period = {period: [] for period in self.periods.keys()}
        self.output_dir = Path(__file__).parent / 'selected_british_books'
        self.ocr_threshold = 0.7
        self.max_articles_per_period = 100

    def process_books(self):
        logging.info("Loading British Library Books dataset...")
        try:
            dataset = load_dataset("TheBritishLibrary/blbooks", 
                                 "1500_1899",
                                 trust_remote_code=True)
            
            for period, (start_year, end_year) in self.periods.items():
                logging.info(f"Processing period {period}")
                period_books = [
                    book for book in dataset['train'] 
                    if start_year <= book['date'] <= end_year 
                    and book['mean_wc_ocr'] >= self.ocr_threshold
                    and not book['empty_pg']
                ]
                
                selected_books = period_books[:self.max_articles_per_period]
                if len(period_books) > self.max_articles_per_period:
                    selected_books = random.sample(period_books, self.max_articles_per_period)
                
                for book in selected_books:
                    book_info = {
                        'record_id': book['record_id'],
                        'title': book['title'],
                        'date': book['date'],
                        'text': book['text'],
                        'language': book['Language_1'],
                        'place': book['place'],
                        'publisher': book['Publisher'],
                        'ocr_quality': book['mean_wc_ocr']
                    }
                    self.articles_by_period[period].append(book_info)
                
                logging.info(f"Selected {len(selected_books)} books for period {period}")
        except Exception as e:
            logging.error(f"Failed to load dataset: {str(e)}")
            raise

    def save_selected_books(self):
        self.output_dir.mkdir(exist_ok=True)
        
        for period, books in self.articles_by_period.items():
            output_file = self.output_dir / f'books_{period}.json'
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(books, f, indent=2, ensure_ascii=False)
            logging.info(f"Saved {len(books)} books for period {period} to {output_file}")

def extract_british_books():
    try:
        extractor = BritishLibraryExtractor()
        extractor.process_books()
        extractor.save_selected_books()
        logging.info("Successfully extracted British Library books")
    except Exception as e:
        logging.error(f"Error extracting books: {str(e)}")
        raise

if __name__ == "__main__":
    extract_british_books()