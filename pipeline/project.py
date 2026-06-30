"""Projection layer: apply runtime config without mutating canonical record."""
from typing import Dict, Any


def project_record(record: Dict[str, Any], config: Dict[str, Any]) -> Dict[str, Any]:
    # shallow copy to avoid mutating canonical
    out = {}
    fields = config.get('select_fields') or list(record.keys())
    rename = config.get('rename', {})
    for f in fields:
        val = record.get(f)
        key = rename.get(f, f)
        out[key] = val
    # toggles
    if not config.get('include_provenance', True):
        out.pop('sources', None)
    if not config.get('include_confidence', True):
        out.pop('confidence', None)
    return out
