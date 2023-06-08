import sys
import json
import requests

def validate_email(email_to_validate):
    API_KEY = 'tswE4KFLOY6mjg7hmClP1N9KsiDstI37ETn83qLY'
    url_bouncer = f"https://api.usebouncer.com/v1.1/email/verify?email={email_to_validate}"
    headers = {'x-api-key': API_KEY}
    
    response = requests.get(url_bouncer, headers=headers)
    response_dict = json.loads(response.text)
    
    return response_dict

def main():
    email_to_validate = sys.argv[1]
    response = validate_email(email_to_validate)

    print("Email:", response["email"])
    print("Status:", response["status"])
    print("Reason:", response["reason"])
    print("Domain Name:", response["domain"]["name"])
    print("Accept All:", response["domain"]["acceptAll"])
    print("Disposable:", response["domain"]["disposable"])
    print("Free:", response["domain"]["free"])
    print("Role:", response["account"]["role"])
    print("Disabled:", response["account"]["disabled"])
    print("Full Mailbox:", response["account"]["fullMailbox"])
    print("DNS Type:", response["dns"]["type"])
    print("DNS Record:", response["dns"]["record"])
    print("Provider:", response["provider"])

    if response['status'] != 'deliverable':
        print("\nInvalid Email, provide a new one.")
if __name__ == "__main__":
    main()
