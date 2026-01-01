import pdbfixer
from io import StringIO

def remove_chains_and_verify(file_content, expected_chain_ids_remaining, **kws):
    # Create a PDBFixer instance for the given pdbid
    fixer = pdbfixer.PDBFixer(pdbfile=StringIO(file_content))
    # Remove specified chains.
    fixer.removeChains(**kws)
    # Check to make sure asserted chains remain.
    chain_ids_remaining = [c.id for c in fixer.topology.chains()]
    assert expected_chain_ids_remaining == chain_ids_remaining

def test_removechain_ids(jsv_content):
    remove_chains_and_verify(jsv_content, ['B', 'D', 'A', 'C', 'B', 'A'], chainIds=[])
    remove_chains_and_verify(jsv_content, ['A', 'C', 'A'], chainIds=['B', 'D'])
    remove_chains_and_verify(jsv_content, ['B', 'D', 'B'], chainIds=['A', 'C'])
    remove_chains_and_verify(jsv_content, ['D', 'C'], chainIds=['B', 'A'])
    remove_chains_and_verify(jsv_content, [], chainIds=['B', 'D', 'A', 'C'])

def test_removechain_indices(jsv_content):
    remove_chains_and_verify(jsv_content, ['B', 'D', 'A', 'C', 'B', 'A'], chainIndices=[])
    remove_chains_and_verify(jsv_content, ['A', 'C', 'B', 'A'], chainIndices=[0, 1])
    remove_chains_and_verify(jsv_content, ['B', 'D', 'B', 'A'], chainIndices=[2, 3])
    remove_chains_and_verify(jsv_content, ['D', 'C', 'B', 'A'], chainIndices=[0, 2])
    remove_chains_and_verify(jsv_content, [], chainIndices=[0, 1, 2, 3, 4, 5])