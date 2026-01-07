import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from collections import deque
import time

class SEOCrawler:
    def __init__(self, base_url, max_pages=10, max_depth=2):
        self.base_url = base_url
        self.max_pages = max_pages
        self.max_depth = max_depth
        self.visited = set()
        self.pages_data = []
        self.broken_links = []
        self.all_links = set()
        
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        
        # Get base domain for internal link filtering
        parsed = urlparse(base_url)
        self.base_domain = f"{parsed.scheme}://{parsed.netloc}"
    
    def is_valid_url(self, url):
        """Check if URL is valid and belongs to same domain"""
        try:
            parsed = urlparse(url)
            # Check if it's the same domain
            return parsed.netloc == urlparse(self.base_url).netloc
        except:
            return False
    
    def normalize_url(self, url):
        """Normalize URL by removing fragments and trailing slashes"""
        parsed = urlparse(url)
        # Remove query parameters and fragments for normalization
        path = parsed.path
        # Always remove trailing slash except for root path
        if path.endswith('/') and path != '/':
            path = path[:-1]
        # If path is empty, make it root
        if not path:
            path = '/'
        normalized = f"{parsed.scheme}://{parsed.netloc}{path}"
        return normalized
    
    def check_link_status(self, url):
        """Check if a link is truly broken (not just bot-protected)"""
        try:
            # Try HEAD request first (faster)
            response = requests.head(url, headers=self.headers, timeout=5, allow_redirects=True)
            status = response.status_code
            
            # If HEAD fails with 405 (Method Not Allowed), try GET
            if status == 405:
                response = requests.get(url, headers=self.headers, timeout=5, allow_redirects=True)
                status = response.status_code
            
            return status
            
        except requests.exceptions.Timeout:
            return 0  # Timeout
        except requests.exceptions.ConnectionError:
            return 0  # Connection failed
        except:
            # Try GET as fallback
            try:
                response = requests.get(url, headers=self.headers, timeout=5, allow_redirects=True)
                return response.status_code
            except:
                return 0  # Connection failed
    
    def is_truly_broken(self, status_code, url=""):
        """Determine if a status code indicates a truly broken link"""
        
        # Special anti-bot status codes (NOT broken)
        if status_code == 999:  # LinkedIn anti-scraping
            return False
        if status_code == 429:  # Rate limiting (link exists, just throttled)
            return False
        
        # Known platforms with aggressive bot protection
        bot_protected_domains = [
            'linkedin.com',
            'facebook.com', 
            'twitter.com',
            'instagram.com',
            'github.com',  # GitHub often blocks automated requests
            'leetcode.com',
            'hackerrank.com'
        ]
        
        # If it's a known bot-protected domain, be lenient
        if url and any(domain in url.lower() for domain in bot_protected_domains):
            # Only flag as broken if it's a clear 404 or 500+ AND we're sure
            if status_code == 404:
                # GitHub 404s might be real, but could also be bot protection
                # Let's be conservative and not flag them
                if 'github.com' in url.lower():
                    return False
            # Don't flag other status codes for protected domains
            if status_code < 500:
                return False
        
        # Truly broken links
        if status_code == 0:  # Connection failed
            return True
        if status_code == 404:  # Not found (for non-protected domains)
            return True
        if status_code >= 500:  # Server errors
            return True
        
        # NOT broken - these are anti-bot or access control
        # 400 - Bad Request (often bot protection)
        # 401 - Unauthorized (requires login, but link exists)
        # 403 - Forbidden (bot protection, but link exists)
        # 405 - Method Not Allowed (HEAD blocked, but link exists)
        
        return False
    
    def extract_page_data(self, url, html_content):
        """Extract comprehensive SEO data from a page"""
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Extract all headings with hierarchy
        headings = {
            'h1': [h.get_text().strip() for h in soup.find_all('h1')],
            'h2': [h.get_text().strip() for h in soup.find_all('h2')],
            'h3': [h.get_text().strip() for h in soup.find_all('h3')],
            'h4': [h.get_text().strip() for h in soup.find_all('h4')],
            'h5': [h.get_text().strip() for h in soup.find_all('h5')],
            'h6': [h.get_text().strip() for h in soup.find_all('h6')]
        }
        
        # Extract title
        title = soup.title.string.strip() if soup.title and soup.title.string else ""
        
        # Extract meta description
        meta_desc = ""
        meta_tag = soup.find("meta", attrs={'name': 'description'})
        if meta_tag:
            meta_desc = meta_tag.get("content", "").strip()
        
        # Extract meta keywords
        meta_keywords = ""
        meta_kw = soup.find("meta", attrs={'name': 'keywords'})
        if meta_kw:
            meta_keywords = meta_kw.get("content", "").strip()
        
        # Extract Open Graph tags
        og_tags = {}
        for og in soup.find_all("meta", property=lambda x: x and x.startswith('og:')):
            og_tags[og.get('property')] = og.get('content', '')
        
        # Extract Twitter Card tags
        twitter_tags = {}
        for tw in soup.find_all("meta", attrs={'name': lambda x: x and x.startswith('twitter:')}):
            twitter_tags[tw.get('name')] = tw.get('content', '')
        
        # Extract canonical URL
        canonical = ""
        canonical_tag = soup.find("link", rel="canonical")
        if canonical_tag:
            canonical = canonical_tag.get("href", "")
        
        # Extract all links
        links = []
        for a in soup.find_all('a', href=True):
            href = a.get('href')
            full_url = urljoin(url, href)
            links.append({
                'url': full_url,
                'text': a.get_text().strip(),
                'is_internal': self.is_valid_url(full_url)
            })
            self.all_links.add(full_url)
        
        # Extract images with alt text analysis
        images = []
        for img in soup.find_all('img'):
            images.append({
                'src': img.get('src', ''),
                'alt': img.get('alt', ''),
                'has_alt': bool(img.get('alt')),
                'title': img.get('title', '')
            })
        
        # Extract visible text
        # Remove script and style elements
        for script in soup(["script", "style", "noscript"]):
            script.decompose()
        
        full_text = soup.get_text()
        # Clean up whitespace
        lines = (line.strip() for line in full_text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        full_text = ' '.join(chunk for chunk in chunks if chunk)
        
        # Check for robots meta tag
        robots_meta = ""
        robots_tag = soup.find("meta", attrs={'name': 'robots'})
        if robots_tag:
            robots_meta = robots_tag.get("content", "")
        
        return {
            'url': url,
            'title': title,
            'title_length': len(title),
            'meta_description': meta_desc,
            'meta_description_length': len(meta_desc),
            'meta_keywords': meta_keywords,
            'canonical': canonical,
            'og_tags': og_tags,
            'twitter_tags': twitter_tags,
            'robots_meta': robots_meta,
            'headings': headings,
            'links': links,
            'internal_links_count': sum(1 for l in links if l['is_internal']),
            'external_links_count': sum(1 for l in links if not l['is_internal']),
            'images': images,
            'images_without_alt': sum(1 for img in images if not img['has_alt']),
            'total_images': len(images),
            'full_text': full_text,
            'word_count': len(full_text.split())
        }
    
    def crawl(self):
        """Crawl website with BFS approach"""
        queue = deque([(self.base_url, 0)])  # (url, depth)
        self.visited.add(self.normalize_url(self.base_url))
        
        while queue and len(self.pages_data) < self.max_pages:
            current_url, depth = queue.popleft()
            
            if depth > self.max_depth:
                continue
            
            # Normalize current URL to check for duplicates
            normalized_current = self.normalize_url(current_url)
            
            # Skip if we've already crawled this normalized URL
            if normalized_current in [self.normalize_url(p.get('url', '')) for p in self.pages_data if 'url' in p]:
                print(f"Skipping duplicate: {current_url} (already crawled as {normalized_current})")
                continue
            
            try:
                print(f"Crawling: {current_url} (depth: {depth})")
                response = requests.get(current_url, headers=self.headers, timeout=10)
                
                # Extract page data
                page_data = self.extract_page_data(current_url, response.text)
                page_data['status_code'] = response.status_code
                page_data['depth'] = depth
                self.pages_data.append(page_data)
                
                # Add internal links to queue if not at max depth
                if depth < self.max_depth:
                    for link in page_data['links']:
                        if link['is_internal']:
                            normalized = self.normalize_url(link['url'])
                            if normalized not in self.visited and len(self.visited) < self.max_pages:
                                self.visited.add(normalized)
                                queue.append((link['url'], depth + 1))
                
                # Small delay to be polite
                time.sleep(0.5)
                
            except Exception as e:
                print(f"Error crawling {current_url}: {str(e)}")
                self.pages_data.append({
                    'url': current_url,
                    'error': str(e),
                    'status_code': 0,
                    'depth': depth
                })
        
        # Check for broken links
        self.check_broken_links()
        
        return {
            'pages': self.pages_data,
            'broken_links': self.broken_links,
            'total_pages_crawled': len(self.pages_data),
            'total_links_found': len(self.all_links)
        }
    
    def check_broken_links(self):
        """Check all discovered links for broken ones"""
        print("Checking for broken links...")
        checked = set()
        
        # Special URI schemes that should not be checked
        skip_schemes = ['mailto:', 'tel:', 'javascript:', 'data:', 'ftp:', 'file:', '#']
        
        for page in self.pages_data:
            if 'links' in page:
                for link in page['links'][:20]:  # Limit to first 20 links per page
                    url = link['url']
                    
                    # Skip special URI schemes
                    if any(url.lower().startswith(scheme) for scheme in skip_schemes):
                        continue
                    
                    # Skip anchor links
                    if url.startswith('#'):
                        continue
                    
                    # Only check HTTP/HTTPS links
                    if not url.startswith(('http://', 'https://')):
                        continue
                    
                    if url not in checked:
                        checked.add(url)
                        status = self.check_link_status(url)
                        
                        # Only report truly broken links (not bot protection)
                        if self.is_truly_broken(status, url):
                            self.broken_links.append({
                                'url': url,
                                'status_code': status,
                                'found_on': page['url'],
                                'link_text': link['text']
                            })



