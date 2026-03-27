import validators
import streamlit as st
from langchain_classic.prompts import PromptTemplate
from langchain_groq import ChatGroq
from langchain_classic.chains.summarize import load_summarize_chain
from langchain_classic.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import YoutubeLoader, UnstructuredURLLoader

###Streamlit App
st.set_page_config(page_title="Summify · Instant AI Summaries", page_icon="⚡")
st.title("⚡ Summify")
st.markdown("<h3>🎬 Paste a <span style='color: red;'>YouTube video</span> or <span style='color: #4a90e2;'>website URL</span> → Get key insights instantly.</h3>", unsafe_allow_html=True)

#Sidebar
with st.sidebar:
    groq_api_key = st.text_input("Groq API Key", value="", type="password")

urls = st.text_input("Entry URL",label_visibility="collapsed")

# ── LLM & Prompt
llm = ChatGroq(model="llama-3.1-8b-instant", groq_api_key=groq_api_key)

prompt_template = """
Provide a summary of the following content in 300 words:
Context: {text}
"""
prompt = PromptTemplate(template=prompt_template, input_variables=["text"])

# ── Summarize Button
if st.button("Summarize the Content from YT or Website"):
    if not groq_api_key.strip() or not urls.strip():
        st.error("Please provide the information to get started")
    elif not validators.url(urls):
        st.error("Please enter a valid URL. It can be a YouTube video URL or website URL")
    else:
        try:
            with st.spinner("Summarizing..."):

                # ── Load content ───────────────────────────────────────────────
                if "youtube.com" in urls:
                    loader = YoutubeLoader.from_youtube_url(
                        urls,
                        add_video_info=False,
                        language=["en"],
                    )
                else:
                    loader = UnstructuredURLLoader(
                        urls=[urls],
                        ssl_verify=False,
                        headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"}
                    )

                docs = loader.load()

                # ── Split into chunks to avoid token limit ─────────────────────
                splitter = RecursiveCharacterTextSplitter(
                    chunk_size=2000,
                    chunk_overlap=100
                )
                chunks = splitter.split_documents(docs)

                # ── Summarize using map_reduce ─────────────────────────────────
                chain = load_summarize_chain(
                    llm,
                    chain_type="map_reduce",
                    map_prompt=prompt,
                    combine_prompt=prompt
                )
                output_summary = chain.run(chunks)

                st.success(output_summary)
                st.snow()

        except Exception as e:
            st.exception(f"Exception: {e}")