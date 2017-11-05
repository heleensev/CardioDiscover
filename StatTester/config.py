
# class containing info from meta data file as attributes
class study:

    def __init__(self, studyID, study_path, study_size):
        self.studyID = studyID
        self.study_path = study_path
        self.study_size = study_size
        self.study_lambda = float
        self.study_correction = float
        self.study_sum_eff = float

    def set_lambda(self, lb):
        self.study_lambda = lb

    def set_correction(self, cor):
        self.study_correction = cor

    def set_sum_eff(self, eff):
        self.study_sum_eff = eff
