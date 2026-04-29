# Document Question Answering System

A lightweight keyword-based question answering system for PDF documents built using Streamlit and pdfplumber.

---
## Project Structure
```
DOCREADER/
├── app.py
├── requirements.txt
└── README.md
```
## Features

- Upload and process PDF documents
- Extract and index textual content
- Perform keyword-based search on document content
- Return top relevant excerpts with expandable view
- Highlight the most relevant sentence as a direct answer
- Display document statistics (pages, chunks)

## Requirements

- Python 3.7+
- Dependencies listed in `requirements.txt`

## Installation

1. Clone or download this repository.
2. Install the required packages:

   ```
   pip install -r requirements.txt
   ```

## Usage

1. Run the Streamlit app:

   ```
   streamlit run app.py
   ```

2. Open your browser to the URL shown (usually http://localhost:8501).
3. Upload a PDF file using the file uploader.
4. Enter your question in the text input box.
5. Click "Search" to get the top 3 relevant excerpts.

## How It Works

- **Text Extraction**: Uses pdfplumber to extract all text from the PDF.
- **Chunking**: Splits the text into paragraphs for searching.
- **Keyword Extraction**: Tokenizes the query and removes common stopwords.
- **Scoring Mechanism**: Ranks chunks based on keyword frequency
- **Results**: Returns the top 3 highest-scoring chunks as expandable cards.
- **Answer Extraction**: Selects the most relevant sentence from the top-ranked chunk

## Example Usage
**Sample Query**: "What is the main objective of the document?"
**Output**:
- Top 3 relevant chunks
- Most relevant sentence highlighted

## Limitations
- Uses keyword matching (no semantic understanding)
- May miss context for complex queries
- Performance depends on text quality in PDF

## Future Improvements
- Semantic search using embeddings
- Integration with LLMs (RAG)
- Multi-document support
- Highlighting matched keywords in UI


## Notes

- Uses exact keyword matching (no semantic understanding)
- Best suited for simple factual queries
- NLTK is optional; a fallback stopword list is included