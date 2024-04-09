import os
from crewai import Agent, Task, Crew
from crewai_tools import SerperDevTool
from event import all_upcoming_event
from about import about_user
from dotenv import load_dotenv
load_dotenv()

# Get to know about the user.

about_the_user = about_user()


all_upcoming_event = all_upcoming_event()

print("The upcoming events are: ", all_upcoming_event)


os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["SERPER_API_KEY"] = os.getenv("SERPER_API_KEY")


print(a, b)

# You can choose to use a local model through Ollama for example. See https://docs.crewai.com/how-to/LLM-Connections/ for more information.

# os.environ["OPENAI_API_BASE"] = 'http://localhost:11434/v1'
# os.environ["OPENAI_MODEL_NAME"] ='openhermes'  # Adjust based on available model
# os.environ["OPENAI_API_KEY"] ='sk-111111111111111111111111111111111111111111111111'

search_tool = SerperDevTool()

# Define your agents with roles and goals
researcher = Agent(
    role="Event manager",
    goal="Help manage events and meetings",
    backstory=f"""Agent may suggest breaking down a complex task into multiple sub-tasks (with rationale) and allow users to either modify or just confirm
Agent may cluster smaller tasks (e.g., call to pick up laundry) and suggest particular time(s) to complete relevant clusters of tasks (based on estimated effort required). Each cluster can be limited to about 1 to no more than 1.5 hours.
In case of upcoming appointments or meetings, Agent may ask questions to help the user prepare for the meeting and then also ask questions to debrief and capture tasks from the meeting. Later on this can be integrated with one of the existing note taking AIs to validate tasks captured by it.
Agent may check-in to see how the user is feeling and may also suggest quick stretch and breathing exercises in between based on the density of the schedule.
Agents may suggest some help or give tips if a user is frequently snoozing the task or it has not been marked complete for a long time.


The events are as follows: {all_upcoming_event}

Also note the user details: {about_the_user}
""",
    verbose=True,
    allow_delegation=False,
    tools=[search_tool],
    # You can pass an optional llm attribute specifying what mode you wanna use.
    # It can be a local model through Ollama / LM Studio or a remote
    # model like OpenAI, Mistral, Antrophic or others (https://docs.crewai.com/how-to/LLM-Connections/)
    #
    # import os
    # os.environ['OPENAI_MODEL_NAME'] = 'gpt-3.5-turbo'
    #
    # OR
    #
    # from langchain_openai import ChatOpenAI
    # llm=ChatOpenAI(model_name="gpt-3.5", temperature=0.7)
)
manager = Agent(
    role="Tech project manager",
    goal="Users can interact with the agent in a conversational manner to create tasks (they can be either high-level or specific). The agent may ask one (e.g., Would you like to add additional details?) or more follow-up questions to capture task details. When a user doesn’t specify additional details, the AI auto-assumes certain parameters based on details shared by the user + past experience + internal knowledge base (initially). ",
    backstory=f"""Users can interact with the agent in a conversational manner to create tasks (they can be either high-level or specific). The agent may ask one (e.g., Would you like to add additional details?) or more follow-up questions to capture task details. When a user doesn’t specify additional details, the AI auto-assumes certain parameters based on details shared by the user + past experience + internal knowledge base (initially).
    
    
    The events are as follows: {all_upcoming_event}

Also note the user details: {about_the_user}
    """,
    verbose=True,
    allow_delegation=True,
)

# Create tasks for your agents
task1 = Task(
    description="Agent may suggest breaking down a complex task into multiple sub-tasks (with rationale) and allow users to either modify or just confirm",
    expected_output="A detailed report on the task breakdown",
    agent=researcher,
)

task2 = Task(
    description="Agent may cluster smaller tasks (e.g., call to pick up laundry) and suggest particular time(s) to complete relevant clusters of tasks (based on estimated effort required). Each cluster can be limited to about 1 to no more than 1.5 hours.",
    expected_output="A detailed break down of the task reports.",
    agent=manager,
)

# Instantiate your crew with a sequential process
crew = Crew(
    agents=[researcher, manager],
    tasks=[task1, task2],
    verbose=2,  # You can set it to 1 or 2 to different logging levels
)

# Get your crew to work!
result = crew.kickoff()

print("######################")
print(result)
