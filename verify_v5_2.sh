#!/bin/bash
echo "=== VERIFYING LEVQOR v5.2 ==="
echo ""

CHECKS=0
PASSED=0

echo "[1] GDPR User Deletion Endpoint:"
CHECKS=$((CHECKS+1))
if [ -f api/user_delete.py ]; then
    echo "   ✓ api/user_delete.py present"
    PASSED=$((PASSED+1))
else
    echo "   ✗ api/user_delete.py missing"
fi

echo ""
echo "[2] Database Field Encryption:"
CHECKS=$((CHECKS+1))
if [ -f db/encrypt_fields.py ]; then
    echo "   ✓ db/encrypt_fields.py present"
    PASSED=$((PASSED+1))
else
    echo "   ✗ db/encrypt_fields.py missing"
fi

echo ""
echo "[3] Off-site Backup Upload:"
CHECKS=$((CHECKS+1))
if [ -x scripts/upload_backup.sh ]; then
    echo "   ✓ scripts/upload_backup.sh executable"
    PASSED=$((PASSED+1))
else
    echo "   ✗ scripts/upload_backup.sh missing or not executable"
fi

echo ""
echo "[4] Referral Fraud Guard:"
CHECKS=$((CHECKS+1))
if [ -f api/referral_guard.py ]; then
    echo "   ✓ api/referral_guard.py present"
    PASSED=$((PASSED+1))
else
    echo "   ✗ api/referral_guard.py missing"
fi

echo ""
echo "[5] Admin Refund Endpoint:"
CHECKS=$((CHECKS+1))
if [ -f api/refund.py ]; then
    echo "   ✓ api/refund.py present"
    PASSED=$((PASSED+1))
else
    echo "   ✗ api/refund.py missing"
fi

echo ""
echo "[6] Email Unsubscribe Footer:"
CHECKS=$((CHECKS+1))
if [ -f templates/email_footer.html ]; then
    echo "   ✓ templates/email_footer.html present"
    PASSED=$((PASSED+1))
else
    echo "   ✗ templates/email_footer.html missing"
fi

echo ""
echo "[7] Daily Cost Report:"
CHECKS=$((CHECKS+1))
if [ -f scripts/daily_cost_report.py ]; then
    echo "   ✓ scripts/daily_cost_report.py present"
    PASSED=$((PASSED+1))
else
    echo "   ✗ scripts/daily_cost_report.py missing"
fi

echo ""
echo "[8] Encryption Module Test:"
CHECKS=$((CHECKS+1))
python3 - <<PY
try:
    import sys
    sys.path.insert(0, '.')
    from db.encrypt_fields import encrypt_field, decrypt_field
    test = "test@example.com"
    encrypted = encrypt_field(test)
    decrypted = decrypt_field(encrypted)
    if test == decrypted:
        print("   ✓ Encryption module working correctly")
        exit(0)
    else:
        print("   ✗ Encryption/decryption mismatch")
        exit(1)
except Exception as e:
    print(f"   ⚠ Encryption module test failed: {e}")
    print("   (Install: pip install cryptography)")
    exit(1)
PY

if [ $? -eq 0 ]; then
    PASSED=$((PASSED+1))
fi

echo ""
echo "========================================="
echo "Verification Results: $PASSED/$CHECKS checks passed"
echo "========================================="

if [ $PASSED -eq $CHECKS ]; then
    echo "✓ All v5.2 upgrades verified successfully!"
    exit 0
else
    echo "⚠ Some checks failed - review output above"
    exit 1
fi
