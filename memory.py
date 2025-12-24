class ConversationMemory:
    def __init__(self, language):
        self.memory = {
            "language": language,
            "profile": {
                "age": None,
                "income": None,
                "state": None
            },
            "history": []
        }

    def add_user_utterance(self, text):
        self.memory["history"].append({
            "role": "user",
            "text": text
        })

    def add_agent_utterance(self, text):
        self.memory["history"].append({
            "role": "agent",
            "text": text
        })

    def update_profile(self, field, value):
        """
        Updates profile field and detects contradiction.
        Returns True if contradiction detected.
        """
        old_value = self.memory["profile"].get(field)

        if old_value is not None and old_value != value:
            return {
                "contradiction": True,
                "field": field,
                "old_value": old_value,
                "new_value": value
            }

        self.memory["profile"][field] = value
        return {
            "contradiction": False
        }

    def get_missing_fields(self):
        return [
            k for k, v in self.memory["profile"].items()
            if v is None
        ]

    def get_memory_snapshot(self):
        return self.memory
    
# test
if __name__ == "__main__":
    mem = ConversationMemory(language="te")

    print(mem.get_missing_fields())

    print(mem.update_profile("age", 25))
    print(mem.update_profile("age", 30))  # contradiction

    print(mem.get_memory_snapshot())
