from crewai import Agent, Task, Crew, Process
import os
import io
import requests
from crewai_tools import tool
import urllib3
import pdfplumber

os.environ["OPENAI_API_KEY"] = "YOUR_OPENAI_API_KEY"  # Replace with your API key

# Custom search tool implementation
@tool('WebSearch')
def search(search_query: str):
    """Search the web for information on a given topic using DuckDuckGo API"""

    print("search_querysearch_querysearch_querysearch_querysearch_querysearch_querysearch_querysearch_querysearch_querysearch_querysearch_querysearch_querysearch_querysearch_querysearch_querysearch_querysearch_querysearch_querysearch_querysearch_querysearch_querysearch_querysearch_querysearch_querysearch_querysearch_query")
    print(search_query)
    print("search_querysearch_querysearch_querysearch_querysearch_querysearch_querysearch_querysearch_querysearch_querysearch_querysearch_querysearch_querysearch_querysearch_querysearch_querysearch_querysearch_querysearch_querysearch_querysearch_querysearch_querysearch_querysearch_querysearch_querysearch_querysearch_query")
    url = f"https://api.duckduckgo.com/?q={search_query}&format=json"
    response = requests.get(url)
    if response.status_code == 200:
        results = response.json()
        return results.get('RelatedTopics', [])
    else:
        return f"Failed to retrieve results: {response.status_code}"

def process(self, task: Task):
    pdf_link = task.input_data.get('report_file_link')
    print("pdf_linkpdf_linkpdf_linkpdf_linkpdf_linkpdf_linkpdf_linkpdf_linkpdf_linkpdf_linkpdf_linkpdf_link")
    print(pdf_link)
    print("pdf_linkpdf_linkpdf_linkpdf_linkpdf_linkpdf_linkpdf_linkpdf_linkpdf_linkpdf_linkpdf_linkpdf_link")
    if pdf_link:
        try:
            report_text = self.read_pdf(pdf_link)
            print("report_textreport_textreport_textreport_textreport_textreport_textreport_text")
            print(report_text)
            print("report_textreport_textreport_textreport_textreport_textreport_textreport_text")
            if report_text:
                task.output_data = {"report_text": report_text}
            else:
                task.output_data = {"error": "Failed to extract text from the PDF"}
        except Exception as e:
            task.output_data = {"error": str(e)}
    else:
        task.output_data = {"error": "No PDF link provided"}
    self.complete_task(task)

def read_pdf(url):
    all_text = ''

    http = urllib3.PoolManager()
    temp = io.BytesIO()
    temp.write(http.request("GET", url).data)
    try:    # to verify is the url has valid pdf file!
        pdf = pdfplumber.open(temp)
        for pdf_page in pdf.pages:
            single_page_text = pdf_page.extract_text()
            # TypeError: can only concatenate str (not "NoneType") to str
            if single_page_text is not None: 
                all_text += '\n' + single_page_text
        pdf.close()
    except:
        pass
    return all_text

doctor = Agent(
    role="Doctor",
    goal="Read prescriptions and understand blood report of the patients using {report_file_data}",
    backstory="You are an expert doctor of blood count report analysis. Given the report you can provide the analysis",
    # allow_code_execution=True,
    verbose=True,
    allow_delegation=False
)

# Define the Researcher agent
researcher = Agent(
    role="Researcher",
    goal="Search the internet for articles to fit the person's needs. Make health recommendations based on what you find along with the links",
    backstory="You are an expert researcher of blood count reports",
    verbose=True,
    allow_delegation=False,
    tools=[search]
)

# File path or link to the PDF report
report_file_link = 'https://cdn1.lalpathlabs.com/live/reports/WM17S.pdf'

# Task for the Doctor agent to investigate the blood test report
task1 = Task(
    description='Investigate the blood test report',
    agent=doctor,
    input_data={'report_file_link': report_file_link},  # Pass the file link here
    expected_output='Blood test report investigated analysis'
)

# Task for the Researcher agent to search the internet and make health recommendations
task2 = Task(
    description='Search the internet for articles to fit the person needs based on the analysis provided as input. Make health recommendations based on what you find along with the links. If the results', 
    agent=researcher,
    expected_output='Suggest health recommendations based on what you find along with the links'
)

# Create and run the Crew
crew = Crew(
    agents=[doctor, researcher],
    tasks=[task1, task2],
    verbose=True,
    process=Process.sequential,
)

result = crew.kickoff(inputs={"report_file_data": read_pdf(report_file_link)})
# print(result)
