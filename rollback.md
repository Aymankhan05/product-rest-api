# Rollback Procedure

## Product REST API

### Purpose

This document describes the rollback procedure for the Product REST API deployment.

---

## 1. Identify the Failed Deployment

Check the deployment logs and identify the commit associated with the failed release.

---

## 2. Identify the Previous Stable Commit

Use Git history:

```bash
git log --oneline