# IQ Foreign Investment Process

This repository contains the IQ Foreign Investment Process project with the following structure:

## Project Structure

### Files/
- **BasePromptinEnglish.docx** - Base prompt document in English
- **IQTest.xlsx** - IQ test data in Excel format
- **ModifiedIQPrompt.docx** - Modified prompt document

### Project/
- **main.py** - Main application file
- **prompts.py** - Prompt handling and processing
- **ranking.py** - Ranking algorithms and logic
- **create_env.py** - Environment setup script
- **IQTest.csv** - IQ test data in CSV format
- **output.csv** - Output data
- **output_5Aug.csv** - Output data from August 5th

## Setup

1. Clone this repository
2. Install Python dependencies
3. Set up your OpenAI API key:
   - Create a `.env` file in the Project/ directory
   - Add: `OPENAI_API_KEY=your_actual_api_key_here`
   - Or run `python Project/create_env.py` and edit the file with your key
4. Run `python Project/main.py` to start the application

## Data Files

The project includes various CSV and Excel files for testing and data processing:
- IQ test datasets
- Output results
- Prompt documents for processing

## Requirements

- Python 3.x
- Required packages (see requirements.txt if available)
