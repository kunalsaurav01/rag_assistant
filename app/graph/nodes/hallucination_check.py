from langchain_core.prompts import ChatPromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field
from app.services.llm_service import get_llm
from app.graph.state import GraphState
from app.utils.logger import logger

class HallucinationGrade(BaseModel):
    binary_score: str = Field(description="Is the generation grounded in the documents? 'yes' or 'no'")

def hallucination_check_node(state: GraphState) -> GraphState:
    logger.info("--- NODE: HALLUCINATION CHECK ---")
    documents = state["documents"]
    generation = state["generation"]
    llm = get_llm()
    
    context = "\n\n".join([doc.page_content for doc in documents])
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a grader assessing whether an LLM generation is grounded in / supported by a set of retrieved documents. "
                   "Give a binary score 'yes' or 'no'. 'yes' means the answer is grounded in the documents."),
        ("human", "Documents: {context}\n\nGeneration: {generation}")
    ])
    
    grader_chain = prompt | llm.with_structured_output(HallucinationGrade)
    result = grader_chain.invoke({"context": context, "generation": generation})
    
    return {
        **state,
        "is_hallucination": "no" if result.binary_score == "yes" else "yes"
    }
