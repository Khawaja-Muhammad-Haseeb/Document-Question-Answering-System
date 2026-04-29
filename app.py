import streamlit as st
import pdfplumber
import re

# Optional: NLTK for stopwords
try:
    import nltk
    from nltk.corpus import stopwords
    nltk.download('stopwords', quiet=True)
    nltk.download('punkt', quiet=True)
    USE_NLTK = True
except ImportError:
    USE_NLTK = False

BASIC_STOPWORDS = {"is", "the", "what", "a", "an", "and", "or", "but", "in", "on", "at", "to", "for", "of", "with", "by", "as", "this", "that", "it", "are", "was", "were", "be", "been", "being", "have", "has", "had", "do", "does", "did", "will", "would", "could", "should", "may", "might", "can", "shall", "i", "you", "he", "she", "we", "they", "me", "him", "her", "us", "them", "my", "your", "his", "its", "our", "their", "mine", "yours", "hers", "ours", "theirs"}

def extract_text_from_pdf(pdf_file):
    """
    Extract all textual content and page count from the PDF using pdfplumber.
    Returns (full_text, total_pages).
    """
    text = ""
    total_pages = 0
    # Reset file pointer before reading
    pdf_file.seek(0)
    with pdfplumber.open(pdf_file) as pdf:
        total_pages = len(pdf.pages)
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text, total_pages

def chunk_text(text):
    """
    Split the document text into chunks (paragraphs).
    Returns a list of non-empty chunks.
    """
    chunks = re.split(r'\n\s*\n', text)
    chunks = [chunk.strip() for chunk in chunks if chunk.strip()]
    return chunks

def extract_keywords(query):
    """
    Tokenize query and remove stopwords to get search keywords.
    Returns a set of lowercase keywords.
    """
    tokens = re.findall(r'\b\w+\b', query.lower())
    stop_words = set(stopwords.words('english')) if USE_NLTK else BASIC_STOPWORDS
    return set(token for token in tokens if token not in stop_words)

def score_chunks(chunks, keywords):
    """
    Score each chunk by how many query keywords it contains.
    Returns a list of (score, chunk_index, chunk_text).
    """
    scored = []
    for idx, chunk in enumerate(chunks):
        chunk_lower = chunk.lower()
        score = sum(1 for kw in keywords if kw in chunk_lower)
        scored.append((score, idx, chunk))
    return scored

def get_top_chunks(scored_chunks, top_n=3):
    """Return the top N highest-scoring chunks."""
    return sorted(scored_chunks, key=lambda x: (-x[0], x[1]))[:top_n]


def extract_answer(top_chunk, keywords):
    """
    From the best chunk, find the single most relevant 
    sentence as the direct answer.
    """
    sentences = top_chunk.split('. ')
    best_sentence = max(sentences, key=lambda s: sum(1 for kw in keywords if kw in s.lower()))
    return best_sentence

def main():
    st.title("Document Question Answering System")
    st.markdown("Upload a PDF and ask questions based on its content using keyword search.")

    # --- Initialize session state ---
    if "chunks" not in st.session_state:
        st.session_state.chunks = []
    if "total_pages" not in st.session_state:
        st.session_state.total_pages = 0
    if "pdf_name" not in st.session_state:
        st.session_state.pdf_name = None

    # --- File uploader ---
    uploaded_file = st.file_uploader("Upload a PDF file", type="pdf")

    if uploaded_file is not None:
        # Only re-extract if a new file is uploaded
        if uploaded_file.name != st.session_state.pdf_name:
            with st.spinner("Extracting text from PDF..."):
                text, total_pages = extract_text_from_pdf(uploaded_file)

            if not text.strip():
                st.error("No text could be extracted from the PDF.")
                return

            # Cache everything in session state
            st.session_state.chunks = chunk_text(text)
            st.session_state.total_pages = total_pages
            st.session_state.pdf_name = uploaded_file.name
            st.success(f"PDF loaded: {uploaded_file.name}")

        # --- Sidebar stats ---
        st.sidebar.header("Document Stats")
        st.sidebar.info(f"📄 Total Pages: {st.session_state.total_pages}")
        st.sidebar.info(f"🧩 Total Chunks: {len(st.session_state.chunks)}")

        # --- Query input ---
        query = st.text_input("Enter your question:")

        if st.button("Search"):
            if not query.strip():
                st.warning("Please enter a question.")
                return

            keywords = extract_keywords(query)
            if not keywords:
                st.warning("No keywords found after removing stopwords. Try more specific words.")
                return

            scored = score_chunks(st.session_state.chunks, keywords)
            top_chunks = get_top_chunks(scored, top_n=3)

            st.subheader("Search Results")
            if top_chunks and top_chunks[0][0] > 0:
                for score, idx, chunk in top_chunks:
                    with st.expander(f"Chunk {idx + 1}  |  Keyword Matches: {score}"):
                        st.markdown(chunk)
                        if score > 0:
                            answer = extract_answer(chunk, keywords)
                            st.markdown(f"**Most Relevant Sentence:** {answer}")
            else:
                st.info("No relevant excerpts found. Try different keywords.")

if __name__ == "__main__":
    main()  