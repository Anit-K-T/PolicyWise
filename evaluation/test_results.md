# PolicyWise – Evaluation Results

## Testing Summary

The following test cases will be used to evaluate the PolicyWise HR Policy Assistant.

| Test ID | Test Scenario | Expected Result | Actual Result | Status |
|---|---|---|---|---|
| TC01 | Annual leave entitlement | Correct policy answer with PDF citation | Pending | Not Tested |
| TC02 | Sick leave policy | Relevant information with PDF citation | Pending | Not Tested |
| TC03 | Leave application procedure | Correct procedure with source reference | Pending | Not Tested |
| TC04 | Employee notice period | Correct notice period with PDF citation | Pending | Not Tested |
| TC05 | Unsupported question | "Not specified in the provided policies." | Pending | Not Tested |

## Evaluation Criteria

1. Answer accuracy – Does the answer match the policy document?
2. Retrieval relevance – Were the correct policy sections retrieved?
3. Source citation – Are the PDF filename and page number correct?
4. Hallucination prevention – Does the system avoid unsupported answers?
5. Version handling – Does it prioritize the latest applicable policy?

## Final Evaluation

Overall result: Pending

Testing will be completed after integration of the document ingestion, retrieval and answer generation modules.