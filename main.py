import csv
import json
import pickle
import database as db
import waterfall_api as api


def store_to_csv(contacts):
    writer = csv.writer(open('output/contacts.csv', 'w', encoding='utf8'), delimiter=',', lineterminator='\n', quotechar='"', quoting=csv.QUOTE_ALL)
    for contact in contacts:
        writer.writerow(contact)


def fetch_contacts(debug=False):
    if not debug:
        reader = csv.reader(open('data/companies.csv', 'r', encoding='utf8'))
        reader.__next__()  # skip header row
        domain_title_list = []
        for row in reader:
            domain, title_filter = row
            domain_title_list.append((domain, title_filter))
        contacts = api.fetch_companies_data(domain_title_list)

        # cache api response for testing
        # pickle.dump(contacts, open('output/contacts.pkl', 'wb'))
    else:
        try:
            contacts = pickle.load(open('output/contacts.pkl', 'rb'))
        except FileNotFoundError:
            contacts = []

    # save contacts to database

    db_contacts = []
    for contact in contacts:
        items = contact.list_contacts()
        if len(items) > 0:
            db_contacts.extend(items)

    db.store_contacts(db_contacts)

    # save contacts to csv
    csv_contacts = []
    for contact in contacts:
        if len(contact.persons) > 0:
            csv_contacts.extend(contact.as_csv())
    store_to_csv(csv_contacts)


if __name__ == '__main__':
    fetch_contacts(debug=False)
