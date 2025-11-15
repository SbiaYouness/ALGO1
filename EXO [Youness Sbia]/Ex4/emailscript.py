from pathlib import Path
from emailutils import is_valid_email, extract_domain, find_emails_in_file

current_dir = Path(__file__).parent


emails = find_emails_in_file(current_dir / "emails.txt")
    
domains = {}
for email in emails:
    if is_valid_email(email):
        domain = extract_domain(email)
        cmpny = domain.split('.')[0]  # gmail, yahoo
        
        if cmpny not in domains:
            domains[cmpny] = []
        domains[cmpny].append(email)

for cmpny, listem in domains.items():
    output_file = current_dir / f"{cmpny}.txt"
    with open(output_file, 'wt') as f:
        for email in listem:
            f.write(email + "\n")
