# main.py
from langchain.llms import Ollama, Gemini
#propmt template import
from prompt_templates import Business_Agent_Template, Engineer_Agent_Template
from langchain.agents import AgentType, initialize_agent, tool
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
from SummaryGenerator import generate_conversation_summary  # new import
from AdvancedMemory import save_memory  # new import

class Orchestrator:
    def __init__(self, business_agent, engineer_agent, memory):
        self.business_agent = business_agent
        self.engineer_agent = engineer_agent
        self.memory = memory

    def handle_user_input(self, user_input):
        # 1. Parse user input (determine target agent, etc.)
        target_agent, message = self.parse_user_input(user_input)

        # 2. Retrieve context from memory
        context = self.memory.load_memory_variables({})['history']

        # 3. Construct prompt (using agent's prompt template + context + message)
        if target_agent == "business":
            prompt = self.business_agent.agent.prompt.format(input=message, history=context)
            response = self.business_agent.run(prompt)
        elif target_agent == "engineer":
            prompt = self.engineer_agent.agent.prompt.format(input=message, history=context)
            response = self.engineer_agent.run(prompt)
        else:  # Default or error handling
            response = "I'm not sure how to respond to that."

        # 4. Update conversation memory
        self.memory.save_context({"input": user_input}, {"output": response})

        # Persist memory to file
        current_history = self.memory.load_memory_variables({})['history']
        save_memory(current_history)

        # 5. Generate Current Proposal Summary (function for this)
        summary = self.generate_summary()

        # 6. Print response and summary
        print(f"{target_agent.capitalize()} Agent: {response}")
        print("\n--- Current Proposal Summary ---")
        print(summary)
        print("-" * 30)

    def initiate_debate(self, topic):
        # Basic debate simulation: alternate one turn each between agents
        turns = 2  # one turn each
        responses = []
        message = topic
        for turn in range(turns):
            if turn % 2 == 0:
                prompt = self.business_agent.agent.prompt.format(input=message, history=self.memory.load_memory_variables({})['history'])
                response = self.business_agent.run(prompt)
                responses.append(response)
                message = response  # feed response to next agent
            else:
                prompt = self.engineer_agent.agent.prompt.format(input=message, history=self.memory.load_memory_variables({})['history'])
                response = self.engineer_agent.run(prompt)
                responses.append(response)
                message = response
        # Print debate responses
        print("\n--- Debate Transcript ---")
        for idx, resp in enumerate(responses, start=1):
            print(f"Turn {idx}: {resp}")
        print("-" * 30)

    def parse_user_input(self, user_input):
        # Basic parsing - can be improved with regex
        if user_input.startswith("@businessAgent"):
            return "business", user_input.replace("@businessAgent", "").strip()
        elif user_input.startswith("@engineerAgent"):
            return "engineer", user_input.replace("@engineerAgent", "").strip()
        else:
            return "business", user_input # Default to business agent

    def generate_summary(self):
        # Use external module to generate summary from conversation history
        history = self.memory.load_memory_variables({})['history']
        return generate_conversation_summary(history)

def main():
    # Initialize LLMs
    ollama_llm = Ollama(model="deepseek-coder") #Ensure deepseek-coder is installed and server is running
    gemini_llm = Gemini( model_name="gemini-pro") #Instal google gemini and configure

    # Initialize memory
    memory = ConversationBufferMemory()

    # Define tools (none for now, but this is where they would go)
    tools = []

    # Initialize agents
    business_agent = initialize_agent(
        tools, 
        gemini_llm, 
        agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION, 
        verbose=True, 
        memory=memory,
        prompt= PromptTemplate.from_template(Business_Agent_Template)
    )
    engineer_agent = initialize_agent(
        tools, 
        ollama_llm, 
        agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION, 
        verbose=True, 
        memory=memory,
        prompt = PromptTemplate.from_template(Engineer_Agent_Template)
    )
    # Initialize orchestrator
    orchestrator = Orchestrator(business_agent, engineer_agent, memory)

    # Welcome message
    print("Welcome to the Business Development Assistant!")
    print("You can address agents with @businessAgent, @engineerAgent or initiate a debate by typing '@debate <topic>'.")
    print("Type 'exit' to quit.")

    # Main loop
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            break
        if user_input.startswith("@debate"):
            topic = user_input.replace("@debate", "").strip()
            orchestrator.initiate_debate(topic)
        else:
            orchestrator.handle_user_input(user_input)

if __name__ == "__main__":
    main()