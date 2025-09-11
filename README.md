# FOIA Request Suggester

This script is a demonstration of using the MuckRock Requests API in conjunction with LLMs. This script generates FOIA (Freedom of Information Act) or public records request language based on past successful requests from [MuckRock](https://www.muckrock.com/).  
It uses the **MuckRock Requests API** to fetch requests that were marked as complete in the past and allows you to pass these successful requests to Simon Willison's **llm** library to generate a suggested request draft based on this input. It allows you to select a model you'd like to run the prompt on.
The script can also file the request directly to MuckRock once the user approves.

---

## Install

```sh
pip install git+https://github.com/duckduckgrayduck/foia-suggester.git

# or uv, which is better and faster
uv add git+https://github.com/duckduckgrayduck/foia-suggester.git
```

## Requirements

- Python 3.9+
- pip
- A MuckRock account with valid login credentials.
- Your credentials should be stored as local environment variables under MUCKROCK_USERNAME and MUCKROCK_PASSWORD for this script to work.
- [llm](https://llm.datasette.io/en/stable/setup.html)
- For any model that requries API calls that you select to use this tool with, you will need to [set API keys](https://llm.datasette.io/en/stable/setup.html#api-key-management). For more assistance with installing more models, [consult the documentation on plugins](https://llm.datasette.io/en/stable/plugins/index.html).
- The python-muckrock package installed in your local environment (pip install python-muckrock).

---

## Example Flow

```console
s@s:~/Downloads$ python3 foia_suggester.py

Available models:
1. OpenAI Chat: gpt-4o
2. OpenAI Chat: chatgpt-4o-latest
3. OpenAI Chat: gpt-4o-mini
4. OpenAI Chat: gpt-4o-audio-preview
5. OpenAI Chat: gpt-4o-audio-preview-2024-12-17
6. OpenAI Chat: gpt-4o-audio-preview-2024-10-01
7. OpenAI Chat: gpt-4o-mini-audio-preview
8. OpenAI Chat: gpt-4o-mini-audio-preview-2024-12-17
9. OpenAI Chat: gpt-4.1
10. OpenAI Chat: gpt-4.1-mini
11. OpenAI Chat: gpt-4.1-nano
12. OpenAI Chat: gpt-3.5-turbo
13. OpenAI Chat: gpt-3.5-turbo-16k
14. OpenAI Chat: gpt-4
15. OpenAI Chat: gpt-4-32k
16. OpenAI Chat: gpt-4-1106-preview
17. OpenAI Chat: gpt-4-0125-preview
18. OpenAI Chat: gpt-4-turbo-2024-04-09
19. OpenAI Chat: gpt-4-turbo
20. OpenAI Chat: gpt-4.5-preview-2025-02-27
21. OpenAI Chat: gpt-4.5-preview
22. OpenAI Chat: o1
23. OpenAI Chat: o1-2024-12-17
24. OpenAI Chat: o1-preview
25. OpenAI Chat: o1-mini
26. OpenAI Chat: o3-mini
27. OpenAI Chat: o3
28. OpenAI Chat: o4-mini
29. OpenAI Chat: gpt-5
30. OpenAI Chat: gpt-5-mini
31. OpenAI Chat: gpt-5-nano
32. OpenAI Chat: gpt-5-2025-08-07
33. OpenAI Chat: gpt-5-mini-2025-08-07
34. OpenAI Chat: gpt-5-nano-2025-08-07
35. OpenAI Completion: gpt-3.5-turbo-instruct
36. Anthropic Messages: anthropic/claude-3-opus-20240229
37. Anthropic Messages: anthropic/claude-3-opus-latest
38. Anthropic Messages: anthropic/claude-3-sonnet-20240229
39. Anthropic Messages: anthropic/claude-3-haiku-20240307
40. Anthropic Messages: anthropic/claude-3-5-sonnet-20240620
41. Anthropic Messages: anthropic/claude-3-5-sonnet-20241022
42. Anthropic Messages: anthropic/claude-3-5-sonnet-latest
43. Anthropic Messages: anthropic/claude-3-5-haiku-latest
44. Anthropic Messages: anthropic/claude-3-7-sonnet-20250219
45. Anthropic Messages: anthropic/claude-3-7-sonnet-latest
46. Anthropic Messages: anthropic/claude-opus-4-0
47. Anthropic Messages: anthropic/claude-sonnet-4-0
48. Anthropic Messages: anthropic/claude-opus-4-1-20250805
49. GeminiPro: gemini/gemini-pro
50. GeminiPro: gemini/gemini-1.5-pro-latest
51. GeminiPro: gemini/gemini-1.5-flash-latest
52. GeminiPro: gemini/gemini-1.5-pro-001
53. GeminiPro: gemini/gemini-1.5-flash-001
54. GeminiPro: gemini/gemini-1.5-pro-002
55. GeminiPro: gemini/gemini-1.5-flash-002
56. GeminiPro: gemini/gemini-1.5-flash-8b-latest
57. GeminiPro: gemini/gemini-1.5-flash-8b-001
58. GeminiPro: gemini/gemini-exp-1114
59. GeminiPro: gemini/gemini-exp-1121
60. GeminiPro: gemini/gemini-exp-1206
61. GeminiPro: gemini/gemini-2.0-flash-exp
62. GeminiPro: gemini/learnlm-1.5-pro-experimental
63. GeminiPro: gemini/gemma-3-1b-it
64. GeminiPro: gemini/gemma-3-4b-it
65. GeminiPro: gemini/gemma-3-12b-it
66. GeminiPro: gemini/gemma-3-27b-it
67. GeminiPro: gemini/gemma-3n-e4b-it
68. GeminiPro: gemini/gemini-2.0-flash-thinking-exp-1219
69. GeminiPro: gemini/gemini-2.0-flash-thinking-exp-01-21
70. GeminiPro: gemini/gemini-2.0-flash
71. GeminiPro: gemini/gemini-2.0-pro-exp-02-05
72. GeminiPro: gemini/gemini-2.0-flash-lite
73. GeminiPro: gemini/gemini-2.5-pro-exp-03-25
74. GeminiPro: gemini/gemini-2.5-pro-preview-03-25
75. GeminiPro: gemini/gemini-2.5-flash-preview-04-17
76. GeminiPro: gemini/gemini-2.5-pro-preview-05-06
77. GeminiPro: gemini/gemini-2.5-flash-preview-05-20
78. GeminiPro: gemini/gemini-2.5-pro-preview-06-05
79. GeminiPro: gemini/gemini-2.5-flash
80. GeminiPro: gemini/gemini-2.5-pro
81. GeminiPro: gemini/gemini-2.5-flash-lite
Choose a model by number (press Enter for default): 79
Enter the topic you want to file a FOIA request about: facial recognition
Do you want to narrow the search to a specific state or only federal agencies? (y/n): n
Searching for FOIA requests about: facial recognition
Found 625 requests for topic 'facial recognition'
146 successful requests found, but only sending the most recent 100 to the model for parsing…

Suggested FOIA request:

All records and materials related to facial recognition technology, including software, hardware, services, and systems, whether developed internally, procured from vendors, or accessed through agreements with other entities (e.g., other agencies, fusion centers, private companies). This includes, but is not limited to, the following:

*   **Inventory and Status:**
    *   Any records identifying the number, type, and current status (e.g., in use, pilot, testing, under consideration, discontinued) of all facial recognition technology.
    *   Documentation specifying if the technology has been purchased, developed internally, or if services are performed by outside contractors or accessed via third-party agreements.
    *   Records detailing where facial recognition technology is deployed or utilized, including but not limited to, county jails, body-worn cameras, fixed surveillance cameras, or mobile devices.

*   **Acquisition and Financial Records:**
    *   Requests for Information (RFIs), Requests for Proposals (RFPs), invitations for bids, bid responses, sole-source or limited-source justification and approval documentation, and other procurement materials.
    *   All contracts, licensing agreements, service agreements, intergovernmental service agreements, memorandums of understanding (MOUs), data sharing agreements, non-disclosure agreements, and any amendments or exhibits thereto.
    *   Purchase orders, invoices, budget allocations, funding opportunity announcements, grant applications, and grantor status/progress reports related to facial recognition technology.

*   **Policies and Operational Procedures:**
    *   All existing or proposed policies, directives, guidance documents, protocols, and Standard Operating Procedures (SOPs) governing the use, acquisition, deployment, data handling, and oversight of facial recognition technology.
    *   Records addressing permissible and prohibited activities, legal standards required for use, data storage procedures, and data retention guidelines.

*   **Training and Personnel Records:**
    *   All instructional materials, user guides, handbooks, technical manuals, presentations, videos, and certification records for any personnel authorized to operate or access facial recognition technology.
    *   Any documents or records related to training on bias in the use of facial recognition technology, accuracy, or ethical considerations.
    *   Lists, rosters, or logs of all personnel (e.g., officers, analysts, staff) who have been trained on, certified in, granted access to, or have used facial recognition technology.

*   **Usage and Performance Data:**
    *   All audit logs for facial recognition systems from [START DATE] to [END DATE, or PRESENT DATE]. If the system provides options for time period granularity, provide daily or weekly reports.
    *   All reports detailing aggregated usage/transaction statistics for facial recognition systems from [START DATE] to [END DATE, or PRESENT DATE], including (but not limited to) the number of queries, number of daily users, and number of photographs/facial templates uploaded to the database. If the system provides options for time period granularity, provide daily reports.
    *   Any documents (including screenshots of program dashboards) detailing the total number of photographs or facial templates included in the database(s) linked to facial recognition systems as of [END DATE, or PRESENT DATE].
    *   Documents sufficient to describe the source of photos or facial templates for the facial recognition databases (e.g., booking photos from this agency, booking photos from other agencies, DMV photos, publicly available images, social media).
    *   Any validation studies, accuracy reports, reliability assessments, performance evaluations, or audits (internal or external) conducted on facial recognition technology.

*   **Legal and Accountability Records:**
    *   Copies of any notices of potential legal action (e.g., intent to sue letters), formal legal complaints, or settlement documents regarding cases of alleged misidentification, false arrest, or other claims arising from the use of facial recognition technology. This should include both open and closed civil lawsuits.
    *   Any privacy impact assessments, security audits, or reports to legislative or oversight bodies concerning facial recognition technology.

*   **Technical and Marketing Information:**
    *   Technical documentation, specification documents, architecture diagrams, emails, handouts, PowerPoint presentations, advertisements, or other materials describing the function and capabilities of the facial recognition software or equipment.
    *   All marketing materials (solicited or unsolicited) acquired from vendors of facial recognition technology.
    *   Any algorithms, source code (including original source code, compiled binaries/executables, program scripts), or detailed explanations of how the software's calculations or decision-making processes work.
    *   Description of input and output data fields for the software, along with a copy of the five most recent sets of data that were used for input and the five most recent outputs of the software, in their native format (redacted for exempt information as required by law).
Would you like to file this request? (y/n): y
Enter the agency name to search: Illinois State Police

Select an agency:
1. Illinois State Police (ID 423)
Choose an agency by number: 1

Select an organization to bill the request under:
1. MuckRock Staff (ID 1)
2. sanjin (ID 24695)
3. test new muck org (ID 166692)
Choose an organization by number: 1
Enter a short title for your request: Test Request
https://www.muckrock.com/foi/multirequest/test-request-162350/

Request filed successfully!
```
