from main import Orchestrator
from langchain.llms import Ollama, Gemini
from langchain.agents import AgentType, initialize_agent
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
from AgentPrompts import Business_Agent_Template, Engineer_Agent_Template

def test_basic_conversation():
    print("Initializing test environment...")
    
    # Initialize components
    try:
        ollama_llm = Ollama(model="deepseek-coder")
        gemini_llm = Gemini(model_name="gemini-pro")
        memory = ConversationBufferMemory()
        
        # Initialize agents
        business_agent = initialize_agent(
            [], gemini_llm,
            agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
            verbose=True,
            memory=memory,
            prompt=PromptTemplate.from_template(Business_Agent_Template)
        )
        
        engineer_agent = initialize_agent(
            [], ollama_llm,
            agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
            verbose=True,
            memory=memory,
            prompt=PromptTemplate.from_template(Engineer_Agent_Template)
        )
        
        # Initialize orchestrator
        orchestrator = Orchestrator(business_agent, engineer_agent, memory)
        
        # Test cases
        test_inputs = [
            "@businessAgent What would be a good approach to develop a new e-commerce platform?",
            "@engineerAgent What technical stack would you recommend for this e-commerce platform?",
            "@debate Should we use microservices or monolithic architecture?"
        ]
        
        print("\nRunning test conversations...")
        for test_input in test_inputs:
            print(f"\nTest input: {test_input}")
            if test_input.startswith("@debate"):
                orchestrator.initiate_debate(test_input.replace("@debate", "").strip())
            else:
                orchestrator.handle_user_input(test_input)
            
        print("\nTest completed successfully!")
        
    except Exception as e:
        print(f"Test failed with error: {str(e)}")

if __name__ == "__main__":
    test_basic_conversation()
