# DebtSimplifer

Debt Simplifier is a Python application designed to simplify debts within a group of individuals. It takes in a list of debts in CSV format, simplifies them, and saves the results to an AWS S3 bucket.

Features
Simplification Algorithm: Implements an algorithm to simplify debts within a group efficiently.
Integration with AWS Services: Utilizes AWS SQS for message queuing and AWS S3 for storage of input and output data.
Error Handling: Provides robust error handling mechanisms to handle exceptions gracefully.
Logging: Utilizes Python's logging module for logging informational and error messages.
Unit Tests: Includes unit tests using Pytest to ensure the correctness of the simplification algorithm.
