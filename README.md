# Bhu-Lok: Blockchain Land Registry System

## Overview

Bhu-Lok is a blockchain-based land registry and property ownership management system developed to demonstrate how blockchain technology can improve transparency, security, and trust in real estate transactions.

The project was inspired by a parliamentary discussion by Rajya Sabha Member of Parliament Raghav Chadha on the digitization of land records and the need for technology-driven reforms in property management. The discussion highlighted challenges such as property fraud, ownership disputes, document tampering, and inefficient record-keeping systems.

Bhu-Lok explores how blockchain can be used to create a tamper-resistant and transparent property registry system.

## Problem Statement

Traditional land registration systems often face issues such as:

* Fake ownership claims
* Property fraud
* Duplicate property sales
* Manual verification processes
* Document tampering
* Lack of transparency in ownership records

These challenges can result in legal disputes, delays, and loss of trust in property transactions.

## Proposed Solution

Bhu-Lok uses blockchain principles to maintain a secure and immutable record of property ownership transfers.

Each ownership transaction is stored as a block containing:

* Property information
* Owner details
* Transaction value
* Timestamp
* Previous block hash
* Current block hash

Because each block is linked to the previous block through cryptographic hashes, unauthorized modifications can be detected immediately.

## Key Features

### Blockchain-Based Property Registry

Maintains a chain of ownership records for every property.

### Ownership History Tracking

Provides complete visibility into previous and current property owners.

### Blockchain Validation

Verifies whether the ownership chain remains intact and untampered.

### Tampering Detection

Detects modifications to historical records and insertion of fraudulent blocks.

### Smart Contract Simulation

Allows ownership transfer only when predefined verification conditions are satisfied.

### Role-Based Access Control

Supports:

* Government Officer
* Buyer
* Seller

### Fraud Detection

Identifies suspicious ownership transfer patterns.

### Property Search

Enables users to search and analyze registered properties.

### Real Dataset Integration

Uses real-world real estate and transaction datasets to simulate practical property registration scenarios.

## Technology Stack

* Python
* Streamlit
* Pandas
* SHA-256 Hashing
* Blockchain Concepts
* CSV Datasets

## Project Workflow

1. Load property and transaction datasets
2. Create genesis blocks for registered properties
3. Generate ownership transfer blocks
4. Link blocks using cryptographic hashes
5. Validate blockchain integrity
6. Detect tampering attempts
7. Display ownership history and analytics

## Future Scope

* Integration with government land record databases
* Aadhaar-based identity verification
* Digital signatures
* Smart contract automation
* IPFS decentralized document storage
* AI-based fraud prediction

## Disclaimer

This project is an academic and hackathon prototype created for educational purposes. It demonstrates how blockchain technology can be applied to land registry systems and is not connected to any official government land registration platform.

## Inspiration

The idea for Bhu-Lok was inspired by discussions on the digitization and modernization of land records highlighted in parliamentary debates by Raghav Chadha. The project explores a technical approach to addressing land registry challenges through blockchain-based record management and ownership verification.
