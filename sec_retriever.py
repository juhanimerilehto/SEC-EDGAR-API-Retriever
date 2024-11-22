import requests
import time
import json
import os

class SECReportRetriever:
    def __init__(self, company_name, email):
        self.base_url = "https://www.sec.gov/Archives"
        self.headers = {
            'User-Agent': f'{company_name} {email}',
            'Accept': 'application/json'
        }
        self.requests_per_second = 10
        self.last_request_time = 0

    def _respect_rate_limit(self):
        current_time = time.time()
        time_since_last_request = current_time - self.last_request_time
        if time_since_last_request < (1 / self.requests_per_second):
            time.sleep((1 / self.requests_per_second) - time_since_last_request)
        self.last_request_time = time.time()

    def get_company_filings(self, cik):
        """Get company filings using the company CIK"""
        try:
            cik_padded = str(cik).zfill(10)
            url = f"https://data.sec.gov/submissions/CIK{cik_padded}.json"
            
            self._respect_rate_limit()
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            
            data = response.json()
            return data['filings']['recent']

        except requests.exceptions.RequestException as e:
            print(f"Error retrieving filings for CIK {cik}: {e}")
            return None

    def get_10k_filings(self, cik):
        """Get only 10-K filings metadata"""
        filings_data = self.get_company_filings(cik)
        
        if not filings_data:
            return []
        
        forms = filings_data.get('form', [])
        dates = filings_data.get('filingDate', [])
        accession_numbers = filings_data.get('accessionNumber', [])
        primary_docs = filings_data.get('primaryDocument', [])
        
        ten_k_filings = []
        for i in range(len(forms)):
            if forms[i] == '10-K':
                ten_k_filings.append({
                    'accessionNumber': accession_numbers[i],
                    'filingDate': dates[i],
                    'form': forms[i],
                    'primaryDocument': primary_docs[i] if i < len(primary_docs) else None
                })
        
        return ten_k_filings

    def download_10k(self, cik, accession_number, primary_doc, output_dir="downloaded_10k"):
        """Download the 10-K document"""
        try:
            # Format CIK and accession number
            cik = str(cik).zfill(10)
            accession_formatted = accession_number.replace('-', '')
            
            # Construct the correct URL using Edgar's archive structure
            url = f"{self.base_url}/edgar/data/{cik}/{accession_formatted}/{primary_doc}"
            
            print(f"Attempting to download from: {url}")
            
            # Create output directory if it doesn't exist
            os.makedirs(output_dir, exist_ok=True)
            
            # Create filename
            filename = f"{cik}_{accession_formatted}.html"
            filepath = os.path.join(output_dir, filename)
            
            # Download the file
            self._respect_rate_limit()
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            
            # Save the file
            with open(filepath, 'wb') as f:
                f.write(response.content)
                
            print(f"Successfully downloaded: {filepath}")
            return filepath
            
        except Exception as e:
            print(f"Error downloading document {accession_number}: {e}")
            return None

def main():
    retriever = SECReportRetriever(
        company_name="Example Company", # Add the company name you wish to use
        email="example@email.com" # Add the email you wish to use
    )
    
    # Lockheed Martin's CIK - add as you see necessary
    lockheed_cik = "936468"
    
    # Get 10-K filings
    filings = retriever.get_10k_filings(lockheed_cik)
    
    if filings:
        print("\nRecent 10-K filings for Lockheed Martin:")
        for filing in filings:
            print(f"Filing Date: {filing['filingDate']}")
            print(f"Accession Number: {filing['accessionNumber']}")
            print(f"Form Type: {filing['form']}")
            print(f"Primary Document: {filing.get('primaryDocument', 'N/A')}")
            print("-" * 50)
            
            # Download the most recent 10-K (first in the list)
            if filing == filings[0] and filing.get('primaryDocument'):
                print("\nDownloading most recent 10-K...")
                filepath = retriever.download_10k(
                    lockheed_cik, 
                    filing['accessionNumber'],
                    filing['primaryDocument']
                )
                if filepath:
                    print(f"Downloaded to: {filepath}")
                    
                    # Preview the first few lines of the file
                    try:
                        with open(filepath, 'r', encoding='utf-8') as f:
                            print("\nFile preview:")
                            print(f.read(500) + "...")
                    except Exception as e:
                        print(f"Error reading file: {e}")
    else:
        print("No 10-K filings found or error occurred")

if __name__ == "__main__":
    main()