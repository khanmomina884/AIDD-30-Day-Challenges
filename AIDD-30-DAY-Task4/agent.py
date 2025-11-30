
import os
import json
import google.generativeai as genai
from PyPDF2 import PdfReader

class PDFProcessorAgent:
    """
    An agent that processes PDF files to generate summaries and quizzes.
    """

    def __init__(self, api_key: str):
        """
        Initializes the agent with a Google Gemini API key.

        Args:
            api_key (str): The Google Gemini API key.
        
        Raises:
            ValueError: If the API key is not provided.
        """
        if not api_key:
            raise ValueError("API key for Google Gemini is required.")
        
        # Configure the generative AI model
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')

    def extract_text_from_pdf(self, pdf_file) -> str:
        """
        Extracts text from an uploaded PDF file.

        Args:
            pdf_file: A file-like object representing the PDF.

        Returns:
            str: The extracted text from the PDF.
        """
        try:
            pdf_reader = PdfReader(pdf_file)
            text = ""
            for page in pdf_reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text
            return text
        except Exception as e:
            print(f"Error extracting text from PDF: {e}")
            return ""

    def generate_summary(self, text: str) -> dict:
        """
        Generates a summary from the provided text using the Gemini model.

        Args:
            text (str): The text to be summarized.

        Returns:
            dict: A dictionary containing the summary, key points, and study questions.
        """
        if not text:
            return {
                "summary": "Could not generate summary because no text was provided.",
                "key_points": [],
                "study_questions": [],
            }

        prompt = f"""
        Based on the following text, please provide:
        1. A concise summary of 5-7 lines.
        2. A list of the 5 most important key points.
        3. A list of 3 study questions that can be answered from the text.

        Text:
        ---
        {text}
        ---

        Please format the output clearly with distinct sections for the summary, key points, and study questions.
        """

        try:
            response = self.model.generate_content(prompt)
            # Simple parsing based on expected structure.
            # A more robust solution might use regex or more structured model output.
            content = response.text
            
            summary_part = content.split("Key Points:")[0].replace("Summary:", "").strip()
            key_points_part = content.split("Study Questions:")[0].split("Key Points:")[1].strip()
            study_questions_part = content.split("Study Questions:")[1].strip()

            key_points = [point.strip() for point in key_points_part.split('\n') if point.strip()]
            study_questions = [question.strip() for question in study_questions_part.split('\n') if question.strip()]

            return {
                "summary": summary_part,
                "key_points": key_points,
                "study_questions": study_questions,
            }
        except Exception as e:
            print(f"Error during summary generation: {e}")
            return {
                "summary": "Failed to generate summary due to an API error.",
                "key_points": [],
                "study_questions": [],
            }

    def generate_quiz(self, text: str) -> dict:
        """
        Generates a quiz from the provided text using the Gemini model.

        The output is requested in JSON format.

        Args:
            text (str): The text to generate the quiz from.

        Returns:
            dict: A dictionary containing MCQs and short-answer questions, parsed from JSON.
        """
        if not text:
            return {
                "multiple_choice_questions": [],
                "short_answer_questions": [],
            }

        prompt = f"""
        Based on the full text provided below, generate a quiz. The quiz should consist of:
        1.  5 multiple-choice questions (MCQs), each with four options (A, B, C, D) and a clear indication of the correct answer.
        2.  3 short-answer questions that require a brief explanation.

        The entire output must be in a single, clean JSON object. Do not include any text or formatting outside of the JSON.

        The JSON structure should be:
        {{
          "multiple_choice_questions": [
            {{
              "question": "...",
              "options": {{
                "A": "...",
                "B": "...",
                "C": "...",
                "D": "..."
              }},
              "correct_answer": "..."
            }}
          ],
          "short_answer_questions": [
            {{
              "question": "..."
            }}
          ]
        }}

        Text:
        ---
        {text}
        ---
        """

        try:
            response = self.model.generate_content(prompt)
            # Clean the response to ensure it's valid JSON
            cleaned_response = response.text.strip().replace("```json", "").replace("```", "").strip()
            
            # Find the start and end of the JSON object
            json_start = cleaned_response.find('{')
            json_end = cleaned_response.rfind('}') + 1
            
            if json_start == -1 or json_end == 0:
                raise json.JSONDecodeError("No JSON object found in the response.", cleaned_response, 0)
                
            json_string = cleaned_response[json_start:json_end]
            
            return json.loads(json_string)
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON from quiz generation response: {e}")
            print(f"Raw response was: {response.text}")
            return {
                "error": "Failed to parse quiz from the model's response.",
                "raw_response": response.text,
            }
        except Exception as e:
            print(f"Error during quiz generation: {e}")
            return {
                "error": "Failed to generate quiz due to an API error.",
            }
