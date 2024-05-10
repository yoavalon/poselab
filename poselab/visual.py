import numpy as np 
from tqdm import tqdm
from poseparser import read_model, write_model
from colorama import Fore
import vedo 

def describe(input_path) : 

    cameras, images, points3D = read_model(input_path)
    print(f'{Fore.GREEN}Imported camera poses{Fore.RESET}')

    print("num_cameras:", len(cameras))
    print("num_images:", len(images))
    print("num_points3D:", len(points3D))

def visualize(input_path) :
    """
    Visualize pose in vedo
    """ 

    cameras, images, points3D = read_model(input_path)
    print(f'{Fore.GREEN}Imported camera poses{Fore.RESET}')

    bodies = []

    cams = []
    #get camera positions
    for i in tqdm(images.keys()) :
        tvec = images[i].tvec
        qvec =images[i].qvec

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
    for feat in tqdm(points3D) : 
        feature3d = points3D[feat].xyz
        col = points3D[feat].rgb
        feats.append(feature3d)
        cols.append(col/255)

    #v_feats = vedo.Points(feats, r = 10, alpha = 0.4, c = 'blue')  #TODO with or without color to arguments
    v_feats = vedo.Points(feats, r = 10, alpha = 0.4, c = cols)
    bodies.append(v_feats)

    vedo.show(bodies)

def main():

    input_path = '/home/algo/nerf/exp30/colmap/sparse/0'
    export_path = '/home/algo/code/poselab/export'

    #visualize(input_path)
    visualize(export_path)
    

if __name__ == "__main__":
    main()           
