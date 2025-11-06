# Stripe Invoice Branding & Tax/VAT Support

## Invoice Branding

### Setup Steps
1. Go to Stripe Dashboard → Settings → Branding
2. Upload company logo (PNG, 512x512px recommended)
3. Set brand color (hex code)
4. Add company details:
   - Legal name
   - Address
   - Tax ID
   - Website

### Email Customization
Configure receipt emails:
- From name: "Levqor"
- Reply-to: billing@levqor.ai
- Custom footer: Support link, unsubscribe

## Tax & VAT Support

### EU VAT Configuration
1. **Enable Tax Collection:**
   - Stripe Dashboard → Settings → Tax
   - Enable "Automatically calculate and collect taxes"
   - Select regions: EU, UK

2. **VAT Rates (Automatic):**
   - Standard: 19-27% (varies by country)
   - Digital services: Destination-based
   - Reverse charge: B2B with VAT ID

3. **Customer Tax ID Capture:**
```javascript
// In checkout session creation
tax_id_collection: {
  enabled: true
}
```

### UK VAT
- Rate: 20%
- Registration threshold: £85,000/year
- VAT number format: GB123456789

### US Sales Tax
- Configure via Stripe Tax
- Nexus detection automatic
- Rates by state (0-10%)

## Implementation

### Backend (run.py)
```python
# In create_checkout_session
checkout_session = stripe.checkout.Session.create(
    # ... existing params ...
    tax_id_collection={'enabled': True},
    automatic_tax={'enabled': True},
    customer_update={
        'address': 'auto',
        'name': 'auto'
    }
)
```

### Invoice Details
Invoices automatically include:
- Company branding
- Tax breakdown
- Customer VAT ID (if provided)
- VAT-compliant format

## Testing

### Test VAT Collection
1. Use test mode
2. Enter EU address at checkout
3. Verify VAT line item appears
4. Check invoice PDF includes VAT

### Test Cards
```
EU: 4242 4242 4242 4242
UK: 4000 0082 6000 0000
```

## Compliance

### EU Requirements
- ✅ Display prices including VAT
- ✅ Collect customer location
- ✅ Apply correct VAT rate
- ✅ Issue VAT-compliant invoices
- ✅ Store VAT evidence (automatic)

### Record Keeping
Stripe automatically stores:
- Customer location evidence
- VAT calculations
- Invoice history
- Tax reports

## Cost
- Stripe Tax: 0.5% of transaction (max $2.00)
- Worth it for automatic compliance

## Status
- ✅ Configuration documented
- ⏳ Requires Stripe dashboard setup (5 min)
