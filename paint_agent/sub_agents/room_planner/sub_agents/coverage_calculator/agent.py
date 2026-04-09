import os
from dotenv import load_dotenv
from google.adk.agents import Agent
from google.adk.models import Gemini
from google.genai import types
from .tools import paint_coverage_calculator
from .....callback_logging import log_query_to_model, log_model_response


load_dotenv()

RETRY_OPTIONS = types.HttpRetryOptions(initial_delay=1, max_delay=3, attempts=30)

coverage_calculator_agent = Agent(
    name="coverage_calculator_agent",
    model=Gemini(model=os.getenv("MODEL"), retry_options=RETRY_OPTIONS),
    instruction="""
    - Ask the user for the following for each room:
        - The room length and width
        - The room height (a typical ceiling height is 2,4-2,7M)
        - The number of doors and windows
    -  Use the 'paint_coverage_calculator' to estimate the amount of
       coverage they will need for each coat. Let them know that two
       coats are recommended and ask them to confirm the number of
       coats they'd like to paint. Store their result as 'coats'
       (default to 2 if they respond with something like 'yes'). 
    - Talk them through the following math for each room:
        - The square meters of paint they need multiplied by
          the number of coats
        - The coverage rate of the paint they have chosen is COVERAGE_RATE,
          so they will need X liters.
        - The paint is sold in 2,5L buckets, so rounding up they will
          need Y buckets.
        - The price is PRICE per bucket, so the total cost is:
          [provide total cost].
    - Express enthusiasm for their project and the color they chose.
      Let them know you are there if they need anything else.
    """,
    before_model_callback=log_query_to_model,
    after_model_callback=log_model_response,
    tools=[paint_coverage_calculator],
)
