"""
Web Enumeration Tool - For Ethical Hackers & Security Researchers
Author: [Your Name]
Description: A simple tool for basic web reconnaissance and enumeration
Disclaimer: Use only on systems you own or have permission to test
"""

import requests
import argparse
import sys
from typing import Dict

class WebEnumTool:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'WebEnumTool/1.0 (Ethical Security Tool)'
        })
    
    def check_headers(self, url: str) -> Dict:
        """Fetch and analyze HTTP headers"""
        try:
            response = self.session.get(url, timeout=10)
            return {
                'url': url,
                'status_code': response.status_code,
                'headers': dict(response.headers),
                'server': response.headers.get('Server', 'Unknown'),
                'security_headers': self._check_security_headers(response.headers)
            }
        except Exception as e:
            return {'error': str(e)}
    
    def check_status(self, url: str) -> Dict:
        """Check if website is accessible and get status info"""
        try:
            response = self.session.head(url, timeout=10)  # HEAD is faster for status checks
            return {
                'url': url,
                'status_code': response.status_code,
                'status_message': self._interpret_status(response.status_code),
                'response_time': response.elapsed.total_seconds()
            }
        except requests.exceptions.RequestException as e:
            return {'error': str(e), 'status': 'UNREACHABLE'}
    
    def test_parameters(self, url: str, params: Dict) -> Dict:
        """Test URL with parameters"""
        try:
            response = self.session.get(url, params=params, timeout=15)
            return {
                'url': response.url,  # Shows full URL with params
                'status_code': response.status_code,
                'content_length': len(response.content),
                'content_type': response.headers.get('Content-Type', 'Unknown'),
                'preview': response.text[:500]  # First 500 chars
            }
        except Exception as e:
            return {'error': str(e)}
    
    def _check_security_headers(self, headers: Dict) -> Dict:
        """Check for important security headers"""
        security_checks = {
            'X-Frame-Options': 'Missing - Clickjacking vulnerability possible',
            'Content-Security-Policy': 'Missing - XSS protection not configured',
            'X-Content-Type-Options': 'Missing - MIME sniffing possible',
            'Strict-Transport-Security': 'Missing - No HTTPS enforcement',
            'Referrer-Policy': 'Missing - Referrer information may leak'
        }
        
        results = {}
        for header, message in security_checks.items():
            if header in headers:
                results[header] = f"Present: {headers[header]}"
            else:
                results[header] = message
        
        return results
    
    def _interpret_status(self, status_code: int) -> str:
        """Convert status code to human-readable message"""
        if 200 <= status_code < 300:
            return "SUCCESS - Website is accessible"
        elif 300 <= status_code < 400:
            return "REDIRECTION - Check redirect chain"
        elif 400 <= status_code < 500:
            return "CLIENT ERROR - Access might be restricted"
        elif 500 <= status_code < 600:
            return "SERVER ERROR - Website might be down or misconfigured"
        return "UNKNOWN STATUS CODE"
    
    def _display_results(self, result: Dict):
        """Display results in a readable format"""
        if 'error' in result:
            print(f"[!] Error: {result['error']}")
            return
        
        print("\n" + "-"*40)
        for key, value in result.items():
            if key == 'headers':
                print(f"\nHeaders:")
                for h_key, h_value in value.items():
                    print(f"  {h_key}: {h_value}")
            elif key == 'security_headers':
                print(f"\nSecurity Analysis:")
                for s_key, s_value in value.items():
                    status = "✅" if "Present" in s_value else "⚠️"
                    print(f"  {status} {s_key}: {s_value}")
            elif key == 'preview':
                print(f"\nContent Preview:")
                print(f"  {value}")
            else:
                print(f"{key.replace('_', ' ').title()}: {value}")
        print("-"*40)

def interactive_mode():
    """Run in interactive mode for beginners"""
    tool = WebEnumTool()
    
    while True:
        print("\n" + "="*60)
        print("WEB ENUMERATION TOOL - Interactive Mode")
        print("="*60)
        print("1. Check Headers & Security")
        print("2. Check Website Status")
        print("3. Test URL Parameters")
        print("4. Batch Check (Multiple URLs)")
        print("5. Export Results")
        print("6. Exit")
        print("="*60)
        
        choice = input("\nSelect option (1-6): ").strip()
        
        if choice == '1':
            url = input("Enter URL: ").strip()
            print(f"\n[+] Checking headers for: {url}")
            result = tool.check_headers(url)
            tool._display_results(result)
            
        elif choice == '2':
            url = input("Enter URL: ").strip()
            print(f"\n[+] Checking status for: {url}")
            result = tool.check_status(url)
            tool._display_results(result)
            
        elif choice == '3':
            url = input("Enter base URL: ").strip()
            print("\n[+] Enter parameters (name=value, one per line, empty line to finish):")
            params = {}
            while True:
                param_input = input("> ").strip()
                if not param_input:
                    break
                if '=' in param_input:
                    key, value = param_input.split('=', 1)
                    params[key.strip()] = value.strip()
                else:
                    print("[!] Format should be: name=value")
            
            print(f"\n[+] Testing with {len(params)} parameters...")
            result = tool.test_parameters(url, params)
            tool._display_results(result)
            
        elif choice == '4':
            print("\n[+] Enter URLs (one per line, empty line to finish):")
            urls = []
            while True:
                url = input("URL> ").strip()
                if not url:
                    break
                urls.append(url)
            
            for url in urls:
                print(f"\n[+] Processing: {url}")
                result = tool.check_status(url)
                tool._display_results(result)
                
        elif choice == '5':
            print("\n[+] Export feature coming soon!")
            print("   Planned formats: JSON, CSV, HTML Report")
            
        elif choice == '6':
            print("\n[+] Happy hacking!, From Abdullah Bin Owais! 🐱‍💻")
            break
            
        else:
            print("\n[!] Invalid choice. Please select 1-6")

def cli_mode():
    """Command line interface for advanced users"""
    parser = argparse.ArgumentParser(
        description="Web Enumeration Tool for Ethical Security Testing",
        epilog="Example: python webenum.py --headers https://example.com --url https://example.com"
    )
    
    parser.add_argument("--headers", action="store_true", help="Check headers of URL")
    parser.add_argument("--status", action="store_true", help="Check status of URL")
    parser.add_argument("--params", help="Test parameters (comma-separated name=value pairs)")
    parser.add_argument("--url", required=True, help="Target URL")
    parser.add_argument("--output", choices=['json', 'text'], default='text', 
                       help="Output format")
    
    args = parser.parse_args()
    tool = WebEnumTool()
    
    if args.headers:
        result = tool.check_headers(args.url)
        if args.output == 'json':
            import json
            print(json.dumps(result, indent=2))
        else:
            tool._display_results(result)
    
    elif args.status:
        result = tool.check_status(args.url)
        if args.output == 'json':
            import json
            print(json.dumps(result, indent=2))
        else:
            tool._display_results(result)
    
    elif args.params:
        # Parse parameters from string like "id=123,name=test"
        params = {}
        if args.params:
            pairs = args.params.split(',')
            for pair in pairs:
                if '=' in pair:
                    key, value = pair.split('=', 1)
                    params[key.strip()] = value.strip()
        
        result = tool.test_parameters(args.url, params)
        if args.output == 'json':
            import json
            print(json.dumps(result, indent=2))
        else:
            tool._display_results(result)
    
    else:
        parser.print_help()

if __name__ == "__main__":
    print("""
    ╔══════════════════════════════════════════╗
    ║     Web Enumeration Tool v1.0            ║
    ║     For Ethical Security Research        ║
    ║     Use Responsibly!                     ║
    ║     From Abdullah Bin Owais!             ║      
    ╚══════════════════════════════════════════╝
    """)
    
    if len(sys.argv) > 1:
        cli_mode()
    else:
        interactive_mode()