from textblob import TextBlob
import textstat
import re
from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer
import math

class SEOAnalyzer:
    def __init__(self):
        # SEO best practices thresholds
        self.IDEAL_TITLE_MIN = 50
        self.IDEAL_TITLE_MAX = 60
        self.IDEAL_META_MIN = 150
        self.IDEAL_META_MAX = 160
        self.MIN_WORD_COUNT = 300
        self.IDEAL_WORD_COUNT = 1000
        
    def analyze_page(self, page_data):
        """Analyze a single page for SEO metrics"""
        if 'error' in page_data:
            return {'error': page_data['error']}
        
        analysis = {
            'url': page_data['url'],
            'technical_seo': self.analyze_technical_seo(page_data),
            'content_seo': self.analyze_content_seo(page_data),
            'accessibility': self.analyze_accessibility(page_data),
            'issues': [],
            'warnings': [],
            'recommendations': [],
            'positive_highlights': []  # What's working well!
        }
        
        # Generate issues and recommendations
        self.generate_issues(page_data, analysis)
        
        # Generate positive highlights
        self.generate_positive_highlights(page_data, analysis)
        
        return analysis
    
    def analyze_technical_seo(self, page_data):
        """Analyze technical SEO aspects"""
        score = 0
        max_score = 100
        details = {}
        
        # Title tag analysis (20 points)
        title = page_data.get('title', '')
        title_length = page_data.get('title_length', 0)
        
        if title:
            if self.IDEAL_TITLE_MIN <= title_length <= self.IDEAL_TITLE_MAX:
                score += 20
                details['title_status'] = 'optimal'
            elif title_length > 0:
                score += 10
                details['title_status'] = 'needs_optimization'
            else:
                details['title_status'] = 'missing'
        else:
            details['title_status'] = 'missing'
        
        details['title_length'] = title_length
        
        # Meta description analysis (20 points)
        meta_desc = page_data.get('meta_description', '')
        meta_length = page_data.get('meta_description_length', 0)
        
        if meta_desc:
            if self.IDEAL_META_MIN <= meta_length <= self.IDEAL_META_MAX:
                score += 20
                details['meta_status'] = 'optimal'
            elif meta_length > 0:
                score += 10
                details['meta_status'] = 'needs_optimization'
            else:
                details['meta_status'] = 'missing'
        else:
            details['meta_status'] = 'missing'
        
        details['meta_length'] = meta_length
        
        # H1 tag analysis (15 points)
        h1_tags = page_data.get('headings', {}).get('h1', [])
        h1_count = len(h1_tags)
        
        if h1_count == 1:
            score += 15
            details['h1_status'] = 'optimal'
        elif h1_count == 0:
            details['h1_status'] = 'missing'
        else:
            score += 5
            details['h1_status'] = 'multiple'
        
        details['h1_count'] = h1_count
        
        # Heading hierarchy (10 points)
        hierarchy_valid = self.check_heading_hierarchy(page_data.get('headings', {}))
        if hierarchy_valid:
            score += 10
            details['heading_hierarchy'] = 'valid'
        else:
            details['heading_hierarchy'] = 'invalid'
        
        # Canonical URL (10 points)
        if page_data.get('canonical'):
            score += 10
            details['has_canonical'] = True
        else:
            details['has_canonical'] = False
        
        # Open Graph tags (10 points)
        og_tags = page_data.get('og_tags', {})
        if len(og_tags) >= 4:  # At least 4 OG tags
            score += 10
            details['og_tags_status'] = 'good'
        elif len(og_tags) > 0:
            score += 5
            details['og_tags_status'] = 'partial'
        else:
            details['og_tags_status'] = 'missing'
        
        details['og_tags_count'] = len(og_tags)
        
        # Status code (15 points)
        status_code = page_data.get('status_code', 0)
        if status_code == 200:
            score += 15
            details['status'] = 'ok'
        elif 300 <= status_code < 400:
            score += 10
            details['status'] = 'redirect'
        else:
            details['status'] = 'error'
        
        details['status_code'] = status_code
        
        return {
            'score': score,
            'max_score': max_score,
            'percentage': round((score / max_score) * 100, 1),
            'details': details
        }
    
    def analyze_content_seo(self, page_data):
        """Analyze content quality and SEO"""
        score = 0
        max_score = 100
        details = {}
        
        text = page_data.get('full_text', '')
        word_count = page_data.get('word_count', 0)
        
        # Word count analysis (25 points)
        if word_count >= self.IDEAL_WORD_COUNT:
            score += 25
            details['word_count_status'] = 'excellent'
        elif word_count >= self.MIN_WORD_COUNT:
            score += 15
            details['word_count_status'] = 'good'
        elif word_count > 0:
            score += 5
            details['word_count_status'] = 'low'
        else:
            details['word_count_status'] = 'none'
        
        details['word_count'] = word_count
        
        # Readability analysis (25 points)
        if text and word_count > 50:
            try:
                flesch_score = textstat.flesch_reading_ease(text)
                details['flesch_reading_ease'] = round(flesch_score, 1)
                
                # Score based on readability
                if 60 <= flesch_score <= 80:  # Ideal range
                    score += 25
                    details['readability_status'] = 'optimal'
                elif 50 <= flesch_score <= 90:
                    score += 15
                    details['readability_status'] = 'good'
                else:
                    score += 5
                    details['readability_status'] = 'needs_improvement'
                
                # Additional readability metrics
                details['flesch_kincaid_grade'] = round(textstat.flesch_kincaid_grade(text), 1)
                details['reading_level'] = self.get_reading_level(flesch_score)
                
            except:
                details['readability_status'] = 'error'
        else:
            details['readability_status'] = 'insufficient_text'
        
        # Sentiment analysis (15 points)
        if text:
            blob = TextBlob(text)
            sentiment = blob.sentiment.polarity
            
            details['sentiment_polarity'] = round(sentiment, 2)
            
            if sentiment > 0.1:
                details['tone'] = 'Positive'
                score += 15
            elif sentiment < -0.1:
                details['tone'] = 'Negative'
                score += 5
            else:
                details['tone'] = 'Neutral'
                score += 10
        
        # Keyword analysis (20 points)
        keywords_analysis = self.extract_keywords_tfidf(text)
        details['top_keywords'] = keywords_analysis['top_keywords']
        details['keyword_density'] = keywords_analysis['keyword_density']
        
        if len(keywords_analysis['top_keywords']) >= 5:
            score += 20
            details['keyword_status'] = 'good'
        elif len(keywords_analysis['top_keywords']) > 0:
            score += 10
            details['keyword_status'] = 'limited'
        else:
            details['keyword_status'] = 'none'
        
        # Content structure (15 points)
        headings = page_data.get('headings', {})
        total_headings = sum(len(h) for h in headings.values())
        
        if total_headings >= 5:
            score += 15
            details['content_structure'] = 'well_structured'
        elif total_headings > 0:
            score += 8
            details['content_structure'] = 'basic'
        else:
            details['content_structure'] = 'poor'
        
        details['total_headings'] = total_headings
        
        return {
            'score': score,
            'max_score': max_score,
            'percentage': round((score / max_score) * 100, 1),
            'details': details
        }
    
    def analyze_accessibility(self, page_data):
        """Analyze accessibility features"""
        score = 0
        max_score = 100
        details = {}
        
        # Image alt text (40 points)
        total_images = page_data.get('total_images', 0)
        images_without_alt = page_data.get('images_without_alt', 0)
        
        if total_images > 0:
            alt_percentage = ((total_images - images_without_alt) / total_images) * 100
            details['images_with_alt_percentage'] = round(alt_percentage, 1)
            
            if alt_percentage == 100:
                score += 40
                details['alt_text_status'] = 'excellent'
            elif alt_percentage >= 80:
                score += 30
                details['alt_text_status'] = 'good'
            elif alt_percentage >= 50:
                score += 15
                details['alt_text_status'] = 'needs_improvement'
            else:
                score += 5
                details['alt_text_status'] = 'poor'
        else:
            score += 40  # No images means no issue
            details['alt_text_status'] = 'no_images'
        
        details['total_images'] = total_images
        details['images_without_alt'] = images_without_alt
        
        # Heading structure for screen readers (30 points)
        headings = page_data.get('headings', {})
        if headings.get('h1') and len(headings.get('h1')) == 1:
            score += 30
            details['heading_accessibility'] = 'good'
        else:
            score += 10
            details['heading_accessibility'] = 'needs_improvement'
        
        # Link text quality (30 points)
        links = page_data.get('links', [])
        empty_link_text = sum(1 for link in links if not link.get('text', '').strip())
        
        if links:
            link_quality = ((len(links) - empty_link_text) / len(links)) * 100
            details['links_with_text_percentage'] = round(link_quality, 1)
            
            if link_quality == 100:
                score += 30
                details['link_text_status'] = 'excellent'
            elif link_quality >= 90:
                score += 20
                details['link_text_status'] = 'good'
            else:
                score += 10
                details['link_text_status'] = 'needs_improvement'
        else:
            score += 30
            details['link_text_status'] = 'no_links'
        
        details['total_links'] = len(links)
        details['links_without_text'] = empty_link_text
        
        return {
            'score': score,
            'max_score': max_score,
            'percentage': round((score / max_score) * 100, 1),
            'details': details
        }
    
    def check_heading_hierarchy(self, headings):
        """Check if heading hierarchy is valid (no skipped levels)"""
        levels = []
        for level in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
            if headings.get(level):
                levels.append(int(level[1]))
        
        if not levels:
            return False
        
        # Check for skipped levels
        for i in range(len(levels) - 1):
            if levels[i + 1] - levels[i] > 1:
                return False
        
        return True
    
    def extract_keywords_tfidf(self, text):
        """Extract keywords using TF-IDF"""
        if not text or len(text.split()) < 10:
            return {'top_keywords': [], 'keyword_density': {}}
        
        try:
            # Clean text
            words = re.findall(r'\b[a-zA-Z]{4,}\b', text.lower())
            
            if len(words) < 10:
                return {'top_keywords': [], 'keyword_density': {}}
            
            # Use TF-IDF
            vectorizer = TfidfVectorizer(max_features=20, stop_words='english')
            tfidf_matrix = vectorizer.fit_transform([text])
            feature_names = vectorizer.get_feature_names_out()
            
            # Get scores
            scores = tfidf_matrix.toarray()[0]
            keyword_scores = list(zip(feature_names, scores))
            keyword_scores.sort(key=lambda x: x[1], reverse=True)
            
            # Calculate keyword density
            word_count = len(words)
            word_freq = Counter(words)
            
            top_keywords = []
            keyword_density = {}
            
            for keyword, score in keyword_scores[:10]:
                count = word_freq.get(keyword, 0)
                density = round((count / word_count) * 100, 2)
                top_keywords.append({
                    'keyword': keyword,
                    'tfidf_score': round(score, 3),
                    'count': count,
                    'density': density
                })
                keyword_density[keyword] = density
            
            return {
                'top_keywords': top_keywords,
                'keyword_density': keyword_density
            }
        except:
            # Fallback to simple frequency
            words = re.findall(r'\b[a-zA-Z]{4,}\b', text.lower())
            word_freq = Counter(words)
            top_words = word_freq.most_common(10)
            
            return {
                'top_keywords': [{'keyword': w, 'count': c, 'density': 0} for w, c in top_words],
                'keyword_density': {}
            }
    
    def get_reading_level(self, flesch_score):
        """Convert Flesch score to reading level"""
        if flesch_score >= 90:
            return "Very Easy (5th grade)"
        elif flesch_score >= 80:
            return "Easy (6th grade)"
        elif flesch_score >= 70:
            return "Fairly Easy (7th grade)"
        elif flesch_score >= 60:
            return "Standard (8th-9th grade)"
        elif flesch_score >= 50:
            return "Fairly Difficult (10th-12th grade)"
        elif flesch_score >= 30:
            return "Difficult (College)"
        else:
            return "Very Difficult (College graduate)"
    
    def generate_issues(self, page_data, analysis):
        """Generate specific issues and recommendations"""
        tech = analysis['technical_seo']['details']
        content = analysis['content_seo']['details']
        access = analysis['accessibility']['details']
        
        # Critical issues
        if tech.get('title_status') == 'missing':
            analysis['issues'].append({
                'severity': 'critical',
                'category': 'Technical SEO',
                'issue': 'Missing title tag',
                'recommendation': 'Add a unique, descriptive title tag (50-60 characters)'
            })
        
        if tech.get('meta_status') == 'missing':
            analysis['issues'].append({
                'severity': 'critical',
                'category': 'Technical SEO',
                'issue': 'Missing meta description',
                'recommendation': 'Add a compelling meta description (150-160 characters)'
            })
        
        if tech.get('h1_status') == 'missing':
            analysis['issues'].append({
                'severity': 'critical',
                'category': 'Technical SEO',
                'issue': 'Missing H1 tag',
                'recommendation': 'Add exactly one H1 tag that describes the page content'
            })
        
        # Warnings
        if tech.get('title_status') == 'needs_optimization':
            title_len = tech.get('title_length', 0)
            if title_len < self.IDEAL_TITLE_MIN:
                analysis['warnings'].append({
                    'severity': 'warning',
                    'category': 'Technical SEO',
                    'issue': f'Title too short ({title_len} characters)',
                    'recommendation': f'Expand title to {self.IDEAL_TITLE_MIN}-{self.IDEAL_TITLE_MAX} characters'
                })
            elif title_len > self.IDEAL_TITLE_MAX:
                analysis['warnings'].append({
                    'severity': 'warning',
                    'category': 'Technical SEO',
                    'issue': f'Title too long ({title_len} characters)',
                    'recommendation': f'Shorten title to {self.IDEAL_TITLE_MIN}-{self.IDEAL_TITLE_MAX} characters'
                })
        
        if tech.get('h1_status') == 'multiple':
            analysis['warnings'].append({
                'severity': 'warning',
                'category': 'Technical SEO',
                'issue': f'Multiple H1 tags found ({tech.get("h1_count")})',
                'recommendation': 'Use only one H1 tag per page for better SEO'
            })
        
        if content.get('word_count_status') == 'low':
            analysis['warnings'].append({
                'severity': 'warning',
                'category': 'Content SEO',
                'issue': f'Low word count ({content.get("word_count")} words)',
                'recommendation': f'Add more content. Aim for at least {self.MIN_WORD_COUNT} words'
            })
        
        if access.get('images_without_alt', 0) > 0:
            analysis['warnings'].append({
                'severity': 'warning',
                'category': 'Accessibility',
                'issue': f'{access.get("images_without_alt")} images missing alt text',
                'recommendation': 'Add descriptive alt text to all images for accessibility and SEO'
            })
        
        # Recommendations
        if not tech.get('has_canonical'):
            analysis['recommendations'].append({
                'category': 'Technical SEO',
                'recommendation': 'Add a canonical URL to avoid duplicate content issues'
            })
        
        if tech.get('og_tags_status') != 'good':
            analysis['recommendations'].append({
                'category': 'Technical SEO',
                'recommendation': 'Add Open Graph tags for better social media sharing'
            })
        
        if content.get('readability_status') == 'needs_improvement':
            analysis['recommendations'].append({
                'category': 'Content SEO',
                'recommendation': 'Improve readability by using shorter sentences and simpler words'
            })
    
    def calculate_overall_score(self, page_analysis):
        """Calculate overall SEO score from all categories"""
        if 'error' in page_analysis:
            return 0
        
        tech_score = page_analysis['technical_seo']['percentage']
        content_score = page_analysis['content_seo']['percentage']
        access_score = page_analysis['accessibility']['percentage']
        
        # Weighted average (Technical: 40%, Content: 40%, Accessibility: 20%)
        overall = (tech_score * 0.4) + (content_score * 0.4) + (access_score * 0.2)
        
        return round(overall, 1)
    
    def analyze_all_pages(self, crawl_data):
        """Analyze all crawled pages"""
        pages_analysis = []
        
        for page in crawl_data['pages']:
            analysis = self.analyze_page(page)
            if 'error' not in analysis:
                analysis['overall_score'] = self.calculate_overall_score(analysis)
            pages_analysis.append(analysis)
        
        # Generate site-wide summary
        summary = self.generate_site_summary(pages_analysis, crawl_data)
        
        return {
            'pages': pages_analysis,
            'summary': summary,
            'broken_links': crawl_data.get('broken_links', [])
        }
    
    def generate_site_summary(self, pages_analysis, crawl_data):
        """Generate overall site summary"""
        valid_pages = [p for p in pages_analysis if 'error' not in p]
        
        if not valid_pages:
            return {'error': 'No valid pages analyzed'}
        
        # Calculate average scores
        avg_overall = sum(p['overall_score'] for p in valid_pages) / len(valid_pages)
        avg_technical = sum(p['technical_seo']['percentage'] for p in valid_pages) / len(valid_pages)
        avg_content = sum(p['content_seo']['percentage'] for p in valid_pages) / len(valid_pages)
        avg_accessibility = sum(p['accessibility']['percentage'] for p in valid_pages) / len(valid_pages)
        
        # Count issues
        total_critical = sum(len(p.get('issues', [])) for p in valid_pages)
        total_warnings = sum(len(p.get('warnings', [])) for p in valid_pages)
        
        # Find common issues
        all_issues = []
        for p in valid_pages:
            all_issues.extend(p.get('issues', []))
            all_issues.extend(p.get('warnings', []))
        
        issue_types = Counter(i['issue'] for i in all_issues)
        common_issues = issue_types.most_common(5)
        
        return {
            'total_pages_analyzed': len(valid_pages),
            'total_pages_crawled': crawl_data.get('total_pages_crawled', 0),
            'total_broken_links': len(crawl_data.get('broken_links', [])),
            'average_scores': {
                'overall': round(avg_overall, 1),
                'technical_seo': round(avg_technical, 1),
                'content_seo': round(avg_content, 1),
                'accessibility': round(avg_accessibility, 1)
            },
            'total_issues': {
                'critical': total_critical,
                'warnings': total_warnings
            },
            'common_issues': [{'issue': issue, 'count': count} for issue, count in common_issues],
            'health_status': self.get_health_status(avg_overall)
        }
    
    def get_health_status(self, score):
        """Get health status based on score"""
        if score >= 80:
            return 'excellent'
        elif score >= 60:
            return 'good'
        elif score >= 40:
            return 'needs_improvement'
        else:
            return 'poor'
    
    def generate_positive_highlights(self, page_data, analysis):
        """Generate positive feedback about what's working well"""
        tech = analysis['technical_seo']['details']
        content = analysis['content_seo']['details']
        access = analysis['accessibility']['details']
        
        highlights = []
        
        # Technical SEO Positives
        if tech.get('title_status') == 'optimal':
            highlights.append({
                'category': 'Technical SEO',
                'icon': 'check-circle',
                'highlight': f'Perfect title length ({tech.get("title_length")} characters)',
                'detail': 'Your title is optimally sized for search results'
            })
        
        if tech.get('meta_status') == 'optimal':
            highlights.append({
                'category': 'Technical SEO',
                'icon': 'check-circle',
                'highlight': f'Ideal meta description ({tech.get("meta_length")} characters)',
                'detail': 'Meta description is perfectly sized for search snippets'
            })
        
        if tech.get('h1_status') == 'optimal':
            highlights.append({
                'category': 'Technical SEO',
                'icon': 'check-circle',
                'highlight': 'Perfect H1 structure',
                'detail': 'Exactly one H1 tag - ideal for SEO'
            })
        
        if tech.get('heading_hierarchy') == 'valid':
            highlights.append({
                'category': 'Technical SEO',
                'icon': 'check-circle',
                'highlight': 'Valid heading hierarchy',
                'detail': 'Headings follow proper H1→H2→H3 structure'
            })
        
        if tech.get('has_canonical'):
            highlights.append({
                'category': 'Technical SEO',
                'icon': 'check-circle',
                'highlight': 'Canonical URL present',
                'detail': 'Helps prevent duplicate content issues'
            })
        
        if tech.get('og_tags_status') == 'good':
            highlights.append({
                'category': 'Technical SEO',
                'icon': 'check-circle',
                'highlight': 'Rich Open Graph tags',
                'detail': 'Great social media sharing optimization'
            })
        
        if tech.get('status') == 'ok':
            highlights.append({
                'category': 'Technical SEO',
                'icon': 'check-circle',
                'highlight': 'Page loads successfully',
                'detail': 'HTTP 200 status - no server errors'
            })
        
        # Content SEO Positives
        if content.get('word_count_status') in ['excellent', 'good']:
            word_count = content.get('word_count', 0)
            highlights.append({
                'category': 'Content SEO',
                'icon': 'check-circle',
                'highlight': f'Substantial content ({word_count} words)',
                'detail': 'Good amount of content for search engines'
            })
        
        if content.get('readability_status') == 'optimal':
            highlights.append({
                'category': 'Content SEO',
                'icon': 'check-circle',
                'highlight': 'Excellent readability',
                'detail': f'Easy to read - {content.get("reading_level", "")}'
            })
        
        if content.get('tone') == 'Positive':
            highlights.append({
                'category': 'Content SEO',
                'icon': 'check-circle',
                'highlight': 'Positive tone detected',
                'detail': 'Content has an engaging, positive sentiment'
            })
        
        if content.get('content_structure') == 'well_structured':
            highlights.append({
                'category': 'Content SEO',
                'icon': 'check-circle',
                'highlight': 'Well-structured content',
                'detail': f'{content.get("total_headings", 0)} headings organize the content'
            })
        
        if content.get('keyword_status') == 'good':
            highlights.append({
                'category': 'Content SEO',
                'icon': 'check-circle',
                'highlight': 'Good keyword usage',
                'detail': 'Content contains relevant keywords'
            })
        
        # Accessibility Positives
        if access.get('alt_text_status') in ['excellent', 'good']:
            percentage = access.get('images_with_alt_percentage', 0)
            highlights.append({
                'category': 'Accessibility',
                'icon': 'check-circle',
                'highlight': f'{percentage}% of images have alt text',
                'detail': 'Great for accessibility and SEO'
            })
        
        if access.get('heading_accessibility') == 'good':
            highlights.append({
                'category': 'Accessibility',
                'icon': 'check-circle',
                'highlight': 'Screen reader friendly headings',
                'detail': 'Proper heading structure for accessibility'
            })
        
        if access.get('link_text_status') in ['excellent', 'good']:
            highlights.append({
                'category': 'Accessibility',
                'icon': 'check-circle',
                'highlight': 'Descriptive link text',
                'detail': 'Links have meaningful text for screen readers'
            })
        
        # Overall Score Highlights
        overall_score = analysis['technical_seo']['percentage']
        if overall_score >= 80:
            highlights.append({
                'category': 'Overall',
                'icon': 'award',
                'highlight': 'Excellent technical SEO!',
                'detail': f'{overall_score}% technical SEO score'
            })
        
        content_score = analysis['content_seo']['percentage']
        if content_score >= 80:
            highlights.append({
                'category': 'Overall',
                'icon': 'award',
                'highlight': 'Outstanding content quality!',
                'detail': f'{content_score}% content SEO score'
            })
        
        access_score = analysis['accessibility']['percentage']
        if access_score >= 80:
            highlights.append({
                'category': 'Overall',
                'icon': 'award',
                'highlight': 'Highly accessible!',
                'detail': f'{access_score}% accessibility score'
            })
        
        analysis['positive_highlights'] = highlights
