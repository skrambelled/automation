import re


def get_document(path):
    with open(path, 'r') as file:
        text = file.read()
    return text


def parse_phone_numbers(text):
    """
    select only phone numbers from a mess of text, and output a neat list of phone numbers

    phone numbers without an area code will be assigned a 206 area code

    example input formats:
    (123) 456 7890
    123 456 7890
    123-456-7890
    (123)456 7890x1234
    etc

    output format is: 123-456-7890
    or there there is an extention associated: 123-456-7890x123 (where the extension can be at least 1 digit long and longer)
    """
    pattern = r"((\(\d{3}\)|\d{3})?[\s-]?(\d{3})[\s-]?(\d{4})(x\d+)?)"
    numbers = re.findall(pattern,text)
    formatted_numbers = []
    for number in numbers:
        preamble = ""
        if not len(number[1]):
            preamble += "206"
        elif len(number[1]) == 5:
            preamble += number[1][1:4]
        else:
            preamble += number[1]

        current_number = f"{preamble}-{number[2]}-{number[3]}{number[4]}"
        if not current_number in formatted_numbers:
            formatted_numbers.append(current_number)
    formatted_numbers.sort()
    return formatted_numbers

def write_phone_numbers(soupy_mess_doc, existing_contacts):
    formatted_numbers = parse_phone_numbers(get_document(soupy_mess_doc))
    existing_contacts = parse_phone_numbers(get_document(existing_contacts))

    # remove contacts from our incomming numbers if we already had them in existing-contacts.txt
    for contact in existing_contacts:
        if contact in formatted_numbers:
            formatted_numbers.remove(contact)

    # hardcoding the output file, cause i dont want to mess with security risks
    target = "phone_numbers.txt"
    with open(target, 'w') as file:
        file.write("\n".join(formatted_numbers))


def parse_emails(text):
    pattern = r"(\w+(\.\w+)*@\w+\.\w+)"
    emails = re.findall(pattern, text)

    new_emails = []
    for email in emails:
        if not email[0] in new_emails:
            new_emails.append(email[0])

    new_emails.sort()
    return new_emails


def write_emails(soupy_mess_doc, existing_contacts):
    new_emails = parse_emails(get_document(soupy_mess_doc))
    existing_emails = parse_emails(get_document(existing_contacts))

    # remove contacts from our incomming numbers if we already had them in existing-contacts.txt
    for email in existing_emails:
        if email in new_emails:
            new_emails.remove(email)

    # hardcoding the output file, cause i dont want to mess with security risks
    target = "emails.txt"
    with open(target, 'w') as file:
        file.write("\n".join(new_emails))


if __name__ == "__main__":
    write_phone_numbers('assets/potential-contacts.txt', 'assets/existing-contacts.txt')
    write_emails('assets/potential-contacts.txt', 'assets/existing-contacts.txt')
