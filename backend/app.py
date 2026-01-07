from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from crawler import SEOCrawler
from analyzer import SEOAnalyzer
from report_generator import PDFReportGenerator, generate_csv_export
from datetime import datetime
import json
import os

app = Flask(__name__)
CORS(app)

# Store recent audits in memory (in production, use a database)
recent_audits = []

@app.route('/api/audit', methods=['POST'])
def audit():
    """Main SEO audit endpoint"""
    try:
        data = request.json
        url = data.get('url')
        max_pages = data.get('max_pages', 5)
        max_depth = data.get('max_depth', 2)
        
        if not url:
            return jsonify({"error": "URL is required"}), 400
        
        # Validate URL format
        if not url.startswith(('http://', 'https://')):
            return jsonify({"error": "URL must start with http:// or https://"}), 400
        
        print(f"Starting audit for: {url}")
        
        # Step 1: Crawl website
        crawler = SEOCrawler(url, max_pages=max_pages, max_depth=max_depth)
        crawl_data = crawler.crawl()
        
        print(f"Crawled {len(crawl_data['pages'])} pages")
        
        # Step 2: Analyze SEO
        analyzer = SEOAnalyzer()
        analysis = analyzer.analyze_all_pages(crawl_data)
        
        print(f"Analysis complete")
        
        # Step 3: Generate AI advice
        ai_advice = generate_ai_advice(analysis)
        
        # Prepare response
        response_data = {
            "url": url,
            "timestamp": datetime.now().isoformat(),
            "analysis": analysis,
            "ai_advice": ai_advice,
            "crawl_stats": {
                "pages_crawled": crawl_data['total_pages_crawled'],
                "links_found": crawl_data['total_links_found'],
                "broken_links": len(crawl_data.get('broken_links', []))
            }
        }
        
        # Store in recent audits (limit to last 10)
        recent_audits.insert(0, {
            'url': url,
            'timestamp': datetime.now().isoformat(),
            'overall_score': analysis['summary'].get('average_scores', {}).get('overall', 0)
        })
        if len(recent_audits) > 10:
            recent_audits.pop()
        
        return jsonify(response_data)
        
    except Exception as e:
        print(f"Error during audit: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500

@app.route('/api/export/pdf', methods=['POST'])
def export_pdf():
    """Export audit results as PDF"""
    try:
        data = request.json
        analysis_data = data.get('analysis')
        url = data.get('url', 'Unknown')
        
        if not analysis_data:
            return jsonify({"error": "Analysis data is required"}), 400
        
        # Generate PDF
        pdf_generator = PDFReportGenerator()
        pdf_buffer = pdf_generator.generate_pdf(analysis_data, url)
        
        # Create filename
        filename = f"seo_audit_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        
        # Create response with explicit headers to force download
        response = send_file(
            pdf_buffer,
            mimetype='application/pdf',
            as_attachment=True,
            download_name=filename
        )
        
        # Add explicit headers to force download
        response.headers['Content-Disposition'] = f'attachment; filename="{filename}"'
        response.headers['Content-Type'] = 'application/pdf'
        
        return response
        
    except Exception as e:
        print(f"Error generating PDF: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/export/csv', methods=['POST'])
def export_csv():
    """Export audit results as CSV"""
    try:
        data = request.json
        analysis_data = data.get('analysis')
        
        if not analysis_data:
            return jsonify({"error": "Analysis data is required"}), 400
        
        # Generate CSV
        csv_data = generate_csv_export(analysis_data)
        
        # Create filename
        filename = f"seo_audit_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        from io import BytesIO
        csv_buffer = BytesIO(csv_data.encode('utf-8'))
        csv_buffer.seek(0)
        
        response = send_file(
            csv_buffer,
            mimetype='text/csv',
            as_attachment=True,
            download_name=filename
        )
        
        # Add explicit headers to force download
        response.headers['Content-Disposition'] = f'attachment; filename="{filename}"'
        response.headers['Content-Type'] = 'text/csv'
        
        return response
        
    except Exception as e:
        print(f"Error generating CSV: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/export/json', methods=['POST'])
def export_json():
    """Export audit results as JSON"""
    try:
        data = request.json
        analysis_data = data.get('analysis')
        url = data.get('url', 'Unknown')
        
        if not analysis_data:
            return jsonify({"error": "Analysis data is required"}), 400
        
        # Create filename
        filename = f"seo_audit_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        # Prepare JSON data
        export_data = {
            'url': url,
            'timestamp': datetime.now().isoformat(),
            'analysis': analysis_data
        }
        
        from io import BytesIO
        json_buffer = BytesIO(json.dumps(export_data, indent=2).encode('utf-8'))
        json_buffer.seek(0)
        
        response = send_file(
            json_buffer,
            mimetype='application/json',
            as_attachment=True,
            download_name=filename
        )
        
        # Add explicit headers to force download
        response.headers['Content-Disposition'] = f'attachment; filename="{filename}"'
        response.headers['Content-Type'] = 'application/json'
        
        return response
        
    except Exception as e:
        print(f"Error generating JSON: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/history', methods=['GET'])
def get_history():
    """Get recent audit history"""
    return jsonify({"history": recent_audits})

@app.route('/api/quick-check', methods=['POST'])
def quick_check():
    """Quick single-page SEO check (faster than full audit)"""
    try:
        data = request.json
        url = data.get('url')
        
        if not url:
            return jsonify({"error": "URL is required"}), 400
        
        # Validate URL format
        if not url.startswith(('http://', 'https://')):
            return jsonify({"error": "URL must start with http:// or https://"}), 400
        
        # Crawl single page only
        crawler = SEOCrawler(url, max_pages=1, max_depth=0)
        crawl_data = crawler.crawl()
        
        if not crawl_data['pages']:
            return jsonify({"error": "Failed to crawl page"}), 500
        
        # Analyze single page
        analyzer = SEOAnalyzer()
        page_data = crawl_data['pages'][0]
        analysis = analyzer.analyze_page(page_data)
        
        if 'error' not in analysis:
            analysis['overall_score'] = analyzer.calculate_overall_score(analysis)
        
        return jsonify({
            "url": url,
            "analysis": analysis,
            "quick_check": True
        })
        
    except Exception as e:
        print(f"Error during quick check: {str(e)}")
        return jsonify({"error": str(e)}), 500

def generate_ai_advice(analysis):
    """Generate AI-powered advice based on analysis"""
    advice = []
    
    if 'summary' not in analysis:
        return advice
    
    summary = analysis['summary']
    avg_scores = summary.get('average_scores', {})
    
    # Overall advice
    overall_score = avg_scores.get('overall', 0)
    
    if overall_score >= 80:
        advice.append({
            'type': 'success',
            'category': 'Overall',
            'message': '🎉 Excellent SEO! Your website is well-optimized. Focus on maintaining quality and monitoring performance.'
        })
    elif overall_score >= 60:
        advice.append({
            'type': 'info',
            'category': 'Overall',
            'message': '👍 Good SEO foundation. Address the warnings to reach excellent status.'
        })
    elif overall_score >= 40:
        advice.append({
            'type': 'warning',
            'category': 'Overall',
            'message': '⚠️ Your SEO needs improvement. Focus on critical issues first.'
        })
    else:
        advice.append({
            'type': 'critical',
            'category': 'Overall',
            'message': '🚨 Critical SEO issues detected. Immediate action required to improve search visibility.'
        })
    
    # Technical SEO advice
    tech_score = avg_scores.get('technical_seo', 0)
    if tech_score < 60:
        advice.append({
            'type': 'critical',
            'category': 'Technical SEO',
            'message': 'Fix missing title tags, meta descriptions, and H1 tags. These are fundamental for SEO.'
        })
    
    # Content SEO advice
    content_score = avg_scores.get('content_seo', 0)
    if content_score < 60:
        advice.append({
            'type': 'warning',
            'category': 'Content SEO',
            'message': 'Improve content quality by adding more text, improving readability, and using relevant keywords.'
        })
    
    # Accessibility advice
    access_score = avg_scores.get('accessibility', 0)
    if access_score < 70:
        advice.append({
            'type': 'warning',
            'category': 'Accessibility',
            'message': 'Add alt text to images and ensure proper link text for better accessibility and SEO.'
        })
    
    # Broken links advice
    if summary.get('total_broken_links', 0) > 0:
        advice.append({
            'type': 'critical',
            'category': 'Technical',
            'message': f'Fix {summary["total_broken_links"]} broken link(s). Broken links hurt user experience and SEO.'
        })
    
    # Common issues advice
    if summary.get('common_issues'):
        top_issue = summary['common_issues'][0]
        advice.append({
            'type': 'info',
            'category': 'Priority',
            'message': f'Most common issue: "{top_issue["issue"]}" found on {top_issue["count"]} page(s). Fix this across your site.'
        })
    
    # Specific recommendations based on patterns
    pages = analysis.get('pages', [])
    if pages:
        # Check for content length issues
        low_content_pages = sum(1 for p in pages 
                               if 'error' not in p and 
                               p.get('content_seo', {}).get('details', {}).get('word_count', 0) < 300)
        
        if low_content_pages > len(pages) * 0.5:
            advice.append({
                'type': 'warning',
                'category': 'Content Strategy',
                'message': f'{low_content_pages} page(s) have low word count. Add comprehensive, valuable content to improve rankings.'
            })
        
        # Check for readability issues
        poor_readability = sum(1 for p in pages 
                              if 'error' not in p and 
                              p.get('content_seo', {}).get('details', {}).get('readability_status') == 'needs_improvement')
        
        if poor_readability > 0:
            advice.append({
                'type': 'info',
                'category': 'Content Quality',
                'message': 'Improve readability by using shorter sentences, simpler words, and better formatting.'
            })
    
    return advice

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "timestamp": datetime.now().isoformat()})

if __name__ == "__main__":
    print("🚀 SEO Audit Platform Starting...")
    print("📊 Backend running on http://127.0.0.1:5000")
    print("🔍 Ready to analyze websites!")
    app.run(debug=True, port=5000)
