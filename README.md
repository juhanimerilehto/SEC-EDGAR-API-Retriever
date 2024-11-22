# SEC Report Retriever

**Version 1.0**
### Creator: Juhani Merilehto - @juhanimerilehto - Jyväskylä University of Applied Sciences (JAMK), Likes institute

![JAMK Likes Logo](./assets/likes_str_logo.png)

## Overview

SEC Report Retriever is a Python tool for automatically retrieving and downloading SEC filings, particularly 10-K reports. It provides a simple interface for accessing SEC's EDGAR database while respecting rate limits and handling document downloads efficiently.

The **SEC Report Retriever** can be valuable for exercise research by i.e., tracking companies' investments in sports/fitness technology, wearables, and health monitoring systems through their R&D expenses and acquisitions. The depending on the level of reporting in the 10K filings, this tool enables analysis of corporate wellness programs, sports facility investments, and market insights about consumer exercise habits – providing strategic data about industry trends and corporate commitments to physical activity initiatives.

## Features

- **SEC EDGAR Integration**: Direct access to SEC's EDGAR database
- **Rate Limiting**: Built-in rate limiting to comply with SEC guidelines
- **Selective Downloads**: Focus on 10-K filings with option to expand
- **Error Handling**: Robust error handling for network requests
- **File Management**: Organized storage of downloaded reports

## Requirements

- Python 3.6+
- Internet connection
- Required Python packages:
  - requests
  - time
  - json
  - os

## Installation

### 1. Clone the repository:
```bash
git clone https://github.com/juhanimerilehto/sec-report-retriever.git
cd sec-report-retriever
```

### 2. Create a virtual environment:
```bash
python -m venv sec-env
source sec-env/bin/activate  # For Windows: sec-env\Scripts\activate
```

### 3. Install dependencies:
```bash
pip install requests
```

## Usage

Initialize the retriever with your company information:
```python
retriever = SECReportRetriever(
    company_name="Your Company",
    email="your.email@company.com"
)
```

Retrieve 10-K filings for a company:
```python
filings = retriever.get_10k_filings("936468")  # Example using Lockheed Martin's CIK
```

Download specific 10-K reports:
```python
filepath = retriever.download_10k(
    cik="936468",
    accession_number="filing_number",
    primary_doc="document_name.htm"
)
```

## File Structure

```plaintext
sec-report-retriever/
├── assets/
│   └── likes_str_logo.png
├── sec_retriever.py
├── requirements.txt
└── README.md
```

## Credits

- **Juhani Merilehto (@juhanimerilehto)** – Specialist, Data and Statistics
- **JAMK Likes** – Organization sponsor

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.