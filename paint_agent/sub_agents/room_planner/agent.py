import os
from dotenv import load_dotenv
from google.adk.agents import Agent
from google.adk.models import Gemini
from google.genai import types
from .sub_agents.coverage_calculator.agent import coverage_calculator_agent

load_dotenv()

RETRY_OPTIONS = types.HttpRetryOptions(initial_delay=1, max_delay=3, attempts=30)
# img_path_1 = f"https://storage.cloud.google.com/{os.getenv("RESOURCES_BUCKET")}/project_paint.png"
# img_path_2 = f"https://storage.cloud.google.com/{os.getenv("RESOURCES_BUCKET")}/surecoverage.png"
# img_path_3 = f"https://storage.cloud.google.com/{os.getenv("RESOURCES_BUCKET")}/ecogreens.png"
# img_path_4 = f"https://storage.cloud.google.com/{os.getenv("RESOURCES_BUCKET")}/forever_paint.png"
assets_path = os.getenv("ASSETS_PATH")
img_path_1 = f"{assets_path}/project_paint.png"
img_path_2 = f"{assets_path}/surecoverage.png"
img_path_3 = f"{assets_path}/ecogreens.png"
img_path_4 = f"{assets_path}/forever_paint.png"

room_planner_agent = Agent(
    name="room_planner_agent",
    model=Gemini(model=os.getenv("MODEL"), retry_options=RETRY_OPTIONS),
    description="""
        after paint product is selected, determine how many rooms and
        present color options.""",
    instruction=f"""
    - Find out how many rooms the user would like to paint and what we should call each room.
    - Based on the {{SELECTED_PAINT?}}, show the corresponding images
      in an img tag with a height attribute of 300px:
        - Project Paint: {img_path_1}
        - SureCoverage: {img_path_2}
        - EcoGreen: {img_path_3}
        - Forever Paint: {img_path_4}
    - If the user has NOT selected a paint yet, show all available paint options with images 
      so they can compare.
    - Have them pick a color for each room. 
    - To calculate the paint needed for each room, transfer to the 'coverage_calculator_agent'
    """,
    sub_agents=[coverage_calculator_agent],
)
