import numpy as np
from numpy import linalg as LA


def couplingEmittance(coup_xy,coup_xpy,coup_xyp,coup_xpyp,coup_err,gamma,solx,soly):
    '''
    This function gives back the intrinsic emittances
    '''
    sigmaMatrix = [
            [solx[0], solx[2], coup_xy, coup_xyp],
            [solx[2], solx[1], coup_xpy, coup_xpyp],
            [coup_xy, coup_xpy, soly[0], soly[2]],
            [coup_xyp, coup_xpyp, soly[2], soly[1]],
            ]

    J4 = [[0, 1, 0, 0],
        [-1, 0, 0, 0],
        [0, 0, 0, 1],
        [0, 0, -1, 0]]

    lam, x = LA.eig(np.dot(J4,sigmaMatrix)) # finds the eigenvalues
    lami1 = (lam[0]).imag # takes only the imaginary part
    lami2 = (lam[2]).imag

    intrinsicEmittance1 = abs(lami1)
    intrinsicEmittance2 = abs(lami2)
    normalizedIntrinsicEmittance1 = intrinsicEmittance1*(gamma)
    normalizedIntrinsicEmittance2 = intrinsicEmittance2*(gamma)

    return intrinsicEmittance1,intrinsicEmittance2, normalizedIntrinsicEmittance1, normalizedIntrinsicEmittance2

