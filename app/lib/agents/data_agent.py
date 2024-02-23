def create_data_analysis_agent(llm, tools):
    system_prompt = "Analyze the provided dataset and summarize key insights."
    # Define the prompt template for data analysis tasks
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        MessagesPlaceholder(variable_name="messages"),
    ])
    # Create the agent
    agent = create_openai_functions_agent(llm, tools, prompt)
    executor = AgentExecutor(agent=agent, tools=tools)
    return executor
    
def create_content_creation_agent(llm, tools):
    system_prompt = "Create a detailed report/article based on the provided insights."
    # Define the prompt template for content creation tasks
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        MessagesPlaceholder(variable_name="messages"),
    ])
    # Create the agent
    agent = create_openai_functions_agent(llm, tools, prompt)
    executor = AgentExecutor(agent=agent, tools=tools)
    return executor
    
def create_automation_agent(llm, tools):
    system_prompt = "Automate the identified routine task based on the criteria provided."
    # Define the prompt template for automation tasks
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        MessagesPlaceholder(variable_name="messages"),
    ])
    # Create the agent
    agent = create_openai_functions_agent(llm, tools, prompt)
    executor = AgentExecutor(agent=agent, tools=tools)
    return executor
    
def create_quality_assurance_agent(llm, tools):
    system_prompt = "Review the output for accuracy, quality, and adherence to guidelines."
    # Define the prompt template for quality assurance tasks
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        MessagesPlaceholder(variable_name="messages"),
    ])
    # Create the agent
    agent = create_openai_functions_agent(llm, tools, prompt)
    executor = AgentExecutor(agent=agent, tools=tools)
    return executor
    
def create_communication_agent(llm, tools):
    system_prompt = "Summarize the discussions and facilitate communication between agents."
    # Define the prompt template for communication tasks
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        MessagesPlaceholder(variable_name="messages"),
    ])
    # Create the agent
    agent = create_openai_functions_agent(llm, tools, prompt)
    executor = AgentExecutor(agent=agent, tools=tools)
    return executor