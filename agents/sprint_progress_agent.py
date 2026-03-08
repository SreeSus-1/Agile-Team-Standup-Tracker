from agents.base_agent import BaseAgent

class SprintProgressEstimatorAgent(BaseAgent):
    def run(self, updates_text: str, sprint_name: str, standup_date: str) -> str:
        prompt = f"""
        You are a Sprint Progress Estimator Agent.

        Review the following standup updates for:
        Sprint: {sprint_name}
        Date: {standup_date}

        Estimate:
        - sprint health
        - whether the team is on track
        - likely risks to delivery
        - confidence level
        - short recommendation for the scrum master

        Team Updates:
        {updates_text[:4000]}
        """
        return self.call_ollama(prompt)