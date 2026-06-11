def build_email(name: str):
    subject = 'Partnership Opportunity with EyDost'
    body = f'''Hi {name or 'there'},

My name is Elvin and I am the founder of EyDost, a travel platform providing eSIM packages in 150+ countries.

We are looking for travel creators to join our affiliate program.

✅ 15% commission on every sale
✅ 10% discount for your audience
✅ Up to $150 advertising budget

Would you be interested in discussing a collaboration?

Best regards,
Elvin Eyvazov
Founder, EyDost
'''
    return subject, body
