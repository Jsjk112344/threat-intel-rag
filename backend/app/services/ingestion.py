import requests
import time
from typing import List, Dict
from datetime import datetime, timedelta
import os

class NVDIngestionService:
    def __init__(self):
        self.base_url = "https://services.nvd.nist.gov/rest/json/cves/2.0"
        self.api_key = os.getenv('NVD_API_KEY')
        
    def fetch_recent_cves(self, days_back: int = 30, max_results: int = 100) -> List[Dict]:
        """Fetch recent CVEs from NVD API"""
        
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days_back)
        
        params = {
            'pubStartDate': start_date.strftime('%Y-%m-%dT00:00:00.000'),
            'pubEndDate': end_date.strftime('%Y-%m-%dT23:59:59.999'),
            'resultsPerPage': min(max_results, 2000)  # NVD max is 2000
        }
        
        headers = {}
        if self.api_key:
            headers['apiKey'] = self.api_key
        
        try:
            response = requests.get(self.base_url, params=params, headers=headers)
            response.raise_for_status()
            
            data = response.json()
            vulnerabilities = data.get('vulnerabilities', [])
            
            processed_cves = []
            for vuln in vulnerabilities:
                cve_item = vuln.get('cve', {})
                processed_cves.append(self._process_cve(cve_item))
            
            print(f"Fetched {len(processed_cves)} CVEs")
            return processed_cves
            
        except requests.exceptions.RequestException as e:
            print(f"Error fetching CVEs: {e}")
            return []
    
    def _process_cve(self, cve_data: Dict) -> Dict:
        """Extract relevant fields from CVE data"""
        
        cve_id = cve_data.get('id', 'N/A')
        
        # Get description
        descriptions = cve_data.get('descriptions', [])
        description = next(
            (d['value'] for d in descriptions if d.get('lang') == 'en'),
            'No description available'
        )
        
        # Get CVSS score
        metrics = cve_data.get('metrics', {})
        cvss_data = metrics.get('cvssMetricV31', [{}])[0] if metrics.get('cvssMetricV31') else {}
        
        if not cvss_data:
            cvss_data = metrics.get('cvssMetricV2', [{}])[0] if metrics.get('cvssMetricV2') else {}
        
        cvss_score = cvss_data.get('cvssData', {}).get('baseScore', 0.0)
        severity = cvss_data.get('cvssData', {}).get('baseSeverity', 'UNKNOWN')
        
        # Get published date
        published = cve_data.get('published', '')
        
        # Get references
        references = cve_data.get('references', [])
        ref_urls = [ref.get('url') for ref in references[:3]]  # Limit to 3
        
        return {
            'cve_id': cve_id,
            'description': description,
            'cvss_score': cvss_score,
            'severity': severity,
            'published_date': published,
            'references': ref_urls,
            'content': f"{cve_id}: {description}"  # For embedding
        }