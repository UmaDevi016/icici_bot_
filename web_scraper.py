import requests
from bs4 import BeautifulSoup
from typing import List, Dict
import time
from urllib.parse import urljoin, urlparse
import re

class ICICIWebScraper:
    def __init__(self, base_url: str = "https://www.iciciprulife.com", max_pages: int = 20):
        self.base_url = base_url
        self.max_pages = max_pages
        self.visited_urls = set()
        self.scraped_content = []
        
    def is_valid_url(self, url: str) -> bool:
        """Check if URL is valid and belongs to ICICI domain"""
        parsed = urlparse(url)
        return bool(parsed.netloc) and 'iciciprulife.com' in parsed.netloc.lower()
    
    def clean_text(self, text: str) -> str:
        """Clean and normalize text"""
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        # Remove special characters but keep important punctuation
        text = re.sub(r'[^\w\s.,!?;:()\-]', '', text)
        return text.strip()
    
    def extract_text_from_page(self, url: str) -> Dict:
        """Extract text content from a webpage"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove script and style elements
            for script in soup(['script', 'style', 'nav', 'footer', 'header']):
                script.decompose()
            
            # Get title
            title = soup.find('title')
            title_text = title.get_text() if title else ""
            
            # Get main content
            # Try to find main content areas
            main_content = soup.find('main') or soup.find('article') or soup.find('div', class_=re.compile('content|main'))
            
            if main_content:
                text = main_content.get_text(separator=' ', strip=True)
            else:
                text = soup.get_text(separator=' ', strip=True)
            
            # Clean the text
            cleaned_text = self.clean_text(text)
            
            # Get meta description
            meta_desc = soup.find('meta', attrs={'name': 'description'})
            description = meta_desc.get('content', '') if meta_desc else ""
            
            return {
                'url': url,
                'title': self.clean_text(title_text),
                'description': self.clean_text(description),
                'content': cleaned_text
            }
            
        except Exception as e:
            print(f"Error scraping {url}: {e}")
            return None
    
    def get_links_from_page(self, url: str, soup: BeautifulSoup) -> List[str]:
        """Extract all links from a page"""
        links = []
        for link in soup.find_all('a', href=True):
            href = link['href']
            full_url = urljoin(url, href)
            
            if self.is_valid_url(full_url) and full_url not in self.visited_urls:
                links.append(full_url)
        
        return links
    
    def scrape_important_pages(self) -> List[Dict]:
        """Scrape important pages from ICICI Insurance website"""
        # Important pages to scrape
        important_urls = [
            "https://www.iciciprulife.com/",
            "https://www.iciciprulife.com/insurance-plans.html",
            "https://www.iciciprulife.com/term-insurance.html",
            "https://www.iciciprulife.com/savings-plan.html",
            "https://www.iciciprulife.com/pension-plans.html",
            "https://www.iciciprulife.com/ulip-plans.html",
            "https://www.iciciprulife.com/claims/death-claim.html",
            "https://www.iciciprulife.com/claims/maturity-claim.html",
            "https://www.iciciprulife.com/about-us.html",
            "https://www.iciciprulife.com/contact-us.html",
        ]
        
        print(f"Starting web scraping from ICICI Insurance website...")
        
        for url in important_urls:
            if len(self.scraped_content) >= self.max_pages:
                break
            
            if url in self.visited_urls:
                continue
            
            print(f"Scraping: {url}")
            self.visited_urls.add(url)
            
            page_data = self.extract_text_from_page(url)
            if page_data and len(page_data['content']) > 100:
                self.scraped_content.append(page_data)
            
            # Be polite - wait between requests
            time.sleep(1)
        
        print(f"Scraped {len(self.scraped_content)} pages successfully")
        return self.scraped_content
    
    def create_chunks_from_web_content(self, chunk_size: int = 500, overlap: int = 50) -> List[str]:
        """Convert scraped web content into chunks"""
        all_chunks = []
        
        for page in self.scraped_content:
            # Create a context prefix for each page
            prefix = f"From {page['title']}: "
            
            # Combine description and content
            full_text = f"{page['description']} {page['content']}"
            
            # Split into words
            words = full_text.split()
            
            # Create chunks
            for i in range(0, len(words), chunk_size - overlap):
                chunk_words = words[i:i + chunk_size]
                chunk = ' '.join(chunk_words)
                
                if len(chunk.strip()) > 100:  # Only add substantial chunks
                    all_chunks.append(prefix + chunk.strip())
        
        print(f"Created {len(all_chunks)} chunks from web content")
        return all_chunks
    
    def save_content_to_file(self, output_path: str = "web_content.txt"):
        """Save scraped content to a text file"""
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                for page in self.scraped_content:
                    f.write(f"=== {page['title']} ===\n")
                    f.write(f"URL: {page['url']}\n")
                    f.write(f"Description: {page['description']}\n\n")
                    f.write(f"{page['content']}\n\n")
                    f.write("=" * 80 + "\n\n")
            print(f"Web content saved to {output_path}")
        except Exception as e:
            print(f"Error saving web content: {e}")

if __name__ == "__main__":
    # Test the scraper
    scraper = ICICIWebScraper()
    content = scraper.scrape_important_pages()
    scraper.save_content_to_file()
    
    chunks = scraper.create_chunks_from_web_content()
    print(f"Total chunks created: {len(chunks)}")
