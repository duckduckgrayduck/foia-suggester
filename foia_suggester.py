import os
import logging
import llm
from muckrock import MuckRock

MUCKROCK_USERNAME = os.environ.get("MUCKROCK_USERNAME")
MUCKROCK_PASSWORD = os.environ.get("MUCKROCK_PASSWORD")
MAX_REQUESTS = 100

if not MUCKROCK_USERNAME or not MUCKROCK_PASSWORD:
    raise ValueError("Please set MUCKROCK_USERNAME and MUCKROCK_PASSWORD as environment variables.")

logging.basicConfig(level=logging.ERROR)
client = MuckRock(MUCKROCK_USERNAME, MUCKROCK_PASSWORD, loglevel=logging.INFO)


def select_model():
    """Prompt user to select a model, fallback to default on invalid input."""
    models = llm.get_models()  # returns a list of model objects
    if not models:
        print("No models found, using default model.")
        return llm.get_model()

    print("\nAvailable models:")
    for idx, model in enumerate(models, start=1):
        # Use str(model) for display; fallback to 'unknown' if needed
        name = getattr(model, "id", None) or str(model) or f"Model {idx}"
        print(f"{idx}. {name}")

    choice = input("Choose a model by number (press Enter for default): ").strip()
    if not choice:
        return llm.get_model()  # default

    # Try to parse user input as integer index
    try:
        index = int(choice)
        if 1 <= index <= len(models):
            return models[index - 1]
    except ValueError:
        pass

    # Invalid input — fallback
    print("Invalid input, using default model.")
    return llm.get_model()


def select_jurisdiction(client):
    narrow = input("Do you want to narrow the search to a specific state or only federal agencies? (y/n): ").strip().lower()
    if narrow != "y":
        return None

    while True:
        abbrev = input("Enter the jurisdiction abbreviation (e.g., MA, IL, send USA for federal): ").strip().upper()
        level = "f" if abbrev == "USA" else "s"
        jurisdictions = client.jurisdictions.list(abbrev=abbrev, level=level)

        if not jurisdictions:
            print(f"No jurisdiction found with abbreviation '{abbrev}'. Please try again.")
            continue

        jurisdiction = jurisdictions[0]
        print(f"Filtering to {jurisdiction.name} (ID {jurisdiction.id})")
        return jurisdiction.id


def search_requests(topic, jurisdiction_id=None):
    params = {"search": topic}
    if jurisdiction_id:
        params["jurisdiction"] = jurisdiction_id
    requests = client.requests.list(**params)
    print(f"Found {requests.count} requests for topic '{topic}'" +
          (f" in this jurisdiction" if jurisdiction_id else ""))
    return requests


def filter_requests(requests):
    success_status = ["done", "partial"]
    successful = [r for r in requests if r.status in success_status]
    unsuccessful = [r for r in requests if r.status not in success_status]
    return successful, unsuccessful


def generate_suggestion(model, topic, requests):
    successful, _ = filter_requests(requests)
    if not successful:
        print("No successful requests found to use as examples.")
        return None

    count = len(successful)
    if count > MAX_REQUESTS:
        print(f"{count} successful requests found, but only sending the most recent {MAX_REQUESTS} to the model for parsing…")
        successful = successful[:MAX_REQUESTS]
    else:
        print(f"Sending {count} successful request{'s' if count != 1 else ''} to the model for parsing…")

    text_examples = "\n\n".join(
        f"Title: {r.title}\nBody: {r.requested_docs or '[No text available]'}" for r in successful
    )

    prompt = f"""
        You are an expert in crafting public records requests.
        Here are some recent successful requests on {topic}:

        {text_examples}

        Suggest a clearer, more effective FOIA request for a journalist who wants records on {topic}.

        Omit any introduction, outtro, citations of laws, rationale, etc. Avoid naming any specific agencies as well. 
        Avoid splitting into a title and body. 
    """

    response = model.prompt(prompt)
    return response.text().strip()


def choose_agency(jurisdiction_id=None):
    while True:
        query = input("Enter the agency name to search: ").strip()
        agencies = client.agencies.list(
            name=query,
            jurisdiction__id=jurisdiction_id
        )
        approved_agencies = [a for a in agencies if getattr(a, "status", None) == "approved"]

        if not approved_agencies:
            print(f"No approved agencies found for '{query}'. Try again.")
            continue

        agencies_to_show = approved_agencies[:5]
        print("\nSelect an agency:")
        for idx, agency in enumerate(agencies_to_show, start=1):
            print(f"{idx}. {agency.name} (ID {agency.id})")

        choice = input("Choose an agency by number: ").strip()
        if not choice.isdigit() or not (1 <= int(choice) <= len(agencies_to_show)):
            print("Invalid choice. Try again.")
            continue

        return agencies_to_show[int(choice) - 1].id


def choose_organization():
    user = client.users.me()
    org_ids = user.organizations
    orgs = [client.organizations.retrieve(org_id) for org_id in org_ids]

    print("\nSelect an organization to bill the request under:")
    for idx, org in enumerate(orgs, start=1):
        print(f"{idx}. {org.name} (ID {org.id})")

    while True:
        choice = input("Choose an organization by number: ").strip()
        if not choice.isdigit() or not (1 <= int(choice) <= len(orgs)):
            print("Invalid choice. Try again.")
            continue
        return orgs[int(choice) - 1].id


def file_request(suggested_request, jurisdiction_id=None):
    confirm = input("Would you like to file this request? (y/n): ").strip().lower()
    if confirm != "y":
        print("Okay, not filing the request.")
        return

    agency_id = choose_agency(jurisdiction_id=jurisdiction_id)
    org_id = choose_organization()

    title = input("Enter a short title for your request: ").strip()
    if not title:
        title = "Public Records Request"

    new_request_data = {
        "title": title,
        "requested_docs": suggested_request,
        "organization": org_id,
        "agencies": [agency_id],
    }

    client.requests.create(**new_request_data)
    print("\nRequest filed successfully!")


def main():
    model = select_model()
    topic = input("Enter the topic you want to file a FOIA request about: ").strip()
    jurisdiction_id = select_jurisdiction(client)
    print(f"Searching for FOIA requests about: {topic}")
    requests = search_requests(topic, jurisdiction_id=jurisdiction_id)
    suggested_request = generate_suggestion(model, topic, requests)

    if suggested_request:
        print("\nSuggested FOIA request:\n")
        print(suggested_request)
        file_request(suggested_request, jurisdiction_id=jurisdiction_id)
    else:
        print("Could not generate a suggestion.")


if __name__ == "__main__":
    main()
