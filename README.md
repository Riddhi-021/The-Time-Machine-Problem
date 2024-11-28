# The Time Machine Problem

## Project Overview
This project analyzes historical text data across different time periods. It utilizes datasets from arXiv papers and American stories to visualize and understand trends over time.

## Project Structure
- `data_processors/`: Contains modules for processing different datasets.
  - `americanstories/`: Processes American stories from various periods.
  - `arxiv/`: Processes academic papers from the arXiv repository.
- `main.py`: The main script to run analyses.

## Setup
To set up the project, you need to install the required Python packages:
```
pip install -r requirements.txt
```
## Running the Project
To run the project, execute the following command:
```
python main.py
```
This will process the datasets and generate visualizations based on the analysis. Because the arXiv data and American Stories are already processed and saved, you can skip the arXiv processing and American Stories processing by commenting out the relevant lines in `main.py`. 

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
