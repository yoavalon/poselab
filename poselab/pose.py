from colorama import Fore
from poselab.poseparser import read_model, write_model
import vedo
from tqdm import tqdm
import numpy as np 
import os 

class Pose() : 

    def __init__(self) : 
        """
        Init objects
        """
        
        self.cameras = None 
        self.images = None 
        self.points3D = None 

    def load(self, input_path) : 
        """
        Load pose from colmap bin path
        """

        cameras, images, points3D = read_model(input_path)

        self.cameras = cameras 
        self.images = images 
        self.points3D = points3D

        print(f'{Fore.GREEN}Loaded pose binaries from: {input_path} {Fore.RESET}')

    def save(self, export_path) : 
        """
        Save poses to export path
        """

        if not os.path.exists(export_path):
            os.makedirs(export_path)

        write_model(self.cameras, self.images, self.points3D, export_path)

        print(f'{Fore.GREEN}Saved poses to: {export_path} {Fore.RESET}')

    def clear(self) : 
        """
        Clear current pose
        """

        self.cameras = None 
        self.images = None 
        self.points3D = None 

    def describe(self) : 
        """
        Describe current model
        """

        print("num_cameras:", len(self.cameras))
        print("num_images:", len(self.images))
        print("num_points3D:", len(self.points3D))

    def show(self, color = True) :
        """
        Visualize pose in vedo
        Inputs: 
            color: default True, slower than without
        """ 

        bodies = []

        cams = []
        #get camera positions
        for i in tqdm(self.images.keys()) :
            tvec = self.images[i].tvec
            qvec =self.images[i].qvec

            w, x, y, z = qvec               
            rotation_matrix = np.array([
                [1 - 2*y*y - 2*z*z, 2*x*y - 2*w*z, 2*x*z + 2*w*y],
                [2*x*y + 2*w*z, 1 - 2*x*x - 2*z*z, 2*y*z - 2*w*x],
                [2*x*z - 2*w*y, 2*y*z + 2*w*x, 1 - 2*x*x - 2*y*y]
            ])
        
            cam_pos = np.dot(-rotation_matrix.T,tvec) 
            cams.append(cam_pos)

        v_cams = vedo.Points(cams, r = 20, alpha = 0.5, c = 'red')
        bodies.append(v_cams)

        feats = []
        cols = []
        #get 3d features
        for feat in tqdm(self.points3D) : 
            feature3d = self.points3D[feat].xyz
            col = self.points3D[feat].rgb
            feats.append(feature3d)
            cols.append(col/255)

        if color : 
            v_feats = vedo.Points(feats, r = 10, alpha = 0.4, c = cols)
            bodies.append(v_feats)
        else : 
            v_feats = vedo.Points(feats, r = 10, alpha = 0.4, c = 'blue')
            bodies.append(v_feats)


        vedo.show(bodies)

pose = Pose()

print("test")

#input_path = '/home/algo/nerf/exp30/colmap/sparse/0'