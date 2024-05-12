from colorama import Fore
from poselab.poseparser import read_model, write_model
import vedo
from scipy.spatial import cKDTree
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


        vedo.show(bodies).close()


    def filter_features_around(self, point, distance) :
        """
        Filter all features around a point
        Inputs: 
            point: 3d point to filter
            d:     distance to filter around
        Outputs:
            Binaries in export path    
        """ 

        clean_points_3d = {}
        for feat in tqdm(self.points3D) : 

            feature3d = self.points3D[feat].xyz

            d_feat = np.linalg.norm(np.array(point)- np.array([feature3d]))

            if d_feat < distance :
                clean_points_3d[feat] = self.points3D[feat] 

        #overwrite features
        self.points3D = clean_points_3d

    def filter_features_distance_camera(self, distance) : 
        """
        Filter features that are more than d units away from 
        any camera

        Inputs: 
            distance:     distance to filter around
        """

        clean_points_3d = {}

        for i in tqdm(self.images) : 
            tvec = self.images[i].tvec

            features = self.images[i].point3D_ids

            for feat in features : 
                if feat == -1 : 
                    continue 

                feature_3d = self.points3D[feat].xyz

                d_feat_cam = np.linalg.norm(np.array([tvec])- np.array([feature_3d]))

                if d_feat_cam < distance :
                    clean_points_3d[feat] = self.points3D[feat] 

        #overwrite points 
        self.points3D = clean_points_3d

    def compute_point_densities(self, points, radius=1.0):
        """
        Compute feature point cloud densities using a KDTree for nnsearch
        """

        # Create a KDTree for efficient nearest neighbor search
        tree = cKDTree(points)

        # Compute the density for each point
        densities = np.zeros(len(points))
        for i, point in tqdm(enumerate(points)):
            # Find points within the specified radius
            indices = tree.query_ball_point(point, radius)
            # The density is the number of points in the radius
            densities[i] = len(indices)

        return densities

    def filter_by_densities(self):
        """
        Filter features by point cloud density
        #TODO parameters to arguments
        """

        print('not fully implemente yet')

        pts = [self.points3D[pointIndx].xyz for pointIndx in self.points3D]
        densities = self.compute_point_densities(pts, 0.5)
        denInd = np.where(densities>20)[0].tolist()
        pts = np.array(pts)[denInd]
        densities = densities[denInd]

        clean_points_3d = {}
        for ind in tqdm(denInd) : 
            clean_points_3d[ind] = self.points3D[ind]   #BUG issue with indices still

pose = Pose()

print("test")

#input_path = '/home/algo/nerf/exp30/colmap/sparse/0'