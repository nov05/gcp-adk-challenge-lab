# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from dotenv import load_dotenv
import google.auth
from google.adk.agents import Agent
from google.adk.tools import AgentTool
from google.adk.models import Gemini
from google.genai import types
import google.cloud.logging
import os

from .callback_logging import log_query_to_model, log_model_response

from .sub_agents.room_planner.agent import room_planner_agent
from .sub_agents.search_agent.agent import search_agent

from .tools import set_session_value


# Load env
load_dotenv()

assets_path = os.getenv("ASSETS_PATH")
img_path_1 = f"{assets_path}/project_paint.png"
img_path_2 = f"{assets_path}/surecoverage.png"
img_path_3 = f"{assets_path}/ecogreens.png"
img_path_4 = f"{assets_path}/forever_paint.png"

RETRY_OPTIONS = types.HttpRetryOptions(initial_delay=1, max_delay=3, attempts=30)

# Configure logging to the Cloud
cloud_logging_client = google.cloud.logging.Client()
cloud_logging_client.setup_logging()

root_agent = Agent(
    name="product_selector",
    model=Gemini(model=os.getenv("MODEL"), retry_options=RETRY_OPTIONS),
    instruction="""
    You represent the paint department of Cymbal Shops.

    Information about Cymbal Shops paint, including prices, is available to you
    through the 'search_agent' tool.

    - At the start of a conversation, let the user know you're here to
      help them find the right paint for their project. Ask them if they'd
      like to learn more about the different paint products offered by
      Cymbal Shops.
    - If the user say yes, include information about all paint products including
      coverage rate and price.
    - If price and coverage rate aren't returned for some products, look them
      up individually.
    - If the user wants to see a picture of a paint, show the corresponding images
      in an img tag with a height attribute of 300px:
        - Project Paint: {img_path_1}
        - SureCoverage: {img_path_2}
        - EcoGreen: {img_path_3}
        - Forever Paint: {img_path_4}
    - After they have selected a paint product, use your 'set_session_value' tool
      to store their selection in the session dictionary with the key
      'SELECTED_PAINT', its coverage rate in 'COVERAGE_RATE', and its price
      per 2.5L container in 'PRICE'.
    - Transfer to the 'room_planner_agent'
    """,
    before_model_callback=log_query_to_model,
    after_model_callback=log_model_response,
    sub_agents=[room_planner_agent],
    tools=[
        set_session_value,
        AgentTool(search_agent, skip_summarization=False),
    ],
)
