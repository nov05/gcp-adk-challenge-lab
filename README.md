# 🟢 Google Skills Lab - **Deploy an Agent with Agent Development Kit (ADK): Challenge Lab**     

* Lab - https://www.skills.google/paths/3273/course_templates/1445/labs/619098
* Notes - https://docs.google.com/document/d/1zKgpvbAlrJetEszvkCvFR6_xovwx1MckBqaLIhis2T8

👉 Demo
<img src="https://raw.githubusercontent.com/nov05/pictures/refs/heads/master/gcp-adk-challenge-lab/20260409_demo.gif">  

* This demo showcases a multi-agent AI application built using Google Cloud’s Agent Development Kit (ADK) and deployed on Agent Engine.
* The “Paint Agent” helps users plan home painting projects by:
    - Recommending paint products based on product data
    - Displaying visual options to support decision-making
    - **Guiding users** through selecting colors for each room
    - **Calculating required paint coverage** from room dimensions
    - Estimating total cost based on selected products
* The system uses a modular multi-agent architecture:
    - A root agent manages user interaction and product selection
    - A search agent **retrieves paint information from [a product datasheet PDF](https://github.com/nov05/pictures/blob/master/gcp-adk-challenge-lab/assets/Cymbal_Shops_Paint_Datasheets.pdf)** using Vertex AI Search
    - A room planner agent handles room dimentions from user inputs
    - A coverage calculator agent computes paint requirements
* The agent also leverages session state to persist user selections across steps, enabling a smooth, conversational workflow from product discovery to final cost estimation.
* This demo is deployed via Agent Engine and accessed through a Chainlit web interface.

<br><br>   

---

<img src=https://raw.githubusercontent.com/nov05/pictures/refs/heads/master/gcp-adk-challenge-lab/company_logo.jpg width=300>   

* Cymbal Shops is an American retail chain headquartered in Minneapolis that sells housewares, electronics, and clothing.
* Cymbal Shops has expanded into Europe and launched a new Paint Department. It plans to use its new online presence to streamline the way people shop for paint for DIY home renovation projects.

We need to develop an agent, Paint Agent, to help the user:
- select a paint product based on Cymbal Shops' paint product datasheets
- choose a color from the selected product line
- determine how much paint is needed by room dimensions
- calculate the price based on the selected options

### 👉 **Agent atlas:**  

<img src="https://raw.githubusercontent.com/nov05/pictures/refs/heads/master/gcp-adk-challenge-lab/agent_atlas.jpg" width=600>    

```bash
root_agent
├─ tools:
│   ├─ AgentTool(search_agent)  # handles all search queries
│   └─ set_session_value
└─ sub_agents:
    └─ room_planner_agent
         └─ sub_agents:
             └─ coverage_calculator
```

The agent atlas in the ADK Dev UI:  
<img src="https://raw.githubusercontent.com/nov05/pictures/refs/heads/master/gcp-adk-challenge-lab/2026-04-09%2018_33_17-local%20testing%20in%20ADK%20web%20UI.jpg" width=800>    

<img src="https://raw.githubusercontent.com/nov05/pictures/refs/heads/master/gcp-adk-challenge-lab/2026-04-09%2018_34_10-agent%20atlas.jpg" width=800>  

### 👉 Test content:  

```text
Hello!
```
```text
Yes.
```
```text
I'd like to use Forever Paint
```
```text
Two rooms. The living room and a baby's room.
```
```text
"Sunlight through a canvas tent" for the baby's room and "Coffee Cream" for the living room.
```
```text
The living room is 5m by 4m. 2.5m high. 1 door, 3 windows.
```
```text
Two coats.
```
```text
The baby's room is 3m by 3m. 2.5m high. 1 door, 1 window.
```
```text
What would be the total cost for painting two rooms?   
```
```text
Thanks! Bye!
```

<br><br>   

---   

## 👉 Logs:
2026-04-09 repo created
