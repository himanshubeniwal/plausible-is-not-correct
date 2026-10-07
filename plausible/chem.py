"""Cheminformatics checks: PubChem look-ups and (optional) RDKit validation.

LLMs are notoriously weak at SMILES: they produce strings that are not valid
molecules, or valid molecules that are not the one they name. Always parse and
compare — never paste an LLM SMILES into a pipeline unchecked.
"""
from __future__ import annotations

from urllib.parse import quote

import requests

from .http import fetch

PUG = "https://pubchem.ncbi.nlm.nih.gov/rest/pug"
# Note: in 2025 PubChem renamed its SMILES properties. "SMILES" is now the full
# (isomeric) SMILES and "ConnectivitySMILES" is the old "CanonicalSMILES".
PROPS = "MolecularFormula,MolecularWeight,SMILES,ConnectivitySMILES,InChIKey,IUPACName"

try:
    from rdkit import Chem, RDLogger
    from rdkit.Chem import Descriptors, rdMolDescriptors
    RDLogger.DisableLog("rdApp.*")
    HAVE_RDKIT = True
except ImportError:  # the demos still work through PubChem
    HAVE_RDKIT = False


def pubchem_by_name(name: str) -> dict | None:
    data = fetch(f"{PUG}/compound/name/{quote(name)}/property/{PROPS}/JSON")
    if not data:
        return None
    return data["PropertyTable"]["Properties"][0]


def pubchem_by_smiles(smiles: str) -> dict | None:
    """Look a SMILES up in PubChem (POST, so special characters are safe)."""
    try:
        data = fetch(f"{PUG}/compound/smiles/property/{PROPS}/JSON", data={"smiles": smiles})
    except requests.HTTPError:
        return None  # PubChem returns HTTP 400 for unparsable SMILES
    if not data:
        return None
    props = data["PropertyTable"]["Properties"][0]
    return props if props.get("CID") else None   # CID 0 = "valid but not in PubChem"


def rdkit_check(smiles: str) -> dict:
    """Parse a SMILES locally. Returns validity, formula, MW and InChIKey."""
    if not HAVE_RDKIT:
        return {"valid": None, "note": "RDKit not installed (pip install rdkit)"}
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return {"valid": False}
    return {
        "valid": True,
        "formula": rdMolDescriptors.CalcMolFormula(mol),
        "mol_weight": round(Descriptors.MolWt(mol), 2),
        "inchikey": Chem.MolToInchiKey(mol),
        "canonical_smiles": Chem.MolToSmiles(mol),
    }


def check_molecule_claim(name: str, smiles: str | None = None, formula: str | None = None,
                         mol_weight: float | None = None, mw_tol: float = 0.5) -> dict:
    """Compare an LLM's claims about a named compound with PubChem."""
    ref = pubchem_by_name(name)
    out = {"name": name, "pubchem_cid": ref and ref["CID"]}
    if ref is None:
        out["verdict"] = "NAME_NOT_IN_PUBCHEM"
        return out
    checks = {}
    if formula:
        checks["formula"] = "OK" if formula.replace(" ", "") == ref["MolecularFormula"] else f"WRONG (PubChem: {ref['MolecularFormula']})"
    if mol_weight is not None:
        ok = abs(float(mol_weight) - float(ref["MolecularWeight"])) <= mw_tol
        checks["mol_weight"] = "OK" if ok else f"WRONG (PubChem: {ref['MolecularWeight']})"
    if smiles:
        # Compare structures by InChIKey: identical molecules have identical keys,
        # regardless of how the SMILES string is written.
        if HAVE_RDKIT:
            parsed = rdkit_check(smiles)
            key = parsed.get("inchikey") if parsed["valid"] else None
        else:
            hit = pubchem_by_smiles(smiles)
            key = hit and hit.get("InChIKey")
        if key is None:
            checks["smiles"] = "INVALID or unparsable SMILES"
        elif key == ref["InChIKey"]:
            checks["smiles"] = "OK (same InChIKey)"
        elif key.split("-")[0] == ref["InChIKey"].split("-")[0]:
            checks["smiles"] = "SAME SKELETON, different stereo/charge (InChIKey block 1 matches)"
        else:
            checks["smiles"] = "DIFFERENT MOLECULE"
    out.update(checks)
    out["verdict"] = "ALL OK" if all(v.startswith("OK") for v in checks.values()) else "PROBLEM"
    return out
