#!/usr/bin/env python3
"""compare.py
Compare fields between the original EL payload JSON and the SSZ-like JSON.
"""
import json, sys
from pathlib import Path

def usage():
    print("Usage: compare.py <payload.json> <payload.ssz.json>")
    sys.exit(1)

if len(sys.argv) < 3:
    usage()

payload = json.loads(Path(sys.argv[1]).read_text())
ssz = json.loads(Path(sys.argv[2]).read_text())

if isinstance(payload, dict) and 'result' in payload:
    payload_obj = payload['result']
else:
    payload_obj = payload

canonical = ssz.get('canonical', {})
field_hashes = ssz.get('field_hashes', {})

mismatches = []
for k in canonical.keys():
    el_val = payload_obj.get(k)
    ssz_val = canonical.get(k)
    if el_val != ssz_val:
        mismatches.append((k, el_val, ssz_val))

if not mismatches:
    print('All canonical fields match between EL JSON and SSZ-like canonicalization.')
else:
    print(f'Found {len(mismatches)} mismatched fields:')
    for k, el_v, ssz_v in mismatches:
        print('---')
        print(f'Field: {k}')
        print('EL value:')
        print(json.dumps(el_v, indent=2))
        print('SSZ canonicalized value:')
        print(json.dumps(ssz_v, indent=2))

    print('\nNote: This is a simplified canonicalization + comparison. For production-level\nSSZ/HashTreeRoot comparisons, use the official consensus libraries or spec tests.')
