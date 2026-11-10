# WhatsApp AI Business Assistant (in progress)

## Project Overview

I am building a reusable AI-powered WhatsApp assistant for local businesses.

The goal is to help businesses answer common customer questions automatically through WhatsApp. Customers should be able to ask questions in English, Malayalam, or Manglish and receive answers based on the business's own information.

## What I Am Trying to Build

The assistant should be able to:

- Answer questions about products, services, and their prices.
- Provide information about available discounts and offers.
- Share important dates and schedules.
- Answer questions about business rules, policies, and frequently asked questions.
- Provide business contact information.
- Direct customers to contact the business when the requested information is unavailable.

## How It Should Work

1. A customer sends a message through WhatsApp.
2. The system identifies what the customer is asking.
3. It searches the business's structured records or information documents.
4. It prepares an answer using the information it finds.
5. If the information is unavailable or uncertain, it asks the customer to contact the business instead of inventing an answer.

## Information Sources

Each business will have its own information, such as:

- Product or service records and prices.
- Discount records and validity dates.
- Business details and contact information.
- Documents containing rules, policies, FAQs, and other information.

Structured information will be handled using Python. Longer documents will be processed, divided into smaller sections, and searched using a retrieval system (RAG).

## Main Development Principles

- Answers must be based on business-approved information.
- The assistant must never invent prices, dates, discounts, or policies.
- Expired discounts must not be presented as active offers.
- If information cannot be found, the assistant must provide a safe fallback.
- Each business must have its own separate information.
- Customer messages may contain English, Malayalam, or Manglish.

## Development Approach

I am developing the project step by step while learning the underlying software engineering concepts.

The initial development will happen locally, using fictional business information for testing.

The planned development stages are:

1. Extract information from business documents.
2. Build structured lookup functions for products, services, prices, and discounts.
3. Divide longer documents into searchable sections.
4. Implement embeddings and semantic retrieval.
5. Connect retrieval results to an AI model for answer generation.
6. Test answers for accuracy, including Malayalam and Manglish questions.
7. Build the backend and connect it to the WhatsApp API.

## Current Goal

The immediate goal is to build a working prototype using fictional business information.

Once the prototype works reliably, the same system should be adaptable to different local businesses by loading their own business information.
