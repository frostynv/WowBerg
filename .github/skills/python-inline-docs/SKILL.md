---
name: python-inline-docs
description: Inline documentation skill for the Fullstack Agent. Use when generating or modifying Python code that needs Google-style docstrings, short import and variable comments, and concise method summaries.
---

Use this skill for Python documentation-focused generation or editing.

Rules
- Use Google-style docstrings for modules, classes, and functions/methods.
- Class docstrings must include a short description, a Contract or Responsibility paragraph, and a Methods section listing each method with a one-line responsibility bullet.
- Add a short comment on the preceding line explaining why a new dependency is introduced.
- Place short usage comments on the preceding line for newly introduced module-level or function-local variables that are not self-evident.
- Under Methods:, list each public method with a hyphen and a one-line description of responsibility.
- Minimize inline comments elsewhere.
- Do not inject these rules into unrelated conversations or files.

Examples

Module example
```python
"""Utilities for processing example data.

This module demonstrates the documentation style used by this skill.
"""

# HTTP client for example requests
import requests

# cached result for repeated lookups
cached_value = None
```

Class example
```python
class ClassA:
	"""Example processor for sample input.

	Contract:
	- Construct with input_name and retry_count.
	- Exposes process_data() to return a normalized payload.

	Methods:
	- __init__(self, input_name, retry_count): store configuration.
	- process_data(self, payload): normalize the payload.
	- reset_cache(self): clear cached state.
	"""

	def __init__(self, input_name: str, retry_count: int) -> None:
		"""Initialize the processor.

		Args:
			input_name (str): Name of the input source.
			retry_count (int): Number of retry attempts.
		"""
		self.input_name = input_name
		self.retry_count = retry_count

	def process_data(self, payload: dict) -> dict:
		"""Normalize a payload.

		Args:
			payload (dict): Raw payload to normalize.

		Returns:
			dict: Normalized payload.
		"""
		return payload

	def reset_cache(self) -> None:
		"""Clear cached state.

		Returns:
			None: This method has no return value.
		"""
		return None
```

Function example
```python
def transform_record(record: dict) -> dict:
	"""Transform a record into the target shape.

	Args:
		record (dict): Input record.

	Returns:
		dict: Transformed record.
	"""
	return record
```
