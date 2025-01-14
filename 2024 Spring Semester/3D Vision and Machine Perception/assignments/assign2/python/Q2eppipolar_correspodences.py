import numpy as np
import helper as hlp
import matplotlib.pyplot as plt
from Q1eight_point import Q1

# Q2

class Q2(Q1):
    def __init__(self):
        super(Q2, self).__init__()

        """
        Write your own code here 

        Step 1. Load points in image 1 from data/temple_coords.npz
            - pts1 

        Step 2. Run epipolar_correspondences to get points in image 2
            - pts2 = self.epipolar_correspondences(self.im1, self.im2, self.F, pts1)

        """
        
        pts1 = np.load('../data/temple_coords.npz')['pts1']
        pts2 = self.epipolar_correspondences(self.im1, self.im2, self.F, pts1)
        
        # DO NOT CHANGE HERE!
        self.pts1 = pts1
        self.pts2 = pts2

    """
    Q2 Epipolar Correspondences
        [I] im1, image 1 (H1xW1 matrix)
            im2, image 2 (H2xW2 matrix)
            F, fundamental matrix from image 1 to image 2 (3x3 matrix)
            pts1, points in image 1 (Nx2 matrix)
        [O] pts2, points in image 2 (Nx2 matrix)
    """
    def epipolar_correspondences(self, im1, im2, F, pts1):
        """
        Write your own code here 
        """
        pts2 = np.zeros_like(pts1)
        
        # Convert to homogeneous coordinates
        pts1 = np.hstack((pts1, np.ones((pts1.shape[0], 1))))
        
        window_size = 10
        H, W = im1.shape[:2]
        N = pts1.shape[0]
        
        for i in range(N):
            u = pts1[i] # homogeneous coordinates of the point in image 1
            u = u.astype(int)
            line_coeff = F @ u
            a, b, c = line_coeff
          
            # Choose candidate points in the epipolar line
            
            if b == 0:
                y = np.arange(H)
                x = (-c - b * y) / a
                mask = (x >= 0) & (x < W)
            else:
                x = np.arange(W)
                y = (-a * x - c) / b
                mask = (y >= 0) & (y < H)
            
            x = x[mask].astype(int)
            y = y[mask].astype(int)
       
            # Compute the distance between the point in image 1 and the candidate points
            source_patch = im1[u[1] - window_size : u[1] + window_size,
                                         u[0] - window_size: u[0] + window_size]
            distances = np.zeros_like(x).astype(float)           
            for j in range(len(x)):
                
                x_candidate_idx = x[j]
                y_candidate_idx = y[j]
                                
                # Compute the sum of squared differences
                candidate_patch = im2[y_candidate_idx - window_size : y_candidate_idx + window_size,
                                         x_candidate_idx - window_size : x_candidate_idx + window_size]
                
                if candidate_patch.shape != source_patch.shape:
                    distances[j] = np.inf
                    continue
                
                distances[j] = np.sum((source_patch - candidate_patch)**2) # Euclidean distance
            
            # choose the point with the smallest distance
            idx = np.argmin(distances)
            pts2[i] = [x[idx], y[idx]]
             
            
        return pts2

    def epipolarMatchGUI(self, I1, I2, F):
        sy, sx, sd = I2.shape
        f, [ax1, ax2] = plt.subplots(1, 2, figsize=(12, 9))
        ax1.imshow(I1)
        ax1.set_title('Select a point in this image')
        ax1.set_axis_off()
        ax2.imshow(I2)
        ax2.set_title('Verify that the corresponding point \n is on the epipolar line in this image')
        ax2.set_axis_off()
        while True:
            plt.sca(ax1)
            x, y = plt.ginput(1, mouse_stop=2)[0]
            xc, yc = int(x), int(y)
            v = np.array([[xc], [yc], [1]])
            l = F @ v
            s = np.sqrt(l[0]**2+l[1]**2)
            if s==0:
                hlp.error('Zero line vector in displayEpipolar')
            l = l / s
            if l[0] != 0:
                xs = 0
                xe = sx - 1
                ys = -(l[0] * xs + l[2]) / l[1]
                ye = -(l[0] * xe + l[2]) / l[1]
            else:
                ys = 0
                ye = sy - 1
                xs = -(l[1] * ys + l[2]) / l[0]
                xe = -(l[1] * ye + l[2]) / l[0]
            ax1.plot(x, y, '*', markersize=6, linewidth=2)
            ax2.plot([xs, xe], [ys, ye], linewidth=2)
            # draw points
            pc = np.array([[xc, yc]])
            p2 = self.epipolar_correspondences(I1, I2, F, pc)
            ax2.plot(p2[0,0], p2[0,1], 'ro', markersize=8, linewidth=2)
            plt.draw()



if __name__ == "__main__":

    Q2 = Q2()
    Q2.epipolarMatchGUI(Q2.im1, Q2.im2, Q2.F)



