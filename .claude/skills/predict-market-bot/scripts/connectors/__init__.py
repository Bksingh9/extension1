"""Data connectors for prediction-market platforms.

No prediction-market MCP connector is assumed available; these are direct REST
connectors the operator runs with their own credentials. Each degrades to an
empty result on any failure so the pipeline never crashes offline.
"""
