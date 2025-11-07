import sqlite3
import datetime

conn = sqlite3.connect('levqor.db')
cursor = conn.cursor()

rows = cursor.execute("""
    SELECT p.id, u.email, p.pending_commission 
    FROM partners p
    JOIN users u ON p.user_id = u.id
    WHERE p.pending_commission >= 50
""").fetchall()

if not rows:
    print("[ℹ] No partners eligible for payout (minimum $50)")
    conn.close()
    exit(0)

print(f"[📋] Found {len(rows)} partners eligible for payout:")
for id, email, amt in rows:
    print(f"   {email}: ${amt:.2f}")

print("\nProcess these payouts? (yes/no): ", end="")
confirm = input().strip().lower()

if confirm != "yes":
    print("[✗] Payout cancelled")
    conn.close()
    exit(0)

for id, email, amt in rows:
    cursor.execute(
        "UPDATE partners SET pending_commission = 0, total_paid = total_paid + ? WHERE id = ?",
        (amt, id)
    )
    cursor.execute(
        "INSERT INTO partner_payouts (partner_id, amount, status, paid_at) VALUES (?, ?, 'completed', ?)",
        (id, amt, datetime.datetime.utcnow().isoformat())
    )
    print(f"[✓] Paid ${amt:.2f} to {email}")

conn.commit()
conn.close()
print(f"\n[✓] Processed {len(rows)} partner payouts successfully")
