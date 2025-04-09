# tests/predefined_tests.py

PREDEFINED_TESTS = {
    "Homepage Load": """
Test the homepage loading of https://pyng.co.in.

Step 1: Open the website https://pyng.co.in.
- If the page loads successfully, proceed.
- Else, mark as FAILED.

Step 2: Check if the text "What are you looking for today?" is visible on the screen.
- If yes, mark step as PASSED.
- If not, mark as FAILED.

Step 3: Check if a "Login" button is visible in the top right corner. DO NOT CLICK IT, only verify the presence.
- If visible, mark step as PASSED.
- If not, mark as FAILED.

Return the pass/fail status of each step.
""",

    "Search via AI Assistant": """
Test search functionality on https://pyng.co.in.

Step 1: Open the homepage.

Step 2: Find the search input box under the text "What are you looking for today?".
- If found and clickable, mark as PASSED.
- Else, mark as FAILED.

Step 3:Enter "Tarot for career" in the chat box and press send.

Step 4: Wait up to 60 seconds for search results to appear.
- Look for cards or results showing professional names

Step 5: If at least one result card is visible (with name, description, etc), mark this step as PASSED.
- If no cards appear, mark as FAILED.

Step 6: Do NOT close the popup until result cards are confirmed to be visible.

Step 7: Return the names of the professionals shown and step-by-step PASSED/FAILED status.
""",

    "Category Navigation": """
Test navigation by clicking on category cards.

Step 1: Open https://pyng.co.in.

Step 2: Locate the category card labeled "Therapists & Counsellors".
- If found, mark as PASSED.
- Else, mark as FAILED.

Step 3: Click on the card.

Step 4: Wait for the view or page to update.

Step 5: Confirm that a new section, result, or content is visible.
- If updated content is shown, mark step as PASSED.
- Else, mark as FAILED.

Return what new content is shown and step-by-step result.
""",

    "Login Popup Flow": """
Test login popup flow on https://pyng.co.in.

Step 1: Open the homepage.

Step 2: Click the "Login" button.
- If login modal appears, mark as PASSED.
- Else, mark as FAILED.

Step 3: Type a dummy number like 1234567976 into the phone field.
- If input is accepted, mark as PASSED.
- Else, mark as FAILED.

Step 4: Click "Proceed".

Step 5: Check if the OTP entry screen appears.
- If OTP fields are visible, mark step as PASSED.
- Else, mark as FAILED.

Return a summary of these steps and whether each passed or failed.
""",

    "Bottom Search Tab": """
Test the bottom search tab functionality on https://pyng.co.in.

Step 1: Open the website https://pyng.co.in.

Step 2: Click on the "Search" icon in the bottom navigation bar.
- If it opens a new search page with a search bar, mark step as PASSED.
- Else, mark step as FAILED.

Step 3: Click into the search input box at the top of the screen.

Step 4: Type the word "decorator" and hit Enter key .
- If the query is entered and the page updates, mark as PASSED.
- Else, mark as FAILED.

Step 5: Wait up to **100 seconds** to give time for results to appear, as the search can be slow.

Step 6: Confirm that at least one result is shown under “Showing results for decorator”.
- If a card like "BE The surprise store" appears, mark step as PASSED.
- Else, mark as FAILED.

Step 7: Extract and return the list of displayed result titles (like business names or profile names).
- For each result, include name, years of experience (if shown), and number of clients (if shown).

Return step-by-step pass/fail and the extracted list of results.
"""
}
