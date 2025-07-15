# Guide to the Project

## Task Overview
Implement two endpoints under `/profiles/` in a FastAPI application:

- **POST /profiles/**: Create a new user profile with strict field validation.
- **GET /profiles/{username}**: Retrieve a user profile by username.

All data is stored in-memory. Error handling must be consistent and centrally managed: all validation and not-found errors return structured JSON responses.

## Requirements
- **Profile Fields:**
  - `username` (alphanumeric, 3-20 chars)
  - `email` (must be a valid email address)
  - `age` (integer, 13-120)
  - `bio` (optional)

- **Validation & Error Handling:**
  - Enforce all field constraints using Pydantic and custom validation.
  - On invalid POST, respond with a custom 422 error structure (not Pydantic's default).
  - On GET, respond with a structured 404 error if the profile is missing.
  - All errors should conform to the same JSON error format.

- **Centralized Error Handling:**
  - Use FastAPI's exception handler system to return errors as unified JSON responses.

- **In-memory Storage:**
  - Store profiles in RAM using a dictionary; no external storage or databases.

- **No authentication, database, or frontend code.**

## What You Need to Do
- Implement or complete the endpoint functions and validation logic for the profiles feature as described above.
- Ensure all error and validation responses follow the format required, using centralized exception handlers.
- Do **not** add authentication, persistence, or frontend logic.

## Verifying Your Solution
- Create valid and invalid POST requests to `/profiles/` and check both success and error responses.
- Make GET requests to `/profiles/{username}` for both existing and non-existing users to confirm correct 404 handling and response structure.
- Examine error payloads to ensure all are using the same structured format.

## Notes
- The implementation should be robust, but code changes should be focused and to-the-point. Avoid overengineering.
- Read through the code, understand existing structures and handlers, and make necessary additions and corrections to achieve the required error and validation behavior.
