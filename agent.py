# agent.py
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage
import config

# Groq LLM initialize karo
llm = ChatGroq(
    api_key    = config.GROQ_API_KEY,
    model_name = config.MODEL_NAME
)

# ─────────────────────────────────────────
# 1. INTENT DETECTION
# ─────────────────────────────────────────
def detect_intent(email_body):
    messages = [
        SystemMessage(content="""
You are a sales assistant. Analyze the customer email and detect the intent.
Reply with ONLY one of these words:
- buying       (customer wants to purchase)
- inquiry      (customer asking for info)
- complaint    (customer has a problem)
- followup     (customer following up)
- other        (anything else)
Just reply with one word, nothing else.
        """),
        HumanMessage(content=f"Customer email:\n{email_body}")
    ]
    response = llm.invoke(messages)
    return response.content.strip().lower()


# ─────────────────────────────────────────
# 2. LEAD SCORING
# ─────────────────────────────────────────
def score_lead(email_body, intent):
    messages = [
        SystemMessage(content="""
You are a sales lead qualifier. Based on the email and intent, 
give a lead score from 1 to 10.
- 8 to 10 = Hot lead (ready to buy)
- 5 to 7  = Warm lead (interested)
- 1 to 4  = Cold lead (just browsing)
Reply with ONLY a number between 1 and 10. Nothing else.
        """),
        HumanMessage(content=f"Intent: {intent}\nCustomer email:\n{email_body}")
    ]
    response = llm.invoke(messages)
    try:
        score = int(response.content.strip())
        # Make sure score is between 1 and 10
        score = max(1, min(10, score))
    except:
        score = 5
    return score


# ─────────────────────────────────────────
# 3. REPLY GENERATION
# ─────────────────────────────────────────
def generate_reply(sender, subject, email_body, intent, lead_score):
    messages = [
        SystemMessage(content="""
You are a professional sales representative. 
Write a personalized, polite and convincing email reply.
Rules:
- Keep it short (max 150 words)
- Be professional and friendly
- Address the customer's concern directly
- End with a call to action
- Do not use placeholders like [Your Name]
- Sign off as: Sales Team
        """),
        HumanMessage(content=f"""
Customer Name/Email : {sender}
Subject             : {subject}
Intent              : {intent}
Lead Score          : {lead_score}/10
Customer Email      :
{email_body}

Write a reply email:
        """)
    ]
    response = llm.invoke(messages)
    return response.content.strip()


# ─────────────────────────────────────────
# 4. PROCESS FULL EMAIL
# ─────────────────────────────────────────
def process_email(email_data):
    sender  = email_data["sender"]
    subject = email_data["subject"]
    body    = email_data["body"]

    print(f"\nProcessing email from: {sender}")

    # Step 1 - Intent detect karo
    intent = detect_intent(body)
    print(f"Intent   : {intent}")

    # Step 2 - Lead score karo
    lead_score = score_lead(body, intent)
    print(f"Lead Score: {lead_score}/10")

    # Step 3 - Reply generate karo
    reply = generate_reply(sender, subject, body, intent, lead_score)
    print(f"Reply Generated!")

    return {
        "sender"    : sender,
        "subject"   : subject,
        "body"      : body,
        "intent"    : intent,
        "lead_score": lead_score,
        "reply"     : reply
    }