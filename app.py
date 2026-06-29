import os
import json
from datetime import datetime
import streamlit as st
from src.rag_chain import answer_question
from src.pipeline import run_ingestion_pipeline

st.set_page_config(
    page_title="Biomedical RAG Assistant",
    page_icon="🩺",
    layout="wide"
)
st.title("🩺 Biomedical Research Assistant")
st.caption(
    "Ask questions grounded only in the uploaded biomedical literature."
)

if "messages" not in st.session_state:
    st.session_state.messages = []
if "feedback" not in st.session_state:
    st.session_state.feedback = {}

with st.sidebar:
    st.header("📚 Corpus")
    st.markdown(
        """This assistant answers questions **only** using the biomedical papers available in the local knowledge base.
Features:

- Semantic Search (RAG)
- Grounded Responses
- Citations
- Confidence Estimation
- Retrieved Evidence
- Trace Logging
"""
    )

    st.divider()
    st.subheader("📄 Upload New PDF")
    uploaded_pdf = st.file_uploader(
        "Upload biomedical paper",
        type=["pdf"]
    )
    if uploaded_pdf is not None:
        save_path = os.path.join(
            "data",
            "papers",
            uploaded_pdf.name
        )
        with open(save_path, "wb") as f:
            f.write(uploaded_pdf.getbuffer())
        with st.spinner("Updating knowledge base..."):
            try:
                run_ingestion_pipeline()
                st.success(
                    "Document uploaded successfully.\n\n"
                    "The knowledge base has been updated."
                )
            except Exception as e:
                st.error(str(e))

    st.divider()
    st.info("Every answer includes retrieved evidence and a trace ID for debugging.")

def confidence_badge(confidence):
    confidence = confidence.lower()
    if confidence == "high":
        st.success("🟢 High Confidence")
        st.caption(
            "The answer is well supported by the retrieved literature."
        )
    elif confidence == "medium":
        st.warning("🟡 Medium Confidence")
        st.caption(
            "The answer is only partially supported by the retrieved literature."
        )
    else:
        st.error("🔴 Low Confidence")
        st.caption(
            "The answer could not be fully verified from the available literature."
        )

def save_feedback(trace_id, feedback):
    os.makedirs("feedback", exist_ok=True)
    file_path = "feedback/feedback.json"
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            data = json.load(f)
    else:
        data = []
    data.append(
        {
            "trace_id": trace_id,
            "feedback": feedback,
            "timestamp": str(datetime.now())
        }
    )

    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)


def render_citations(citations):
    if len(citations) == 0:
        st.info("No citations available.")
        return

    for citation in citations:
        title = citation.get("title", "Unknown Document")
        page = citation.get("page_number", "-")
        st.markdown(
            f"📄 **{title}** &nbsp;&nbsp; *(Page {page})*"
        )


def render_chunks(chunks):
    if len(chunks) == 0:
        st.info("No retrieved chunks.")
        return
    for i, chunk in enumerate(chunks, start=1):

        similarity_distance = chunk["distance"]

        title = chunk["metadata"].get(
            "title",
            chunk["metadata"]["document_title"]
        )

        with st.expander(
            f"Retrieved Chunk {i} "
            f"(Distance: {similarity_distance:.2f})"
        ):

            st.markdown(f"**Document:** {title}")

            st.markdown(
                f"**Page:** {chunk['metadata']['page_number']}"
            )

            st.markdown("---")

            st.write(chunk["text"])

# -------------------------------------------------------
# Chat History
# -------------------------------------------------------

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        if message["role"] == "user":

            st.markdown(message["content"])

        else:

            response = message["content"]

            st.markdown("### Answer")
            st.write(response["answer"])

            st.markdown("### Confidence")
            confidence_badge(response["confidence"])

            st.markdown("### Citations")
            render_citations(response.get("citations", []))

            st.markdown("### Retrieved Evidence")
            render_chunks(response.get("retrieved_chunks", []))

            if "trace_id" in response:

                st.markdown("### Trace ID")
                st.code(response["trace_id"])

                col1, col2 = st.columns(2)

                with col1:

                    if st.button(
                        "👍 Helpful",
                        key=f"up_{response['trace_id']}"
                    ):
                        save_feedback(
                            response["trace_id"],
                            "up"
                        )
                        st.success("Thanks for your feedback!")

                with col2:

                    if st.button(
                        "👎 Not Helpful",
                        key=f"down_{response['trace_id']}"
                    ):
                        save_feedback(
                            response["trace_id"],
                            "down"
                        )
                        st.success("Thanks for your feedback!")


# -------------------------------------------------------
# User Input
# -------------------------------------------------------

question = st.chat_input(
    "Ask a biomedical question..."
)

if question:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question
        }
    )

    with st.chat_message("user"):

        st.markdown(question)

    with st.chat_message("assistant"):

        with st.spinner("Searching literature..."):

            response = answer_question(question)

        # ----------------------------
        # Guardrail / Error Response
        # ----------------------------

        if isinstance(response, str):

            st.error(response)

            assistant_response = {
                "answer": response,
                "confidence": "low",
                "citations": [],
                "retrieved_chunks": [],
                "trace_id": None
            }

        else:

            assistant_response = response

            st.markdown("### Answer")
            st.write(response["answer"])

            st.markdown("### Confidence")
            confidence_badge(response["confidence"])

            st.markdown("### Citations")
            render_citations(
                response.get("citations", [])
            )

            st.markdown("### Retrieved Evidence")
            render_chunks(
                response.get("retrieved_chunks", [])
            )

            if "trace_id" in response:

                st.markdown("### Trace ID")

                st.code(response["trace_id"])

                col1, col2 = st.columns(2)

                with col1:

                    if st.button(
                        "👍 Helpful",
                        key=f"new_up_{response['trace_id']}"
                    ):

                        save_feedback(
                            response["trace_id"],
                            "up"
                        )

                        st.success(
                            "Thanks for your feedback!"
                        )

                with col2:

                    if st.button(
                        "👎 Not Helpful",
                        key=f"new_down_{response['trace_id']}"
                    ):

                        save_feedback(
                            response["trace_id"],
                            "down"
                        )

                        st.success(
                            "Thanks for your feedback!"
                        )

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": assistant_response
        }
    )