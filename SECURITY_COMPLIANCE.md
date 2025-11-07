# Security & Compliance Documentation

## Overview
Levqor implements enterprise-grade security controls and privacy protections to ensure safe handling of customer data and compliance with industry standards.

## Security Architecture

### 1. Authentication & Identity

#### User Authentication
- **Provider**: Supabase Auth
- **Method**: JWT-based authentication
- **Session Management**: Secure HTTP-only cookies
- **Token Expiry**: 1 hour (configurable)
- **Refresh Tokens**: 30 days

#### API Authentication
- **Method**: Bearer token authentication
- **Header Format**: `Authorization: Bearer <token>`
- **Key Rotation**: Manual (automated rotation planned for Q2 2025)

### 2. Data Protection

#### Encryption

**Data in Transit**:
- TLS 1.3 enforced for all connections
- HSTS header with 1-year max-age
- Certificate pinning (future enhancement)

**Data at Rest**:
- SQLite database: Filesystem encryption (host-level)
- Future PostgreSQL: Transparent data encryption (TDE)
- Secrets: Environment variables (encrypted at platform level)

#### PII Protection
- **Email addresses**: SHA-256 hashed in analytics tables
- **Credit card data**: Never stored (handled by Stripe)
- **API keys**: Stored as environment variables, never logged
- **User metadata**: Encrypted JSON blobs

### 3. Access Controls

#### Backend API
- Rate limiting: 100 req/min global, 20 req/min per IP
- Request size limits: 10MB max
- API key validation on sensitive endpoints
- User-scoped data access (queries filtered by user_id)

#### Frontend
- Route protection via Supabase client
- Automatic redirect for unauthenticated users
- CSRF protection via SameSite cookies

### 4. Input Validation

#### Schema Validation
- JSON Schema validation on all API requests
- Content-Type enforcement (application/json)
- SQL injection prevention via parameterized queries
- XSS prevention via output encoding

#### Sanitization
- Email addresses: Lowercased and trimmed
- User input: HTML entity encoding
- File uploads: Type validation (future feature)

### 5. Security Headers

**Implemented Headers**:
```
Strict-Transport-Security: max-age=31536000; includeSubDomains
Content-Security-Policy: default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
Cross-Origin-Opener-Policy: same-origin
Cross-Origin-Embedder-Policy: require-corp
```

### 6. Logging & Monitoring

#### What We Log
- API request metadata (timestamp, endpoint, status code)
- Authentication events (login, logout, failed attempts)
- Billing events (payments, refunds, subscription changes)
- Error stack traces (sanitized, no PII)

#### What We DON'T Log
- Passwords or authentication credentials
- Credit card numbers or CVV codes
- Full request/response bodies with PII
- IP addresses beyond rate limiting (30-day retention)

#### Log Retention
- Application logs: 90 days
- Access logs: 30 days
- Audit logs: 7 years (regulatory compliance)
- Error logs: 180 days

### 7. Third-Party Security

#### Vetted Providers
| Service | Purpose | SOC 2 | GDPR | Data Location |
|---------|---------|-------|------|---------------|
| Stripe | Payments | ✅ | ✅ | US/EU |
| Supabase | Auth | ✅ | ✅ | US-East |
| Resend | Email | ✅ | ✅ | US |
| OpenAI | AI workflows | ✅ | ✅ | US |
| Replit | Hosting | ✅ | ✅ | US |

#### Data Sharing
- **Stripe**: Payment metadata only (no passwords)
- **OpenAI**: Workflow descriptions only (no user PII)
- **Resend**: Recipient email + message content
- **Supabase**: Email + hashed password

## Compliance

### 1. GDPR (General Data Protection Regulation)

#### Data Subject Rights
- **Right to Access**: `/api/v1/me` endpoint provides user data export
- **Right to Deletion**: Account deletion available (support@levqor.ai)
- **Right to Rectification**: `/api/v1/users/{user_id}` PATCH endpoint
- **Right to Portability**: JSON export of user data
- **Right to Object**: Opt-out of analytics tracking

#### Legal Basis for Processing
- **Contract**: User account and billing data
- **Legitimate Interest**: Analytics for product improvement
- **Consent**: Marketing communications (opt-in)

#### Data Minimization
- Collect only essential data (email, name, usage metrics)
- No social media tracking pixels
- No third-party advertising cookies
- Analytics hashed before storage

#### Privacy Policy
- **Location**: `/privacy` page
- **Last Updated**: 2025-01-01
- **Review Cycle**: Quarterly

### 2. CCPA (California Consumer Privacy Act)

#### Consumer Rights
- **Right to Know**: Data inventory provided on request
- **Right to Delete**: Account deletion within 45 days
- **Right to Opt-Out**: No sale of personal information (we don't sell data)
- **Right to Non-Discrimination**: Equal service regardless of privacy choices

#### Do Not Sell
- Levqor does NOT sell personal information
- Third-party sharing limited to service providers
- No advertising or marketing data brokers

### 3. PCI DSS (Payment Card Industry)

#### Compliance Level
- **Level**: Service Provider Level 4
- **Scope**: We do NOT process or store card data
- **Method**: Stripe-hosted payment forms only
- **Attestation**: Stripe PCI DSS Level 1 certified

#### Card Data Handling
- All payment forms hosted by Stripe
- Tokenized card references only
- No card numbers in logs or databases
- PCI scope: Zero (out-of-scope)

### 4. SOC 2 Type II (Planned Q3 2025)

#### Current Status: In Preparation

#### Control Objectives
- **Security**: Access controls, encryption, monitoring
- **Availability**: 99.9% uptime SLA, disaster recovery
- **Processing Integrity**: Data validation, error handling
- **Confidentiality**: Secrets management, encryption at rest
- **Privacy**: GDPR/CCPA compliance, data minimization

#### Timeline
- **Q1 2025**: Internal controls documentation
- **Q2 2025**: Third-party audit engagement
- **Q3 2025**: SOC 2 Type II certification

## Incident Response

### 1. Incident Classification

#### Severity Levels
- **Critical (P0)**: Data breach, complete service outage
- **High (P1)**: Partial outage, authentication bypass
- **Medium (P2)**: Performance degradation, minor bugs
- **Low (P3)**: Cosmetic issues, feature requests

### 2. Response Procedures

#### Data Breach Protocol
1. **Detection** (0-1 hour): Alert via monitoring systems
2. **Containment** (1-4 hours): Isolate affected systems
3. **Notification** (24-72 hours): Inform affected users
4. **Remediation** (1-7 days): Patch vulnerabilities
5. **Post-Mortem** (7-14 days): Root cause analysis

#### Notification Thresholds
- **Immediate**: >100 users affected OR payment data exposed
- **24-hour**: >10 users affected OR PII exposed
- **72-hour**: Any confirmed security incident (GDPR requirement)

### 3. Contact Information

**Security Team**: security@levqor.ai
**Bug Bounty**: No formal program (planned Q2 2025)
**Responsible Disclosure**: 90-day disclosure policy

## Vulnerability Management

### 1. Dependency Scanning
- **Tool**: npm audit (frontend), safety (Python backend)
- **Frequency**: Weekly automated scans
- **Critical CVEs**: Patched within 48 hours
- **High CVEs**: Patched within 7 days

### 2. Penetration Testing
- **Status**: Not yet conducted
- **Planned**: Q2 2025 (external pentest)
- **Scope**: API endpoints, authentication, authorization

### 3. Code Security

#### Secure Development Practices
- Input validation on all user inputs
- Parameterized SQL queries (no raw SQL)
- Output encoding to prevent XSS
- Rate limiting on all public endpoints
- Error messages sanitized (no stack traces to users)

#### Code Review
- All code changes reviewed before deployment
- Security-focused review for auth/billing changes
- Automated linting (ESLint, Pylint)

## Data Residency & Sovereignty

### Current Architecture
- **Primary Region**: US-East (Replit/Supabase)
- **Backup Storage**: Local filesystem (same region)
- **Email Service**: US (Resend)

### Future Multi-Region
- **Q2 2025**: EU-West region deployment
- **GDPR Compliance**: EU customer data stays in EU
- **Data Localization**: Regional database replicas

## Security.txt

**Location**: `/.well-known/security.txt`
**Contents**:
```
Contact: mailto:security@levqor.ai
Expires: 2025-12-31T23:59:59.000Z
Preferred-Languages: en
Canonical: https://levqor.ai/.well-known/security.txt
Policy: https://levqor.ai/security-policy
```

## Certifications & Audits

### Current Status
- [x] HTTPS/TLS encryption
- [x] Secure authentication (Supabase)
- [x] PCI DSS compliance (via Stripe)
- [x] Privacy policy published
- [x] Terms of service published
- [ ] SOC 2 Type II (Q3 2025)
- [ ] ISO 27001 (Q4 2025)
- [ ] HIPAA compliance (future, if needed)

## Security Roadmap

### Q1 2025
- [ ] Implement automated vulnerability scanning
- [ ] Add rate limiting per user
- [ ] Deploy WAF (Web Application Firewall)
- [ ] Implement audit logging

### Q2 2025
- [ ] External penetration testing
- [ ] Bug bounty program launch
- [ ] SOC 2 Type II audit initiation
- [ ] Multi-factor authentication (MFA)

### Q3 2025
- [ ] SOC 2 Type II certification
- [ ] ISO 27001 preparation
- [ ] Enhanced DDoS protection
- [ ] Security training for team

### Q4 2025
- [ ] ISO 27001 certification
- [ ] Annual penetration test
- [ ] Security incident tabletop exercises
- [ ] Compliance automation tooling

## Contact & Reporting

**Security Issues**: security@levqor.ai
**Privacy Questions**: privacy@levqor.ai
**Compliance Inquiries**: compliance@levqor.ai
**General Support**: support@levqor.ai

**Response Time SLA**:
- Critical security issues: 4 hours
- Privacy requests: 24 hours
- Compliance questions: 48 hours

---

*Last Updated: 2025-01-07*
*Next Review: 2025-04-07*
