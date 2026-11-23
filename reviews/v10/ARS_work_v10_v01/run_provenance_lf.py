"""Run the ARS review_panel_provenance.py builder/validator unchanged, except that
its canonical-contract digest check reads an LF-normalised copy of
shared/contracts/reviewer/full.json.

Why: in this Windows install the plugin's full.json was checked out with CRLF
line endings (114 CRLF pairs), so its raw SHA-256 is 900290ba...b300, while the
script pins d958bc2a...e5c, which is the SHA-256 of the same bytes with LF line
endings. The plugin files are not modified; only the path the script reads for
that one check is redirected to an LF copy written next to this wrapper.
"""
import pathlib
import sys

PLUGIN = pathlib.Path(
    r"<user folder>\academic-research-skills"
    r"\academic-research-skills\3.24.3"
)
sys.path.insert(0, str(PLUGIN / "scripts"))

import review_panel_provenance as rpp  # noqa: E402

lf_copy = pathlib.Path(__file__).resolve().parent / "full_contract_LF_copy.json"
raw = (PLUGIN / "shared" / "contracts" / "reviewer" / "full.json").read_bytes()
lf_copy.write_bytes(raw.replace(b"\r\n", b"\n"))
rpp.FULL_CONTRACT_PATH = lf_copy

if __name__ == "__main__":
    sys.exit(rpp.main(sys.argv[1:]))
