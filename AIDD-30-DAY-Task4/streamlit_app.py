
import streamlit as st
from agent import PDFProcessorAgent
import json

# --- Page Configuration ---
st.set_page_config(
    page_title="PDF Summarizer & Quiz Generator",
    page_icon="📚",
    layout="wide",
)

# --- CSS for Styling ---
st.markdown("""
<style>
    .main {
        background-color: #f0f2f6;
    }
    .stApp {
        background-color: #f0f2f6;
    }
    .st-emotion-cache-1y4p8pa {
        max-width: 90%;
    }
    h1, h2, h3 {
        color: #31333f;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border-radius: 8px;
        border: none;
        padding: 10px 24px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        margin: 4px 2px;
        cursor: pointer;
        transition-duration: 0.4s;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
</style>
""", unsafe_allow_html=True)


# --- Application State Management ---
if 'processing_complete' not in st.session_state:
    st.session_state.processing_complete = False
if 'summary_data' not in st.session_state:
    st.session_state.summary_data = None
if 'quiz_data' not in st.session_state:
    st.session_state.quiz_data = None
if 'error_message' not in st.session_state:
    st.session_state.error_message = None


# --- UI Layout ---
st.title("📚 PDF Summarizer & Quiz Generator")
st.markdown("Upload a PDF to get a concise summary, key points, and a generated quiz.")

with st.sidebar:
    st.header("Configuration")
    api_key = st.text_input("Enter your Google Gemini API Key", type="password", key="api_key_input")
    uploaded_file = st.file_uploader("Upload your PDF document", type=["pdf"], key="pdf_uploader")
    
    process_button = st.button("Generate Insights ✨", key="process_button")

# --- Main Logic ---
if process_button:
    # Reset state
    st.session_state.processing_complete = False
    st.session_state.summary_data = None
    st.session_state.quiz_data = None
    st.session_state.error_message = None

    if not api_key:
        st.session_state.error_message = "Please enter your Google Gemini API key in the sidebar."
    elif not uploaded_file:
        st.session_state.error_message = "Please upload a PDF file."
    else:
        try:
            with st.spinner("Processing your PDF... This may take a moment. ⏳"):
                # Initialize agent
                agent = PDFProcessorAgent(api_key=api_key)
                
                # Extract text
                st.write("Step 1: Extracting text from the PDF...")
                pdf_text = agent.extract_text_from_pdf(uploaded_file)
                
                if not pdf_text:
                    st.session_state.error_message = "Could not extract text from the PDF. The file might be empty or corrupted."
                else:
                    # Generate summary
                    st.write("Step 2: Generating summary and study points...")
                    summary_results = agent.generate_summary(pdf_text)
                    st.session_state.summary_data = summary_results
                    
                    # Generate quiz
                    st.write("Step 3: Generating quiz...")
                    quiz_results = agent.generate_quiz(pdf_text)
                    st.session_state.quiz_data = quiz_results
                    
                    st.session_state.processing_complete = True
            
        except Exception as e:
            st.session_state.error_message = f"An unexpected error occurred: {str(e)}"

# --- Display Results or Errors ---
if st.session_state.error_message:
    st.error(st.session_state.error_message)

if st.session_state.processing_complete:
    st.success("Processing complete! Here are your results:")
    
    # --- Summary and Key Points Display ---
    if st.session_state.summary_data:
        st.header("📝 Summary & Study Points")
        summary_info = st.session_state.summary_data
        
        with st.expander("📄 Summary", expanded=True):
            st.write(summary_info.get("summary", "No summary available."))
            
        with st.expander("🔑 Key Points", expanded=True):
            key_points = summary_info.get("key_points", [])
            if key_points:
                for i, point in enumerate(key_points, 1):
                    st.markdown(f"- {point}")
            else:
                st.write("No key points were generated.")

        with st.expander("🤔 Study Questions", expanded=True):
            study_questions = summary_info.get("study_questions", [])
            if study_questions:
                for i, question in enumerate(study_questions, 1):
                    st.markdown(f"{i}. {question}")
            else:
                st.write("No study questions were generated.")

    # --- Quiz Display ---
    if st.session_state.quiz_data:
        st.header("🧠 Generated Quiz")
        quiz_info = st.session_state.quiz_data

        if "error" in quiz_info:
            st.error(f"Quiz Generation Failed: {quiz_info['error']}")
            if "raw_response" in quiz_info:
                st.code(quiz_info["raw_response"], language="text")
        else:
            # Display Multiple Choice Questions
            st.subheader("Multiple Choice Questions")
            mcqs = quiz_info.get("multiple_choice_questions", [])
            if mcqs:
                for i, mcq in enumerate(mcqs, 1):
                    st.markdown(f"**{i}. {mcq['question']}**")
                    # Use a form to manage state for each question's radio buttons
                    with st.form(key=f"mcq_form_{i}"):
                        options = mcq.get("options", {})
                        user_answer = st.radio("Choose your answer:", list(options.values()), key=f"mcq_{i}")
                        
                        submitted = st.form_submit_button("Check Answer")
                        if submitted:
                            correct_option_key = mcq.get("correct_answer")
                            correct_answer_value = options.get(correct_option_key)
                            if user_answer == correct_answer_value:
                                st.success(f"Correct! The answer is {correct_answer_value}")
                            else:
                                st.error(f"Incorrect. The correct answer is {correct_answer_value}")
            else:
                st.write("No multiple-choice questions were generated.")

            # Display Short Answer Questions
            st.subheader("Short Answer Questions")
            short_questions = quiz_info.get("short_answer_questions", [])
            if short_questions:
                for i, sq in enumerate(short_questions, 1):
                    st.markdown(f"**{i}. {sq['question']}**")
                    st.text_area("Your answer:", key=f"saq_{i}", height=100)
            else:
                st.write("No short-answer questions were generated.")

            # Display the raw JSON for verification
            with st.expander("View Raw Quiz JSON"):
                st.json(quiz_info)
else:
    st.info("Please provide your API key, upload a PDF, and click 'Generate Insights' to begin.")
