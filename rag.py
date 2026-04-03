import os

def load_knowledge_base():
    with open("knowledge_base/company_policy.txt", "r", encoding="utf-8") as f:
        return f.read()
kb = load_knowledge_base()

prompt = f"""
You are an enterprise IT assistant.

Use the following internal knowledge base to answer accurately:

{kb}

Now analyze this ticket:
{ticket_text}

Return JSON...
"""