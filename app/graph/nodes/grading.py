from langchain_core.prompts import ChatPromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field
from app.services.llm_service import get_llm
from app.graph.state import GraphState
from app.utils.logger import logger

class DocGrade(BaseModel):
    binary_score: str = Field(description="Is the document relevant to the user question? 'yes' or 'no'")

def grading_node(state: GraphState) -> GraphState:
    logger.info("--- NODE: DOCUMENT GRADING ---")
    documents = state["documents"]
    question = state["question"]
    llm = get_llm()
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a grader assessing relevance of a retrieved document to a user question. "
                   "If the document contains keyword(s) or semantic meaning related to the user question, grade it as relevant. "
                   "Give a binary score 'yes' or 'no' score to indicate whether the document is relevant to the question."),
        ("human", "Question: {question}\n\nDocument: {document_content}")
    ])
    
    grader_chain = prompt | llm.with_structured_output(DocGrade)
    
    filtered_docs = []
    relevance_scores = []
    
    for doc in documents:
        result = grader_chain.invoke({"question": question, "document_content": doc.page_content})
        score = result.binary_score
        
        if score == "yes":
            logger.info("  Grade: DOCUMENT RELEVANT")
            filtered_docs.append(doc)
            relevance_scores.append("relevant")
        else:
            logger.info("  Grade: DOCUMENT IRRELEVANT")
            relevance_scores.append("irrelevant")
            
    return {
        **state,
        "documents": filtered_docs,
        "relevance_scores": relevance_scores
    }
