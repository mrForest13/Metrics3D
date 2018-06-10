from Bio.PDB import *
import shutil


class PDBLoader(object):

    def __init__(self):
        self.pdb_list = PDBList()
        self.parser = PDBParser()
        shutil.rmtree('obsolete', ignore_errors=True)

    def retrieve_pdb_file(self, pdb_id):
        self.pdb_list.retrieve_pdb_file(pdb_id, file_format='pdb', pdir='pdb')
        shutil.rmtree('obsolete', ignore_errors=True)

    def parse_structure_by_id(self, pdb_id):
        self.retrieve_pdb_file(pdb_id)
        return self.parser.get_structure(pdb_id, 'pdb/pdb{}.ent'.format(pdb_id.lower()))

    def parse_structure_by_file(self, file_path):
        return self.parser.get_structure('pdb_id', file_path)

    def get_residue(self, pdb_path):
        """
        Get list of residues in structure for given PDB path
        :param pdb_path: path to pdb file
        :return: List of residues in structure
        """
        return list(self.parse_structure_by_file(pdb_path).get_residues())

    def get_atoms(self, pdb_path):
        """
        Get list of atoms in structure for given PDB path
        :param pdb_path: path to pdb file
        :return: List of atoms in structure
        """
        return list(self.parse_structure_by_file(pdb_path).get_atoms())

    def get_length(self, pdb_id):
        """
        Get length of given pdb structure
        :param pdb_id:
        :return: length of pdb structure
        """
        return len(self.get_residue(pdb_id))

    def get_residue_as_map(self, pdb_path):
        return {e.get_id()[1]: e for e in self.parse_structure_by_file(pdb_path).get_residues()}