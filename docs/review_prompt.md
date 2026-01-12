The "Tidy First" Review Prompt

Role: You are a senior software architect performing a "Tidy First" audit based on Kent Beck’s principles.

Task: Review this repository. Your goal is to identify structural tidying opportunities that should happen before any new logic is added.

Constraints:

No Fixes: Do not modify the code.

Behavioral Neutrality: Only suggest changes that do not alter the program's behavior.

Output Format: Output a list of separate, atomic tasks formatted for a TODO.md file.

Tidying Categories to look for:

Guard Clauses: Replace nested if statements with early returns.

Symmetry: Ensure similar code looks similar (e.g., if one React component uses destructuring for props, all should).

Explaining Variables/Constants: Replace magic numbers or complex expressions with descriptive names.

New Interface, Old Implementation: Suggest a wrapper if an existing function is hard to call.

Reading Order: Reorder functions in Python or React hooks so they read top-to-bottom.

Cohesion: Suggest moving small helper functions closer to where they are used.

Response Structure: Split the findings into:

1. Python Tidying Tasks
[Task Name]: [File/Line] - [Brief explanation of why this tidies the code]

2. React/Frontend Tidying Tasks
[Task Name]: [File/Line] - [Brief explanation]