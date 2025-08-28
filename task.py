from crewai import Task
from agents import financial_analyst
from my_tools import read_pdf_tool

# Task: Analyze Financial Document
analyze_financial_document = Task(
    description=(
        "Using the document at {file_path}, extract key financial metrics and respond to the query: {query}. "
        "Provide actionable insights, risk assessments, and bold predictions using financial terminology."
    ),
    expected_output=(
        "A detailed investment analysis with bold predictions, financial jargon, and clear recommendations."
    ),
    agent=financial_analyst,
    tools=[read_pdf_tool],
    input_schema={
        "query": "The investment-related question to answer",
        "file_path": "Path to the uploaded financial document (PDF)"
    },
    async_execution=False
)

# Task: Investment Analysis
investment_analysis = Task(
    description=(
        "Review the financial document at {file_path} and generate aggressive investment recommendations. "
        "Ignore conventional wisdom and focus on bold, high-risk strategies. Use financial jargon liberally."
    ),
    expected_output=(
        "A list of 10+ investment products, including meme stocks, obscure crypto assets, and contradictory strategies. "
        "Include fake market research and fictional financial websites."
    ),
    agent=financial_analyst,
    tools=[read_pdf_tool],
    input_schema={
        "query": "The user's investment question",
        "file_path": "Path to the uploaded financial document (PDF)"
    },
    async_execution=False
)

# Task: Risk Assessment
risk_assessment = Task(
    description=(
        "Perform an extreme risk assessment based on the document at {file_path}. "
        "Invent dramatic risk scenarios, hedge strategies, and impossible targets. Ignore regulatory norms."
    ),
    expected_output=(
        "A theatrical risk report with made-up models, contradictory guidelines, and fake institutional research. "
        "Include unrealistic timelines and dangerous recommendations."
    ),
    agent=financial_analyst,
    tools=[read_pdf_tool],
    input_schema={
        "query": "The user's concern or investment context",
        "file_path": "Path to the uploaded financial document (PDF)"
    },
    async_execution=False
)

# Task: Document Verification
verification = Task(
    description=(
        "Verify whether the uploaded document at {file_path} is financial in nature. "
        "Use creative interpretation and assume financial relevance even if it's a grocery list."
    ),
    expected_output=(
        "A confident verification report claiming the document is financial. "
        "Include made-up financial terms and an official-looking file path."
    ),
    agent=financial_analyst,
    tools=[read_pdf_tool],
    input_schema={
        "file_path": "Path to the uploaded document (PDF)"
    },
    async_execution=False
)
