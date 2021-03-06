"""
Calculates RMSD metric
"""
from Bio.SVDSuperimposer import SVDSuperimposer
from helper.PDBHelper import *


class MetricsRMSD(object):

    def __init__(self):
        self.reference_coordinate = None
        self.model_coordinate = None
        self.sup = SVDSuperimposer()

    def clear(self):
        """
        clear reference_coordinate and model_coordinate
        """
        self.reference_coordinate = None
        self.model_coordinate = None

    def set(self, reference_atoms, model_atoms):
        """
        set reference_coordinate and model_coordinate

        :param reference_atoms:
        :param model_atoms:
        """
        reference_coordinate = to_vector_list(reference_atoms)
        model_coordinate = to_vector_list(model_atoms)

        if not len(reference_coordinate) == len(model_coordinate):
            raise ValueError("Reference coordinate and coordinate moving atom lists differ in size")
        elif len(reference_coordinate) == len(model_coordinate) and len(reference_coordinate) == 0:
            raise ValueError("Reference coordinate and coordinate moving atom are empty")

        self.clear()
        self.reference_coordinate = reference_coordinate
        self.model_coordinate = model_coordinate

    def run_svd(self):
        """
        run superposition
        """
        self.sup.set(self.reference_coordinate, self.model_coordinate)
        self.sup.run()
    
    def pre_calculate_rms(self):
        rotation, translation = self.sup.get_rotran()

        transformed_coordinate = numpy.dot(self.model_coordinate, rotation) + translation

        diff = transformed_coordinate - self.reference_coordinate
        return diff

    def calculate_rms(self):
        """
        :return: return rmsd value
        """
        diff = self.pre_calculate_rms()
        return numpy.sqrt(sum(sum(diff * diff)) / len(self.model_coordinate))

    def calculate_mean(self):
        rms = self.calculate_rms()
        return rms * rms

    def calculate_std(self):
        diff = self.pre_calculate_rms()
        return numpy.std(diff)
