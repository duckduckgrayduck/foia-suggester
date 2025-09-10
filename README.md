# FOIA Request Suggester

This script is a demonstration of using the MuckRock Requests API in conjunction with LLMs. This script generates FOIA (Freedom of Information Act) or public records request language based on past successful requests from [MuckRock](https://www.muckrock.com/).  
It uses the **MuckRock Requests API** to fetch requests that were marked as complete in the past and the **Google Gemini API** to generate a suggested request draft based on this input. 
The script can also file the request directly to MuckRock once the user approves.

---

## Requirements

- Python 3.9+
- pip
- A MuckRock account with valid login credentials.
- Your credentials should be stored as local environment variables under MUCKROCK_USERNAME and MUCKROCK_PASSWORD for this script to work. 
- Access to the Google Gemini API (via the `google.genai` package) and the GEMINI_API_KEY set in your local development environment. See Google's [Gemini Quick Start Guide](https://ai.google.dev/gemini-api/docs/quickstart?lang=python).
- The python-muckrock package installed in your local environment (pip install python-muckrock). 
---

## Example Flow

```console
s@s:~/Downloads$ python3 foia_suggestor.py 
Enter the topic you want to file a FOIA request about: facial recognition
Do you want to narrow the search to a specific state or only federal agencies? (y/n): n
Searching for FOIA requests about: facial recognition
Found 625 requests for topic 'facial recognition'
146 successful requests found, but only sending the most recent 100 to Gemini for parsing…

Suggested FOIA request:

All records concerning facial recognition technology and services, encompassing all systems, software, and equipment currently in use, under consideration, or previously used by the agency, whether purchased, licensed, developed internally, or accessed via external contractors or other agencies. This includes pilot programs, testing programs, and prototypes.

The period of this request is from January 1, 2017, to the present date, unless a different period is specified for a particular item below.

Records requested include, but are not limited to:

*   **Technology Overview & Deployment:**
    *   The number of facial recognition software licenses or facial recognition-enabled equipment currently in place.
    *   Identification of all facial recognition systems or services used or accessed, including the vendor (if external) or details of internal development, and their current status (e.g., in use, pilot, testing, under consideration, retired).
    *   Materials describing the function, capabilities, and technical specifications of any facial recognition system considered or in use.

*   **Acquisition, Procurement, and Financial Records:**
    *   All agreements, contracts (including amendments, attachments, and exhibits), licensing agreements, data sharing agreements, intergovernmental service agreements, memoranda of understanding (MOUs), and non-disclosure agreements related to the acquisition, use, or sharing of facial recognition technology or services.
    *   All bidding and procurement documents, including Requests for Proposal (RFPs), Requests for Information (RFIs), sole source or limited source justifications, responsive bids, and documentation of vendor selection.
    *   All financial records, including purchase orders, invoices, payment records, funding opportunity announcements, grant applications, and progress reports related to facial recognition technology or services.
    *   All marketing materials, brochures, fact sheets, or presentations received from or provided by vendors of facial recognition technology.

*   **Policies, Procedures, and Training:**
    *   All existing or proposed usage policies, protocols, directives, guidance documents, memoranda, or standard operating procedures (SOPs) governing the use, access, and administration of facial recognition technology. This includes permissible/impermissible uses, data storage procedures, and prohibited activities.
    *   All training materials, manuals, user guides, handbooks, presentations (including recorded video/audio, PowerPoint files, slides), or other instructional materials provided to personnel regarding the use, sharing, or access to facial recognition technology or data. This should include any legal standards required before use and any training materials addressing bias in facial recognition.

*   **Data Management and Privacy:**
    *   Documents describing the source(s) of photographs or facial templates included in any facial recognition database accessible to or used by this agency (e.g., agency booking photos, other agency booking photos, DMV photos, publicly sourced images).
    *   Documents detailing the current number of photographs or facial templates included in any facial recognition database accessible to or used by this agency, including screenshots of program dashboards if they contain this information.
    *   All data retention policies, data security policies, data security specifications, privacy impact assessments, and security audits related to facial recognition systems or the data they process.
    *   For any machine learning algorithms or programs that rely on input data, provide copies of the five most recent sets of data that were used for input, and the five most recent outputs of the software, in their native format. If these contain exempt information, please provide all material save for specific information legally exempted. Also, a description of input and output data fields to aid in understanding the type of information submitted and produced.

*   **Performance, Audits, and Usage Statistics:**
    *   All validation studies, accuracy assessments, reliability reports, audits, or other documents evaluating the performance or policy compliance of facial recognition systems.
    *   All audit logs for any facial recognition system(s) from January 1, 2020, to the present date. If the system provides options for the time period covered in the audit logs, please provide daily reports.
    *   All reports detailing aggregated usage and transaction statistics for any facial recognition system(s) from January 1, 2020, to the present date. This includes, but is not limited to, the number of queries, number of unique users, and number of photographs/facial templates uploaded. If the system provides options for the time period covered in these statistics, please provide daily reports.
    *   Any reports (weekly, monthly, annual, or otherwise), presentations, spreadsheets, or memoranda relating to the volume or efficacy of facial recognition searches.
    *   Any algorithm or code developed for implementation of or as part of any facial recognition software or program, or any related system that conducts calculations or decision-making. This includes original source code, compiled binaries (executables), specification documents, spreadsheets, program scripts, and other digital materials.

*   **Requests for Facial Recognition Searches:**
    *   All requests for facial recognition searches and associated reports made by local, county, state, or federal law enforcement to this agency from January 1, 2020, to December 31, 2020. This includes email requests (entire threads and attachments) and requests submitted via standardized forms or web portals.

*   **Litigation and Complaints:**
    *   Any notices of potential legal action (e.g., intent to sue letters), formal legal complaints, or comparable documents received by or sent to this agency, or its legal representatives, regarding alleged misidentification, false arrest, or other issues related to the use of facial recognition technology since January 1, 2018. This includes civil lawsuits that are open or closed.
    *   Any settlement agreements or other resolutions relating to such cases.
    *   A list, database, or spreadsheet detailing each false arrest lawsuit brought against this agency or departments it represents since January 1, 2018, including (where available) plaintiff, defendant, court docket number, date filed, date settled/closed, and settlement amount.
Would you like to file this request? (y/n): y
Enter the agency name to search: Chicago Police Department

Select an agency:
1. Chicago Police Department (ID 503)
2. North Chicago Police Department (ID 28690)
3. University of Chicago Police Department (ID 7116)
4. East Chicago Police Department (ID 11945)
Choose an agency by number: 1

Select an organization to bill the request under:
1. MuckRock Staff (ID 1)
2. sanjin (ID 24695)
3. test new muck org (ID 166692)
Choose an organization by number: 1
Enter a short title for your request: Gemini Test Request
https://www.muckrock.com/foi/multirequest/gemini-test-request-162339/
```

Request filed successfully!

