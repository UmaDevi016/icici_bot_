# 🌐 Web Scraping Feature - ICICI Insurance Chatbot

## Overview

The chatbot now combines **TWO sources** of knowledge:
1. **PDF Documentation** (ICICI_Insurance.pdf) - ~150 chunks
2. **Live Website Content** (iciciprulife.com) - ~50 chunks

This dual-source approach provides more comprehensive and up-to-date information.

---

## 🎯 Key Features

### 1. Automatic Web Scraping
- Scrapes important pages from iciciprulife.com
- Extracts clean text content from each page
- Creates searchable chunks from web content

### 2. Source Attribution
Every response now shows its source:
- `📚 Source: PDF` - Information from PDF document
- `📚 Source: Website` - Information from ICICI website
- `📚 Source: PDF and Website` - Combined sources

### 3. Intelligent Chunk Distribution
- **150 chunks** from PDF (detailed documentation)
- **50 chunks** from website (latest online info)
- Total: **~200 chunks** maintained

### 4. Source Tagging
Each chunk is tagged with its origin:
- `[PDF]` prefix for PDF-sourced content
- `[WEB]` prefix for website-sourced content

---

## 📄 Files Added/Modified

### New Files
- **web_scraper.py** (4.9 KB) - Web scraping module
  - ICICIWebScraper class
  - BeautifulSoup-based extraction
  - Chunk creation from web content

### Modified Files
- **chatbot.py** - Enhanced to support dual sources
- **requirements.txt** - Added beautifulsoup4 and lxml
- **README.md** - Updated documentation

---

## 🔧 How It Works

### Step 1: Content Collection
```python
# PDF Processing
processor = PDFProcessor(pdf_path, max_chunks=150)
pdf_chunks = processor.process_pdf()

# Web Scraping
scraper = ICICIWebScraper(max_pages=10)
scraper.scrape_important_pages()
web_chunks = scraper.create_chunks_from_web_content()
```

### Step 2: Source Tagging
```python
pdf_chunks = [f"[PDF] {chunk}" for chunk in pdf_chunks]
web_chunks = [f"[WEB] {chunk}" for chunk in web_chunks]
```

### Step 3: Combined Embeddings
```python
all_chunks = pdf_chunks + web_chunks
embeddings = model.encode(all_chunks)
```

### Step 4: Response with Source
When answering, the bot indicates the source of information.

---

## 🌐 Scraped Website Pages

The scraper targets key pages from iciciprulife.com:

1. **Homepage** - https://www.iciciprulife.com/
2. **Insurance Plans** - /insurance-plans.html
3. **Term Insurance** - /term-insurance.html
4. **Savings Plans** - /savings-plan.html
5. **Pension Plans** - /pension-plans.html
6. **ULIP Plans** - /ulip-plans.html
7. **Death Claims** - /claims/death-claim.html
8. **Maturity Claims** - /claims/maturity-claim.html
9. **About Us** - /about-us.html
10. **Contact** - /contact-us.html

---

## ⚙️ Configuration

You can configure web scraping in `chatbot.py`:

```python
chatbot = ICICIInsuranceChatbot(
    pdf_path="ICICI_Insurance.pdf",
    use_web_content=True,      # Enable/disable web scraping
    max_pdf_chunks=150,         # Max chunks from PDF
    max_web_pages=10            # Max pages to scrape
)
```

### Disable Web Scraping
If you want PDF-only mode:
```python
chatbot = ICICIInsuranceChatbot(use_web_content=False)
```

---

## 📊 Content Distribution

### Before (PDF Only)
```
Total: 200 chunks
├── PDF: 200 chunks
└── Web: 0 chunks
```

### After (PDF + Web)
```
Total: ~200 chunks
├── PDF: ~150 chunks (75%)
└── Web: ~50 chunks (25%)
```

---

## 🎯 Benefits

### 1. **More Current Information**
- Website may have updates not in PDF
- Latest product information
- Current contact details

### 2. **Broader Coverage**
- PDF provides detailed documentation
- Website provides summary and overview
- Combined = Comprehensive knowledge

### 3. **Source Transparency**
- Users know where information comes from
- Can verify with original source
- Builds trust

### 4. **Flexibility**
- Easy to enable/disable web scraping
- Configurable chunk distribution
- Can adjust which pages to scrape

---

## 🧪 Testing

### Test Web Scraper
```bash
python web_scraper.py
```

Expected output:
```
Starting web scraping from ICICI Insurance website...
Scraping: https://www.iciciprulife.com/
Scraping: https://www.iciciprulife.com/insurance-plans.html
...
Scraped X pages successfully
Created Y chunks from web content
```

### Test Chatbot with Dual Sources
```bash
python chatbot.py
```

Look for output showing both sources:
```
✅ Successfully created embeddings for 200 chunks
   - PDF chunks: 150
   - Web chunks: 50
```

---

## 🔒 Polite Scraping

The scraper follows best practices:
- ✅ Respects robots.txt (implicit)
- ✅ 1-second delay between requests
- ✅ Proper User-Agent header
- ✅ Error handling for failed requests
- ✅ Limited to important pages only
- ✅ No aggressive crawling

---

## 🐛 Troubleshooting

### Issue: Web scraping fails
**Solution**: The bot will continue with PDF-only content
```
Warning: Could not scrape web content: [error]
Continuing with PDF content only...
```

### Issue: Some pages return 404
**Normal behavior**: Website structure changes over time. The scraper will skip failed pages and continue with successful ones.

### Issue: Slow first startup
**Expected**: First run scrapes website and creates embeddings. Subsequent runs load cached embeddings instantly.

---

## 🚀 Future Enhancements

Potential improvements:
1. **Dynamic URL Discovery** - Automatically find relevant pages
2. **Scheduled Re-scraping** - Update web content periodically
3. **More Sources** - Add blogs, FAQs, policy documents
4. **Caching Strategy** - Cache web content with expiry
5. **Language Support** - Scrape Hindi/regional pages

---

## 📝 Dependencies

Added to requirements.txt:
```txt
beautifulsoup4>=4.12.0  # HTML parsing
lxml>=4.9.0             # Fast XML/HTML parser
requests>=2.31.0        # HTTP requests
```

---

## ✅ Summary

The web scraping feature enhances the chatbot by:
- ✅ Combining PDF + website content
- ✅ Providing source attribution
- ✅ Maintaining ~200 total chunks
- ✅ Offering more comprehensive answers
- ✅ Keeping information current

**Result**: A more knowledgeable and trustworthy chatbot! 🎉
