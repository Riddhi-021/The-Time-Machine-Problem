# The Time Machine Problem

## Project Overview
This project analyzes historical text data across different time periods. It utilizes datasets from arXiv papers and American stories to visualize and understand trends over time.

## Project Structure
- `data_processors/`: Contains modules for processing different datasets.
  - `americanstories/`: Processes American stories from various periods.
    - `americanstories.py`: Processes American stories from various periods from [American Stories](https://huggingface.co/datasets/dell-research-harvard/AmericanStories).
    - `selected_stories/`: Contains randomly selected American stories from the `americanstories.py` output.
  - `arxiv/`: Processes academic papers from the arXiv repository.
    - `arxiv.py`: Processes academic papers from the arXiv repository from [arXiv](https://www.kaggle.com/datasets/Cornell-University/arxiv/data).
    - `selected_papers/`: Contains randomly selected arXiv papers from the `arxiv.py` output.
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

If you want to run the arXiv and American Stories data and visualizations, you can do so by uncommenting the relevant lines in `main.py`.

For the arXiv data, you need to download the [arXiv dataset](https://www.kaggle.com/datasets/Cornell-University/arxiv/data) and save it in the `datasets/arxiv` folder before running the project.

For the American Stories data, you need to set the hugging face token "HUGGINGFACE_TOKEN" from [Hugging Face tokens page](https://huggingface.co/settings/tokens) before running the project.

windows:
```
set HUGGINGFACE_TOKEN=<your_token>
```

mac/linux:
```
export HUGGINGFACE_TOKEN=<your_token>
```

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
