from agents.base_agent import BaseAgent

class SummaryAgent(BaseAgent):
    def run(self, updates_text: str, sprint_name: str, standup_date: str) -> str:
        prompt = f"""
        You are a Summary Agent for an agile software team.

        Summarize the following daily standup updates for:
        Sprint: {sprint_name}
        Date: {standup_date}

        Focus on:
        - completed work
        - ongoing work
        - next steps
        - team-wide progress

        Team Updates:
        {updates_text[:4000]}
        """
        return self.call_ollama(prompt)