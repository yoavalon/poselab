import numpy as np 
from tqdm import tqdm
from posefilter.poseparser import read_model, write_model

def filter_features(input_path, export_path, point, distance) :
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

    clean_points_3d = {}
    for i in tqdm(images) : 
        pass 

        #TODO complete function


def filter_distant_features(cameras, images, points3D, d) : 
    """
    Filter features that are more than d units away from 
    any camera

    Keep in mind that cameras can also be wrong!!
    """

    clean_points_3d = {}

    for i in tqdm(images) : 
        tvec = images[i].tvec

        features = images[i].point3D_ids

        for feat in features : 
            if feat == -1 : 
                continue 

            feature_3d = points3D[feat].xyz

            d_feat_cam = np.linalg.norm(np.array([tvec])- np.array([feature_3d]))

            if d_feat_cam < d :
                clean_points_3d[feat] = points3D[feat] 

    return cameras, images, clean_points_3d

cameras, images, clean_points_3d = filter_distant_features(cameras, images, points3D, 6)

write_model(cameras, images, clean_points_3d, export_path)
print('done')