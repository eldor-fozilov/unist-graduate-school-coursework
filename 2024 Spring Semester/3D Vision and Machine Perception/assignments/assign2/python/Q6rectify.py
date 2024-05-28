import cv2
import numpy as np
import helper as hlp
import matplotlib.pyplot as plt

# Q6

class Q6:
    
    def __init__(self):


        """
        Write your own code here 

        Step 1. Load the images and the intrinsic and extrinsic parameters from '../data'.
            - im1, im2, K1, K2, R1, R2, t1, t2

        Step 2. Rectify the images with 'def rectify_pair' and save the paramters as '../data/rectify.npz'.
            - self.rectify_pair()
            - M1, M2, K1p, K2p, R1p, R2p, t1p, t2p

        Step 3. Warp the image with hlp.warpStereo().

        """

        # DO NOT CHANGE HERE!
        self.I1 = im1_rec
        self.I2 = im2_rec
        self.bb = bb
        self.M1 = M1
        self.M2 = M2
        
    
    """
    Q6 Image Rectification
        [I] K1 K2, camera matrices (3x3 matrix)
            R1 R2, rotation matrices (3x3 matrix)
            t1 t2, translation vectors (3x1 matrix)
        [O] M1 M2, rectification matrices (3x3 matrix)
            K1p K2p, rectified camera matrices (3x3 matrix)
            R1p R2p, rectified rotation matrices (3x3 matrix)
            t1p t2p, rectified translation vectors (3x1 matrix)
    """
    def rectify_pair(self, K1, K2, R1, R2, t1, t2):
        
        """
        Write your own code here 


        

        replace pass by your implementation
        """
        pass


if __name__ == "__main__":

    Q6 = Q6()

    r, c = Q6.I1.shape
    I = np.zeros((r, 2*c))
    I[:,:c] = Q6.I1
    I[:,c:] = Q6.I2

    T = np.array([[1,0,-Q6.bb[0]],[0,1,-Q6.bb[1]],[0,0,1]])
    M1_shifted = np.matmul(T, Q6.M1)
    M2_shifted = np.matmul(T, Q6.M2)

    corresp = np.load('../data/some_corresp.npz')
    pts1, pts2 = corresp['pts1'][::18].T, corresp['pts2'][::18].T
    pts1, pts2 = hlp._projtrans(M1_shifted, pts1), hlp._projtrans(M2_shifted, pts2)
    pts2[0,:] = pts2[0,:] + c

    plt.imshow(I, cmap='gray')
    plt.scatter(pts1[0,:], pts1[1,:], s=60, c='r', marker='*')
    plt.scatter(pts2[0,:], pts2[1,:], s=60, c='r', marker='*')
    for p1, p2 in zip(pts1.T, pts2.T):
        plt.plot([p1[0],p2[0]], [p1[1],p2[1]], '-', c='b')
    plt.show()
