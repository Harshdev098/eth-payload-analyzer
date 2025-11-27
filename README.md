# eth-payload-analyzer — Rust + Python prototype

A compact prototype that fetches an Execution Layer (EL) Engine API payload, converts it into a simplified SSZ-like representation, and compares the EL JSON payload against the SSZ-derived root to surface inconsistencies.

## Running on the Terminal:

1. Start a local geth that exposes Engine API at port 8551, or point to an EL node.
2. Build and run the Rust fetcher to save payload.json
   - `cd fetcher && cargo run -- --url http://localhost:8551 --outfile ../sample_output/payload.json`
3. Run the SSZ converter:
   - `cd ../ssz_tool && python3 ssz_convert.py ../sample_output/payload.json ../sample_output/payload.ssz.json`
4. Run the comparer:
   - `python3 compare.py ../sample_output/payload.json ../sample_output/payload.ssz.json`
