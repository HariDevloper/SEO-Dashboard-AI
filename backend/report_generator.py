from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from reportlab.pdfgen import canvas
from datetime import datetime
import io

class PDFReportGenerator:
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self.setup_custom_styles()
    
    def setup_custom_styles(self):
        """Setup custom paragraph styles"""
        # Title style
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1e293b'),
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))
        
        # Heading style
        self.styles.add(ParagraphStyle(
            name='CustomHeading',
            parent=self.styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#334155'),
            spaceAfter=12,
            spaceBefore=12,
            fontName='Helvetica-Bold'
        ))
        
        # Subheading style
        self.styles.add(ParagraphStyle(
            name='CustomSubHeading',
            parent=self.styles['Heading3'],
            fontSize=12,
            textColor=colors.HexColor('#475569'),
            spaceAfter=8,
            fontName='Helvetica-Bold'
        ))
        
        # Body text
        self.styles.add(ParagraphStyle(
            name='CustomBody',
            parent=self.styles['Normal'],
            fontSize=10,
            textColor=colors.HexColor('#1e293b'),
            spaceAfter=6
        ))
    
    def get_score_color(self, score):
        """Get color based on score"""
        if score >= 80:
            return colors.HexColor('#10b981')  # Green
        elif score >= 60:
            return colors.HexColor('#3b82f6')  # Blue
        elif score >= 40:
            return colors.HexColor('#f59e0b')  # Orange
        else:
            return colors.HexColor('#ef4444')  # Red
    
    def get_severity_color(self, severity):
        """Get color based on severity"""
        if severity == 'critical':
            return colors.HexColor('#ef4444')
        elif severity == 'warning':
            return colors.HexColor('#f59e0b')
        else:
            return colors.HexColor('#3b82f6')
    
    def generate_pdf(self, analysis_data, url):
        """Generate PDF report"""
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter,
                                rightMargin=72, leftMargin=72,
                                topMargin=72, bottomMargin=18)
        
        story = []
        
        # Title
        story.append(Paragraph("SEO Audit Report", self.styles['CustomTitle']))
        story.append(Spacer(1, 12))
        
        # URL and date
        story.append(Paragraph(f"<b>Website:</b> {url}", self.styles['CustomBody']))
        story.append(Paragraph(f"<b>Generated:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", 
                              self.styles['CustomBody']))
        story.append(Spacer(1, 20))
        
        # Executive Summary
        if 'summary' in analysis_data:
            story.extend(self.create_summary_section(analysis_data['summary']))
        
        # Overall Scores
        if 'pages' in analysis_data and analysis_data['pages']:
            story.extend(self.create_scores_section(analysis_data))
        
        # Broken Links
        if analysis_data.get('broken_links'):
            story.extend(self.create_broken_links_section(analysis_data['broken_links']))
        
        # Page-by-page analysis
        if 'pages' in analysis_data:
            story.extend(self.create_pages_section(analysis_data['pages']))
        
        # Build PDF
        doc.build(story)
        buffer.seek(0)
        return buffer
    
    def create_summary_section(self, summary):
        """Create executive summary section"""
        elements = []
        
        elements.append(Paragraph("Executive Summary", self.styles['CustomHeading']))
        elements.append(Spacer(1, 12))
        
        # Summary stats table
        data = [
            ['Metric', 'Value'],
            ['Pages Analyzed', str(summary.get('total_pages_analyzed', 0))],
            ['Broken Links Found', str(summary.get('total_broken_links', 0))],
            ['Critical Issues', str(summary.get('total_issues', {}).get('critical', 0))],
            ['Warnings', str(summary.get('total_issues', {}).get('warnings', 0))],
            ['Health Status', summary.get('health_status', 'Unknown').upper()]
        ]
        
        table = Table(data, colWidths=[3*inch, 2*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e293b')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        elements.append(table)
        elements.append(Spacer(1, 20))
        
        # Average scores
        if 'average_scores' in summary:
            elements.append(Paragraph("Average Scores", self.styles['CustomSubHeading']))
            scores = summary['average_scores']
            
            score_data = [
                ['Category', 'Score', 'Status'],
                ['Overall SEO', f"{scores.get('overall', 0)}%", ''],
                ['Technical SEO', f"{scores.get('technical_seo', 0)}%", ''],
                ['Content SEO', f"{scores.get('content_seo', 0)}%", ''],
                ['Accessibility', f"{scores.get('accessibility', 0)}%", '']
            ]
            
            score_table = Table(score_data, colWidths=[2*inch, 1.5*inch, 1.5*inch])
            score_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e293b')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 11),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            elements.append(score_table)
            elements.append(Spacer(1, 20))
        
        # Common issues
        if summary.get('common_issues'):
            elements.append(Paragraph("Most Common Issues", self.styles['CustomSubHeading']))
            
            for issue in summary['common_issues'][:5]:
                elements.append(Paragraph(
                    f"• {issue['issue']} (found on {issue['count']} page(s))",
                    self.styles['CustomBody']
                ))
            
            elements.append(Spacer(1, 20))
        
        elements.append(PageBreak())
        return elements
    
    def create_scores_section(self, analysis_data):
        """Create scores overview section"""
        elements = []
        
        elements.append(Paragraph("SEO Scores Overview", self.styles['CustomHeading']))
        elements.append(Spacer(1, 12))
        
        pages = [p for p in analysis_data['pages'] if 'error' not in p]
        
        if pages:
            # Create scores table
            data = [['Page', 'Overall', 'Technical', 'Content', 'Accessibility']]
            
            for page in pages[:10]:  # Limit to first 10 pages
                url = page['url']
                if len(url) > 50:
                    url = url[:47] + '...'
                
                data.append([
                    url,
                    f"{page.get('overall_score', 0)}%",
                    f"{page['technical_seo']['percentage']}%",
                    f"{page['content_seo']['percentage']}%",
                    f"{page['accessibility']['percentage']}%"
                ])
            
            table = Table(data, colWidths=[2.5*inch, 1*inch, 1*inch, 1*inch, 1*inch])
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1e293b')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
                ('ALIGN', (0, 0), (0, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 9),
                ('FONTSIZE', (0, 1), (-1, -1), 8),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            elements.append(table)
            elements.append(Spacer(1, 20))
        
        return elements
    
    def create_broken_links_section(self, broken_links):
        """Create broken links section"""
        elements = []
        
        if not broken_links:
            return elements
        
        elements.append(Paragraph(f"Broken Links ({len(broken_links)} found)", 
                                 self.styles['CustomHeading']))
        elements.append(Spacer(1, 12))
        
        data = [['Broken URL', 'Status', 'Found On']]
        
        for link in broken_links[:20]:  # Limit to first 20
            url = link['url']
            if len(url) > 40:
                url = url[:37] + '...'
            
            found_on = link['found_on']
            if len(found_on) > 40:
                found_on = found_on[:37] + '...'
            
            data.append([
                url,
                str(link['status_code']),
                found_on
            ])
        
        table = Table(data, colWidths=[2.5*inch, 1*inch, 2.5*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#ef4444')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 9),
            ('FONTSIZE', (0, 1), (-1, -1), 7),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        elements.append(table)
        elements.append(Spacer(1, 20))
        elements.append(PageBreak())
        
        return elements
    
    def create_pages_section(self, pages):
        """Create detailed page analysis section"""
        elements = []
        
        elements.append(Paragraph("Detailed Page Analysis", self.styles['CustomHeading']))
        elements.append(Spacer(1, 12))
        
        for idx, page in enumerate(pages[:5], 1):  # Limit to first 5 pages
            if 'error' in page:
                continue
            
            # Page header
            elements.append(Paragraph(f"Page {idx}: {page['url']}", 
                                     self.styles['CustomSubHeading']))
            elements.append(Spacer(1, 8))
            
            # Scores
            elements.append(Paragraph(
                f"<b>Overall Score:</b> {page.get('overall_score', 0)}% | "
                f"<b>Technical:</b> {page['technical_seo']['percentage']}% | "
                f"<b>Content:</b> {page['content_seo']['percentage']}% | "
                f"<b>Accessibility:</b> {page['accessibility']['percentage']}%",
                self.styles['CustomBody']
            ))
            elements.append(Spacer(1, 8))
            
            # Issues
            if page.get('issues'):
                elements.append(Paragraph("<b>Critical Issues:</b>", self.styles['CustomBody']))
                for issue in page['issues']:
                    elements.append(Paragraph(
                        f"• {issue['issue']}: {issue['recommendation']}",
                        self.styles['CustomBody']
                    ))
                elements.append(Spacer(1, 6))
            
            # Warnings
            if page.get('warnings'):
                elements.append(Paragraph("<b>Warnings:</b>", self.styles['CustomBody']))
                for warning in page['warnings'][:3]:  # Limit to 3 warnings
                    elements.append(Paragraph(
                        f"• {warning['issue']}: {warning['recommendation']}",
                        self.styles['CustomBody']
                    ))
                elements.append(Spacer(1, 6))
            
            # Key metrics
            content_details = page['content_seo']['details']
            if 'word_count' in content_details:
                elements.append(Paragraph(
                    f"<b>Word Count:</b> {content_details['word_count']} | "
                    f"<b>Readability:</b> {content_details.get('reading_level', 'N/A')}",
                    self.styles['CustomBody']
                ))
            
            elements.append(Spacer(1, 15))
        
        return elements

def generate_csv_export(analysis_data):
    """Generate CSV export of analysis data"""
    import csv
    import io
    
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Header
    writer.writerow(['URL', 'Overall Score', 'Technical SEO', 'Content SEO', 
                     'Accessibility', 'Critical Issues', 'Warnings'])
    
    # Data rows
    if 'pages' in analysis_data:
        for page in analysis_data['pages']:
            if 'error' not in page:
                writer.writerow([
                    page['url'],
                    page.get('overall_score', 0),
                    page['technical_seo']['percentage'],
                    page['content_seo']['percentage'],
                    page['accessibility']['percentage'],
                    len(page.get('issues', [])),
                    len(page.get('warnings', []))
                ])
    
    output.seek(0)
    return output.getvalue()
