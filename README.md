# 🚀 AI-Powered SEO Audit Platform

A comprehensive, full-stack SEO audit tool that analyzes websites and provides AI-driven insights, technical SEO checks, content analysis, and actionable recommendations.

## ✨ Features

### Must-Have Features (100% Implemented)

#### 1. URL Crawl & Page Analysis ✅
- Multi-page crawling with configurable depth
- Broken link detection (4xx/5xx errors)
- Duplicate title tag detection
- Meta description validation
- H1 tag analysis
- Per-page structured reports

#### 2. On-Page SEO Metrics ✅
- Title length validation (50-60 chars optimal)
- Meta description length check (150-160 chars optimal)
- H1-H6 hierarchy validation
- Image alt attribute detection
- Keyword presence analysis in title/meta/headings

#### 3. AI-Based Content Analysis ✅
- **Readability Score** (Flesch Reading Ease)
- **Sentiment Analysis** (Positive/Neutral/Negative)
- Content quality insights
- Reading level assessment

#### 4. Keyword & Content Suggestions ✅
- **TF-IDF keyword extraction**
- Keyword density analysis
- Top keywords identification
- Content expansion recommendations

#### 5. SEO Score & Health Summary ✅
- Overall SEO score (0-100)
- Section-wise scoring:
  - Technical SEO (40% weight)
  - Content SEO (40% weight)
  - Accessibility (20% weight)
- Color-coded indicators (Excellent/Good/Needs Improvement/Poor)

#### 6. Dashboard UI ✅
- Modern dark mode design
- Progress indicators
- Tab-based report layout:
  - Overview
  - Technical Issues
  - Content Analysis
  - Page Details
  - AI Insights
- Charts and visualizations
- Premium glassmorphism design

#### 7. Export & Reporting ✅
- **PDF export** with professional formatting
- **CSV export** for data analysis
- **JSON export** for programmatic access
- Timestamped reports

## 🛠️ Tech Stack

### Backend
- **Flask** - Python web framework
- **BeautifulSoup4** - HTML parsing
- **TextBlob** - Sentiment analysis
- **textstat** - Readability metrics
- **scikit-learn** - TF-IDF keyword extraction
- **ReportLab** - PDF generation

### Frontend
- **React 19** - UI framework
- **Modern CSS** - Premium dark mode design
- **Google Fonts (Inter)** - Typography

## 📋 Prerequisites

- Python 3.8 or higher
- Node.js 16 or higher
- npm or yarn

## 🚀 Installation & Setup

### 1. Clone or Navigate to Project

```bash
cd "c:\Users\harik\Desktop\SEO dashboard AI"
```

### 2. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Install Python dependencies
pip install -r requirements.txt

# Download TextBlob corpora (required for sentiment analysis)
python -m textblob.download_corpora
```

### 3. Frontend Setup

```bash
# Navigate to frontend directory
cd ../frontend

# Install Node dependencies
npm install
```

## 🎯 Running the Application

### Option 1: Run Both Servers Separately

#### Terminal 1 - Backend
```bash
cd backend
python app.py
```
Backend will run on: `http://127.0.0.1:5000`

#### Terminal 2 - Frontend
```bash
cd frontend
npm start
```
Frontend will run on: `http://localhost:3000`

### Option 2: Quick Start (PowerShell)

```powershell
# Start backend in background
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd 'c:\Users\harik\Desktop\SEO dashboard AI\backend'; python app.py"

# Start frontend
cd "c:\Users\harik\Desktop\SEO dashboard AI\frontend"
npm start
```

## 📖 Usage Guide

### Basic Usage

1. **Enter URL**: Type or paste a website URL (must include `http://` or `https://`)
2. **Configure Options**:
   - **Max Pages**: Number of pages to crawl (1-20)
   - **Crawl Depth**: How deep to crawl (0-3 levels)
3. **Run Audit**: Click "Run Full Audit" button
4. **View Results**: Explore different tabs for detailed insights
5. **Export Report**: Download as PDF, CSV, or JSON

### Understanding Scores

- **80-100**: 🟢 Excellent - Well optimized
- **60-79**: 🔵 Good - Minor improvements needed
- **40-59**: 🟡 Needs Improvement - Several issues to fix
- **0-39**: 🔴 Poor - Critical issues require immediate attention

### Tab Descriptions

- **📊 Overview**: Summary statistics and common issues
- **⚙️ Technical Issues**: Critical SEO problems and broken links
- **📝 Content Analysis**: Content quality, readability, and keywords
- **📄 Page Details**: Individual page analysis and scores
- **🤖 AI Insights**: AI-generated recommendations

## 🔍 API Endpoints

### POST /api/audit
Full website audit with crawling and analysis.

**Request:**
```json
{
  "url": "https://example.com",
  "max_pages": 5,
  "max_depth": 2
}
```

### POST /api/quick-check
Quick single-page analysis (faster).

**Request:**
```json
{
  "url": "https://example.com"
}
```

### POST /api/export/pdf
Export audit results as PDF.

### POST /api/export/csv
Export audit results as CSV.

### POST /api/export/json
Export audit results as JSON.

### GET /api/history
Get recent audit history.

## 🎨 Design Features

- **Dark Mode**: Premium dark theme with gradient accents
- **Glassmorphism**: Modern frosted glass effects
- **Smooth Animations**: Micro-interactions and transitions
- **Responsive Design**: Works on all screen sizes
- **Color-Coded Scores**: Visual feedback for quick assessment
- **Progress Indicators**: Real-time crawling feedback

## 📊 What This Project Demonstrates

✅ **Real-world Problem Solving** - Practical SEO analysis tool  
✅ **SEO Domain Understanding** - Comprehensive SEO knowledge  
✅ **Python Data Processing** - Web scraping, NLP, data analysis  
✅ **Practical AI/NLP Usage** - Sentiment analysis, TF-IDF, readability  
✅ **Full-Stack Capability** - Flask backend + React frontend  
✅ **Professional UI/UX** - Modern, premium design  
✅ **Export Functionality** - PDF, CSV, JSON generation  

## 🐛 Troubleshooting

### Backend Issues

**Error: Module not found**
```bash
pip install -r requirements.txt
python -m textblob.download_corpora
```

**Error: Port 5000 already in use**
```python
# In app.py, change the port:
app.run(debug=True, port=5001)
```

### Frontend Issues

**Error: npm install fails**
```bash
# Clear cache and reinstall
npm cache clean --force
rm -rf node_modules package-lock.json
npm install
```

**CORS errors**
- Ensure backend is running on port 5000
- Check that Flask-CORS is installed

## 📝 Project Structure

```
SEO dashboard AI/
├── backend/
│   ├── app.py              # Flask application
│   ├── crawler.py          # Multi-page crawler
│   ├── analyzer.py         # SEO analysis engine
│   ├── scraper.py          # (Legacy - replaced by crawler.py)
│   ├── report_generator.py # PDF/CSV export
│   └── requirements.txt    # Python dependencies
├── frontend/
│   ├── public/
│   │   └── index.html      # HTML template
│   ├── src/
│   │   ├── App.js          # Main React component
│   │   ├── App.css         # Premium styling
│   │   └── index.js        # React entry point
│   └── package.json        # Node dependencies
└── README.md               # This file
```

## 🚀 Future Enhancements (Optional)

- [ ] Competitor URL comparison
- [ ] Mobile-friendliness checks
- [ ] Page load time estimation
- [ ] User authentication & saved audits
- [ ] Historical trend analysis
- [ ] Scheduled audits
- [ ] Email reports

## 📄 License

This project is for educational and portfolio purposes.

## 👨‍💻 Author

Built as a demonstration of full-stack development, SEO expertise, and AI/NLP integration.

---

**Happy Auditing! 🚀**
