# test_agent.py
from agent import process_email

# Fake email banao test k leye
test_email = {
    "sender" : "ahmed@gmail.com",
    "subject": "Product Price Inquiry",
    "body"   : """
    Hello,
    I am interested in buying your software product.
    Can you please tell me the pricing plans?
    I need it for my team of 10 people.
    Looking forward to your response.
    Thanks,
    Ahmed
    """
}

result = process_email(test_email)

print("\n========== RESULT ==========")
print(f"Intent    : {result['intent']}")
print(f"Lead Score: {result['lead_score']}/10")
print(f"\nGenerated Reply:\n{result['reply']}")