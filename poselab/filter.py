import numpy as np 
from tqdm import tqdm
from poseparser import read_model, write_model
from scipy.spatial import cKDTree
from colorama import Fore
import os 

def filter_features_around(input_path, export_path, point, distance) :
    """
    Filter all features around a point
    Inputs: 
        input_path: Path of colmap binaries
        export_path: Path to export filtered pose to. If input and export identical will be overwritten
        point: 3d point to filter
        d:     distance to filter around
    Outputs:
        Binaries in export path    
    """ 

    cameras, images, points3D = read_model(input_path)
    print(f'{Fore.GREEN}Imported camera poses{Fore.RESET}')

    clean_points_3d = {}
    for feat in tqdm(points3D) : 

        feature3d = points3D[feat].xyz

        d_feat = np.linalg.norm(np.array(point)- np.array([feature3d]))

        if d_feat < distance :
            clean_points_3d[feat] = points3D[feat] 

    if not os.path.exists(export_path):
        os.makedirs(export_path)

    write_model(cameras, images, clean_points_3d, export_path)
    print(f'{Fore.GREEN}Saved model{Fore.RESET}')

def filter_features_distance_camera(input_path, export_path, distance) : 
    """
    Filter features that are more than d units away from 
    any camera

    Inputs: 
        input_path: Path of colmap binaries
        export_path: Path to export filtered pose to. If input and export identical will be overwritten
        d:     distance to filter around
    Outputs:
        Binaries in export path    
    """

    cameras, images, points3D = read_model(input_path)
    print(f'{Fore.GREEN}Imported camera poses{Fore.RESET}')

    clean_points_3d = {}

    for i in tqdm(images) : 
        tvec = images[i].tvec

        features = images[i].point3D_ids

        for feat in features : 
            if feat == -1 : 
                continue 

            feature_3d = points3D[feat].xyz

            d_feat_cam = np.linalg.norm(np.array([tvec])- np.array([feature_3d]))

            if d_feat_cam < distance :
                clean_points_3d[feat] = points3D[feat] 

    if not os.path.exists(export_path):
        os.makedirs(export_path)

    write_model(cameras, images, clean_points_3d, export_path)
    print(f'{Fore.GREEN}Saved model{Fore.RESET}')

def compute_point_densities(points, radius=1.0):
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

def filter_by_densities(input_path, export_path):
    """
    Filter features by point cloud density
    #TODO parameters to arguments
    """

    cameras, images, points3D = read_model(input_path)
    print(f'{Fore.GREEN}Imported camera poses{Fore.RESET}')

    pts = [points3D[pointIndx].xyz for pointIndx in points3D]
    densities = compute_point_densities(pts, 0.5)
    denInd = np.where(densities>20)[0].tolist()
    pts = np.array(pts)[denInd]
    densities = densities[denInd]

    clean_points_3d = {}
    for ind in tqdm(denInd) : 
        clean_points_3d[ind] = points3D[ind]   #BUG issue with indices still

    if not os.path.exists(export_path):
        os.makedirs(export_path)

    write_model(cameras, images, clean_points_3d, export_path)
    print(f'{Fore.GREEN}Saved model{Fore.RESET}')

def main():

    input_path = '/home/algo/nerf/exp30/colmap/sparse/0'
    export_path = '/home/algo/code/poselab/export'

    #filter_features_around(input_path, export_path, [0,0,0], 4)
    filter_features_distance_camera(input_path, export_path, 2)
    #filter_by_densities(input_path, export_path)

if __name__ == "__main__":
    main()           

