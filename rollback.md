# Rollback Documentation

## Project

Product REST API

## Purpose

This document describes the rollback procedure for the deployed
Product REST API.

## Version History

### Version 1.0.0

Initial stable release containing:

- Product creation
- Product listing
- Product retrieval
- Product update
- Product partial update
- Product deletion
- Request validation
- HTTP status codes
- SQLite database
- API documentation
- Health check

## Rollback Strategy

The project uses Git for version control.

If a newly deployed version causes problems, the previous stable
Git commit can be restored and redeployed.

### Rollback Commands

```bash
git log --oneline