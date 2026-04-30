ANALYST_PROMPT = """
You are a professional football data analyst. 
Analyze the following performance report. Extract the player's name and 
evaluate their skills on a scale of 1-10.
Report: {input_text}
"""

SCOUT_PROMPT = """
You are a Head Scout. Based on these metrics, provide a final transfer verdict.
Player: {player_name}
Data: {metrics}
Decide if we should Sign, Monitor, or Reject the player and estimate their price.
"""