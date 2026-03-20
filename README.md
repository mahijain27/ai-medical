# CrewAI Implementation

## Overview

This project implements a CrewAI setup with two agents: a `Doctor` and a `Researcher`. The goal is to analyze a blood test report and provide health recommendations based on the analysis and relevant online research.

- **Doctor Agent**: Analyzes the blood test report provided as a PDF.
- **Researcher Agent**: Searches the internet for articles that fit the person’s needs and makes health recommendations based on the Doctor’s analysis.

## Project Structure

- **`health-check-recommendations`**: Contains the implementation of the CrewAI setup, including the definition of agents and tasks.
- **`README.md`**: The file you are currently reading.
- **Dependencies**: External libraries used for PDF processing and web requests.

## How to Run the Code

### 1. Clone the Repository
```bash
git clone https://github.com/mahijain27/ai-medical
cd health-check
```

### 2. Install Dependencies

Make sure you have Python 3.7+ installed. Then install the required libraries:
```bash
pip install crewai crewai_tools pdfplumber urllib3 requests
```

### 3. Set Up Your Environment

Replace `"YOUR_OPENAI_API_KEY"` in the `health-check-recommendations` file with your actual OpenAI API key:
```python
os.environ["OPENAI_API_KEY"] = "YOUR_OPENAI_API_KEY"
```

### 4. Run the Script

Execute the script using the following command:
```bash
python health-check.py
```

### 5. Expected Output

- The `Doctor` agent will analyze the blood test report linked in the code.
- The `Researcher` agent will search for relevant health information on the internet and provide links to useful articles.
- The output will be printed in the console, showing the results of the analysis and the recommendations.

## Code Explanation

### Agents

- **Doctor Agent**: Reads and analyzes the blood test report. This agent uses `pdfplumber` to extract text from the provided PDF and then performs an analysis based on the extracted data.
- **Researcher Agent**: Performs a web search using the DuckDuckGo API and provides health recommendations based on the Doctor’s findings.

### Tasks

- **Task 1**: Investigates the blood test report using the `Doctor` agent.
- **Task 2**: Uses the `Researcher` agent to find articles related to the health needs identified in the blood report.

### PDF Handling

The PDF report is fetched from the provided URL, and its contents are read using the `pdfplumber` library. This text is then processed by the `Doctor` agent.

### Web Search

The `Researcher` agent uses a custom `WebSearch` tool to query the DuckDuckGo API for relevant articles. If successful, the search results are returned and analyzed for health recommendations.

## Notes

- **PDF File**: Ensure that the PDF file is accessible via the provided link. If the link is broken, update the `report_file_link` variable with a working URL.
- **Web Search**: The DuckDuckGo API may have limitations; consider using other APIs or methods if needed.

## Potential Improvements

- **Enhanced PDF Parsing**: Implement more advanced parsing techniques to extract structured data from the PDF.
- **Error Handling**: Improve error handling, especially in the web search functionality.
- **More Agents**: Consider adding more agents for specific tasks, such as diet recommendations or exercise plans.

---
