import numpy as np

class LinearFit:
    def __init__(self, A, y, w):
        """
        Least-squares for the equation A*x = y with weights w
        """
        w_diag = np.eye(len(w))*w
        covariance_matrix = np.linalg.inv(self.dotOfMatrixList([A.T, w_diag, A]))
        self.solution = self.dotOfMatrixList([
            covariance_matrix,
            A.T,
            w_diag,
            y,
            ])
        self.covariance_matrix = covariance_matrix
        self.solution_errors = np.sqrt(np.diag(covariance_matrix))
        self.y_solution = np.dot(A, self.solution)
        self.chi_squared = np.sum((self.y_solution - y)**2*w)
        self.red_chi_squared = self.chi_squared/len(y)

    @staticmethod
    def dotOfMatrixList(matrix_list):
        output = matrix_list[0]
        for m in matrix_list[1:]:
            output = np.dot(output, m)
        return output

    def error_propagation(self, gradient):
        return np.sqrt(self.dotOfMatrixList([gradient.T, self.covariance_matrix, gradient]))

