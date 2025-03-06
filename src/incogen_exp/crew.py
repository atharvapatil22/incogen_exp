from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from pydantic import BaseModel,Field
from typing import List 
from crewai_tools import DallETool

dalle_tool = DallETool(model="dall-e-3",
                       size="1024x1024",
                       quality="standard",
                       n=1)

# Define a class for an individual scene
class StoryScene(BaseModel):
    scene_number: int 
    narration: str

# Define a class for a list of story scenes
class StoryScenes(BaseModel):
 story_name: str 
 summary: str 
 background: str 
 lesson: str 
 scenes: List[StoryScene]

# Define a class for an individual scene
class SceneImage(BaseModel):
    prompt: str = Field(description = "A prompt for text to image models that can be used to generate an image.", max_length = 50)
    image_url: str = Field(description = "Url to the image generated by the tool")

@CrewBase
class StoryCrew():
 """StoryCrew crew"""

 agents_config = 'config/story/agents.yaml'
 tasks_config = 'config/story/tasks.yaml'

#  @llm
#  def llm_model(self):
#   return ChatOpenAI(temperature=0.0,  # Set to 0 for deterministic output
#                     model="gpt-4o-mini",  # Using the GPT-4 Turbo model
#                     max_tokens=8000) 

 @agent
 def scriptwriter(self) -> Agent:
  return Agent(
   config=self.agents_config['scriptwriter'],
   output_pydantic = StoryScenes,   
   verbose=True
  )

 @task
 def scriptwriting(self) -> Task:
  return Task(
   config=self.tasks_config['scriptwriting'],
   output_pydantic = StoryScenes,   
  )

 @crew
 def crew(self) -> Crew:
  """Creates the StoryCrew crew"""
  script_crew =  Crew(
   agents=self.agents, # Automatically created by the @agent decorator
   tasks=self.tasks, # Automatically created by the @task decorator
   process=Process.sequential,
   verbose=True,
   # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
  )

  return script_crew
 
@CrewBase
class ArtistCrew():

 agents_config = 'config/visual/agents.yaml'
 tasks_config = 'config/visual/tasks.yaml'

#  @llm
#  def llm_model(self):
#   return ChatOpenAI(temperature=0.0,  # Set to 0 for deterministic output
#                     model="gpt-4o-2024-08-06",  # Using the GPT-4 Turbo model
#                     max_tokens=8000) 

 @agent
 def visualartist(self) -> Agent:
  return Agent(
   config=self.agents_config['visualartist'],
   
   tools=[dalle_tool],   
   verbose=True
  )

 @task
 def illustration(self) -> Task:
  return Task(
   config=self.tasks_config['illustration'],
   
#    output_pydantic = SceneImage,      
   output_file='report.md'
  )

 @crew
 def crew(self) -> Crew:
  """Create the picture book crew"""
  artist_crew =  Crew(
   agents=self.agents, # Automatically created by the @agent decorator
   tasks=self.tasks, # Automatically created by the @task decorator
   process=Process.sequential,
   verbose=True,
   # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
  ) 

  return artist_crew