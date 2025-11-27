#!/usr/bin/env python3
"""ssz_convert.py
Simplified SSZ-like conversion for an EL execution payload JSON.
"""
import json, sys, hashlib
from pathlib import Path

def usage():
    print("Usage: ssz_convert.py <payload.json> <out.ssz.json>")
    sys.exit(1)

if len(sys.argv) < 3:
    usage()

infile = Path(sys.argv[1])
outfile = Path(sys.argv[2])

payload = json.loads(infile.read_text())

if isinstance(payload, dict) and 'result' in payload:
    payload_obj = payload['result']
else:
    payload_obj = payload

fields = [
    'parentHash',
    'feeRecipient',
    'stateRoot',
    'receiptsRoot',
    'logsBloom',
    'prevRandao',
    'blockNumber',
    'gasUsed',
    'timestamp',
    'transactions',
    'withdrawals'
]

canonical = {}
for k in fields:
    canonical[k] = payload_obj.get(k)

field_hashes = {}
for k, v in canonical.items():
    if v is None:
        raw = b""
    else:
        raw = json.dumps(v, separators=(',', ':'), sort_keys=True).encode('utf-8')
    h = hashlib.sha256(raw).hexdigest()
    field_hashes[k] = h

concat = ''.join(field_hashes[k] for k in sorted(field_hashes.keys()))
root = hashlib.sha256(concat.encode('utf-8')).hexdigest()

ssz_like = {
    'canonical': canonical,
    'field_hashes': field_hashes,
    'ssz_like_root_sha256': root
}

outfile.write_text(json.dumps(ssz_like, indent=2))
print(f'Wrote simplified SSZ JSON to {outfile} (root: {root})')
