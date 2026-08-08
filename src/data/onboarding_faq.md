# PrintFlow — Onboarding FAQ

## Getting Started

**Q: How do I create my PrintFlow account?**  
A: Go to app.printflow.io and click "Sign up." Enter your business email and choose a password. You will receive a verification email — click the link inside to activate your account. After verification, you will be prompted to select a subscription plan and enter billing details.

**Q: Can I try PrintFlow before paying?**  
A: Yes. All new accounts get a 14-day free trial on the Pro plan. No credit card is required to start the trial. At the end of the trial, your account downgrades to Starter unless you add a payment method.

**Q: How do I add team members to my account?**  
A: Go to Settings > Team Members > Invite. Enter the email addresses of your colleagues. You can assign them one of three roles: Viewer (read-only), Operator (submit and manage jobs), or Admin (full account access including billing). Team member seats are included in Pro (up to 5 seats) and Enterprise (unlimited seats). Starter accounts support only 1 user.

**Q: What is a "tenant" in PrintFlow?**  
A: A tenant is the organizational unit that holds your account — your company's subscription, users, files, and job history all live inside your tenant. Each tenant is isolated; users in one tenant cannot see or access another tenant's data.

---

## Submitting Jobs

**Q: How do I submit a print job?**  
A: From the dashboard, click "New Job." Select the product type (offset, digital, wide format), upload your file, configure quantity and finishing options, and click "Place Order." The system runs a pre-flight check automatically. If the file passes, your job enters the production queue.

**Q: My file failed pre-flight. What do I do?**  
A: The pre-flight report in the portal shows the exact error code and which page or element caused the failure. Common fixes:
- **ERR_BLEED**: Add 3mm bleed to all sides in your design software and re-export.
- **ERR_FONT**: Re-export your PDF with fonts embedded, or outline all text.
- **ERR_COLOR**: Convert the file to CMYK before uploading (for offset jobs).
- **ERR_RES**: Increase the resolution of embedded images to at least 300 DPI.

**Q: Can I cancel a job after placing it?**  
A: Yes, but only before the job enters the production queue (status "Pending" or "Pre-flight"). Once the status changes to "In Production," cancellation is not possible. To cancel, click the job in your dashboard and select "Cancel Job."

**Q: How do I track my job status?**  
A: All jobs appear in the Jobs dashboard with a live status: Pending → Pre-flight → In Production → Quality Check → Shipped → Delivered. You can also enable email notifications for status changes in Settings > Notifications.

---

## API Integration

**Q: How do I get API access?**  
A: API access is available on the Pro and Enterprise plans. Go to Settings > Developer > API Keys and click "Generate new key." Copy the key immediately — it is shown only once. Store it securely; you will use it as a bearer token in the `Authorization` header on every API request.

**Q: Where is the API documentation?**  
A: Full API reference is at docs.printflow.io/api. The API follows REST conventions and returns JSON. A Postman collection is available for download on the same page.

**Q: What is the API rate limit?**  
A: Pro accounts: 60 requests per minute. Enterprise accounts: 600 requests per minute. Exceeding the limit returns a `429 Too Many Requests` response with a `Retry-After` header indicating how many seconds to wait. Starter accounts do not have API access.

**Q: Can I use webhooks to get notified when a job status changes?**  
A: Yes. Configure webhooks in Settings > Developer > Webhooks. Add the endpoint URL and select which events to subscribe to (e.g., `job.status_changed`, `job.shipped`, `job.delivered`). Webhooks are available on Pro and Enterprise plans only.

---

## Billing and Payments

**Q: What payment methods do you accept?**  
A: PrintFlow accepts all major credit and debit cards (Visa, Mastercard, Amex, Discover) and ACH bank transfer (US accounts only). Enterprise accounts can also be invoiced monthly with Net-30 terms.

**Q: When am I charged?**  
A: Print jobs are charged when you place the order. Subscription fees are billed on the same day each month (the anniversary of your signup date). Invoices are emailed to the billing contact on file.

**Q: Can I get a refund?**  
A: If a job is damaged, incorrect, or PrintFlow is at fault, you are entitled to a reprint or full refund. For buyer's remorse or design errors (where the file itself was wrong), reprints are offered at a 25% discount. Subscription fees are non-refundable once a billing cycle has started.

---

## Support

**Q: How do I contact support?**  
A: In-app chat is available Monday–Friday, 9am–6pm ET. Email support (support@printflow.io) is 24/7. Enterprise accounts have a dedicated account manager and a direct phone line.

**Q: What is the SLA for support response?**  
A: Starter: email within 48 hours. Pro: email within 24 hours, chat within 2 hours during business hours. Enterprise: email within 4 hours, chat within 30 minutes, phone always answered during business hours.

**Q: Is there a status page for platform uptime?**  
A: Yes, at status.printflow.io. You can subscribe to email or SMS alerts for incidents and maintenance windows.
