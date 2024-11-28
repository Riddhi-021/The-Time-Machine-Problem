import json
import matplotlib.pyplot as plt
import re
from collections import defaultdict
import seaborn as sns
from pathlib import Path
import logging
import pandas as pd
import numpy as np
import random

def extract_year_from_paper(paper):
    # Try to get year from journal reference first
    journal_ref = paper.get('journal-ref')
    if journal_ref:
        try:
            # Common format: "Phys.Rev.D76:013009,2007"
            year_match = re.search(r',(\d{4})', journal_ref)
            if year_match:
                year = int(year_match.group(1))
                if 1900 <= year <= 2024:  # Allow older papers
                    return year
        except (ValueError, IndexError):
            pass
    
    # If no journal ref, try DOI as backup
    doi = paper.get('doi')
    if doi:
        try:
            # DOIs sometimes contain years
            year_match = re.search(r'(?:19|20)\d{2}', doi)
            if year_match:
                year = int(year_match.group())
                if 1900 <= year <= 2024:
                    return year
        except (ValueError, IndexError):
            pass
    return None

class ArxivVisualizer:
    def __init__(self, json_path):
        self.json_path = Path(json_path)
        self.years_data = defaultdict(int)
        self.categories_data = defaultdict(int)
        self.output_dir = self.json_path.parent

    def extract_year(self, paper):
        return extract_year_from_paper(paper)

    def process_data(self):
        logging.info("Starting to process arXiv data for visualization...")
        paper_count = 0
        with open(self.json_path, 'r') as f:
            for line in f:
                paper = json.loads(line)
                paper_count += 1
                if paper_count % 10000 == 0:
                    logging.info(f"Processed {paper_count} papers...")
                
                year = self.extract_year(paper)
                if year:
                    self.years_data[year] += 1
                    
                categories = paper.get('categories', '').split()
                if categories:
                    primary_cat = categories[0]
                    main_category = self._get_main_category(primary_cat)
                    if main_category:
                        self.categories_data[main_category] += 1
        logging.info(f"Finished processing {paper_count} papers for visualization")

    def _get_main_category(self, category):
        category_map = {
            'astro-ph': 'Astrophysics',
            'cond-mat': 'Condensed Matter',
            'gr-qc': 'General Relativity',
            'hep-': 'High Energy Physics',
            'math': 'Mathematics',
            'nlin': 'Nonlinear Sciences',
            'nucl-': 'Nuclear',
            'physics': 'Physics',
            'quant-ph': 'Quantum Physics',
            'cs': 'Computer Science',
            'stat': 'Statistics',
            'q-bio': 'Quantitative Biology',
            'q-fin': 'Quantitative Finance',
            'econ': 'Economics'
        }
        
        for prefix, name in category_map.items():
            if category.startswith(prefix):
                return name
        return 'Other'

    def create_visualizations(self):
        plt.style.use('default')
        
        # 1. Year Distribution (Line Plot)
        plt.figure(figsize=(12, 6))
        years = sorted(self.years_data.keys())
        counts = [self.years_data[year] for year in years]
        plt.plot(years, counts, marker='o', linewidth=2)
        plt.title('Distribution of arXiv Papers by Year')
        plt.xlabel('Year')
        plt.ylabel('Number of Papers')
        plt.grid(True)
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(self.output_dir / 'year_distribution.png')
        plt.close()

        # 2. Year Distribution (Bar Plot)
        plt.figure(figsize=(12, 6))
        plt.bar(years, counts, alpha=0.8)
        plt.title('Distribution of arXiv Papers by Year (Bar Chart)')
        plt.xlabel('Year')
        plt.ylabel('Number of Papers')
        plt.xticks(rotation=45)
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig(self.output_dir / 'year_distribution_bar.png')
        plt.close()
        
        # 3. Modified Category Distribution
        plt.figure(figsize=(12, 8))
        top_categories = dict(sorted(self.categories_data.items(), 
                                  key=lambda x: x[1], 
                                  reverse=True))
        colors = plt.cm.viridis(np.linspace(0, 0.8, len(top_categories)))
        plt.barh(list(top_categories.keys()), list(top_categories.values()),
                color=colors)
        plt.title('arXiv Papers by Main Category')
        plt.xlabel('Number of Papers')
        plt.tight_layout()
        plt.savefig(self.output_dir / 'category_distribution.png')
        plt.close()

        # 4. Modified Heatmap - Decade-based
        plt.figure(figsize=(15, 8))
        decades = {}
        for year, count in sorted(self.years_data.items()):
            decade = f"{year//10*10}s"
            if decade not in decades:
                decades[decade] = {}
            decades[decade][year % 10] = count
        
        decade_df = pd.DataFrame(decades).fillna(0)
        decade_df.index = range(10)
        
        sns.heatmap(decade_df, 
                    cmap='YlOrRd',
                    fmt='.0f',
                    annot=True,
                    cbar_kws={'label': 'Number of Papers'})
        plt.title('Publication Distribution by Decade')
        plt.xlabel('Decade')
        plt.ylabel('Year within Decade')
        plt.tight_layout()
        plt.savefig(self.output_dir / 'decade_heatmap.png')
        plt.close()

class ArxivPaperExtractor:
    def __init__(self, json_path):
        self.json_path = Path(json_path)
        self.papers_by_period = {
            "1900-1950": [],
            "1950-2000": [],
            "2000+": []
        }
    
    def get_period(self, year):
        if 1900 <= year < 1950:
            return "1900-1950"
        elif 1950 <= year < 2000:
            return "1950-2000"
        elif 2000 <= year <= 2024:
            return "2000+"
        return None

    def extract_year(self, paper):
        return extract_year_from_paper(paper)

    def process_papers(self):
        logging.info("Starting to process arXiv data for paper extraction...")
        paper_count = 0
        with open(self.json_path, 'r') as f:
            for line in f:
                paper = json.loads(line)
                paper_count += 1
                if paper_count % 10000 == 0:
                    logging.info(f"Processed {paper_count} papers...")
                
                year = self.extract_year(paper)
                if year:
                    period = self.get_period(year)
                    if period:
                        paper_info = {
                            'title': paper.get('title', ''),
                            'authors': paper.get('authors', ''),
                            'year': year,
                            'abstract': paper.get('abstract', ''),
                            'categories': paper.get('categories', ''),
                            'journal-ref': paper.get('journal-ref', '')
                        }
                        self.papers_by_period[period].append(paper_info)
        logging.info(f"Finished processing {paper_count} papers for extraction")

    def save_selected_papers(self):
        output_dir = self.json_path.parent / 'selected_papers'
        output_dir.mkdir(exist_ok=True)
        
        for period, papers in self.papers_by_period.items():
            selected = papers if len(papers) <= 100 else random.sample(papers, 100)
            output_file = output_dir / f'papers_{period.replace("+", "plus")}.json'
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(selected, f, indent=2, ensure_ascii=False)
            logging.info(f"Saved {len(selected)} papers for period {period} to {output_file}")

def visualize_arxiv_data():
    try:
        json_path = Path(__file__).parent.parent.parent / 'datasets' / 'arxiv' / 'arxiv-metadata-oai-snapshot.json'
        visualizer = ArxivVisualizer(json_path)
        visualizer.process_data()
        visualizer.create_visualizations()
        logging.info("Successfully created arXiv visualizations")
    except Exception as e:
        logging.error(f"Error creating visualizations: {str(e)}")

def extract_random_papers():
    try:
        json_path = Path(__file__).parent.parent.parent / 'datasets' / 'arxiv' / 'arxiv-metadata-oai-snapshot.json'
        extractor = ArxivPaperExtractor(json_path)
        extractor.process_papers()
        extractor.save_selected_papers()
        logging.info("Successfully extracted random papers from different time periods")
    except Exception as e:
        logging.error(f"Error extracting papers: {str(e)}")