from agents.base_agent import BaseAgent

class BlockerDetectorAgent(BaseAgent):
    def run(self, updates_text: str, sprint_name: str, standup_date: str) -> str:
        prompt = f"""
        You are a Blocker Detector Agent for an agile software team.

        Analyze the following standup updates for:
        Sprint: {sprint_name}
        Date: {standup_date}

        Identify:
        - blockers
        - delays
        - missing dependencies
        - risks
        - people who may need help

        Return a concise blocker report.

        Team Updates:
        {updates_text[:4000]}
        """
        return self.call_ollama(prompt)