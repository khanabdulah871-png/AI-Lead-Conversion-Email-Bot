# test_db.py
from database import create_tables, save_lead, save_message, get_all_leads

# Tables banao
create_tables()

# Ek test lead save karo
lead_id = save_lead(
    sender     = "customer@gmail.com",
    subject    = "Product inquiry",
    body       = "Mujhe aapke product ki price batayein",
    intent     = "buying",
    lead_score = 8
)
print(f"Lead saved! ID: {lead_id}")

# Message save karo
save_message(lead_id, "customer", "Mujhe aapke product ki price batayein")
save_message(lead_id, "agent",    "Assalam o Alaikum! Hamara product...")

# Saare leads dekho
leads = get_all_leads()
for lead in leads:
    print(f"ID: {lead['id']} | {lead['sender']} | Score: {lead['lead_score']} | Status: {lead['status']}")