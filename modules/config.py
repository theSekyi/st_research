import json
import os
import streamlit as st

def load_config():
    """Load configuration from JSON file or use defaults"""
    config_path = "papers_config.json"
    
    default_config = {
        "papers": [
            {
                "id": 1,
                "title": "Attention Is All You Need",
                "pdf_url": "https://arxiv.org/pdf/1706.03762.pdf",
                "local_pdf": None
            },
            {
                "id": 2,
                "title": "Highly accurate protein structure prediction with AlphaFold",
                "pdf_url": "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8372483/pdf/41586_2021_3819_merged_1626279313.pdf",
                "local_pdf": None
            },
            {
                "id": 3,
                "title": "BERT: A Review of Applications in Biomedical Information Extraction",
                "pdf_url": "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7356345/pdf/bioengineering-07-00057.pdf",
                "local_pdf": None
            }
        ],
        "question_templates": {
            "understanding": [
                {
                    "text": "What is the main research question or problem addressed in this paper?",
                    "type": "text"
                },
                {
                    "text": "What is the primary hypothesis or thesis statement?",
                    "type": "text"
                },
                {
                    "text": "What are the key objectives of this research?",
                    "type": "text"
                }
            ],
            "methodology": [
                {
                    "text": "What research methodology was employed?",
                    "type": "multiple_choice",
                    "options": ["Experimental", "Theoretical", "Computational", "Mixed Methods", "Other"]
                },
                {
                    "text": "Describe the experimental setup or study design in detail.",
                    "type": "text"
                }
            ],
            "results": [
                {
                    "text": "What are the three most significant findings?",
                    "type": "text"
                },
                {
                    "text": "Were there any unexpected results?",
                    "type": "multiple_choice",
                    "options": ["Yes", "No", "Somewhat"]
                }
            ],
            "analysis": [
                { "text": "What are the main limitations?", "type": "text" },
                {
                    "text": "How robust are the conclusions?",
                    "type": "multiple_choice",
                    "options": ["Very Robust", "Robust", "Moderate", "Weak", "Very Weak"]
                }
            ],
            "impact": [
                { "text": "What are the practical applications?", "type": "text" },
                {
                    "text": "Rate the overall quality",
                    "type": "rating",
                    "min": 1,
                    "max": 5
                }
            ]
        }
    }
    
    try:
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                return json.load(f)
    except Exception as e:
        st.warning(f"Using default configuration. Create 'papers_config.json' to customize.")
    
    return default_config

def get_questions_for_paper(paper_id, question_templates):
    """Compile all questions with proper IDs and metadata"""
    questions = []
    q_id = 0
    
    for category, category_questions in question_templates.items():
        for question in category_questions:
            questions.append({
                "id": q_id,
                "category": category,
                "text": question["text"],
                "type": question["type"],
                "options": question.get("options", []),
                "min": question.get("min", 1),
                "max": question.get("max", 5)
            })
            q_id += 1
    
    return questions