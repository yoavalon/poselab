from poselab import filter, visual

def main():

    input_path = '/home/algo/nerf/exp30/colmap/sparse/0'
    export_path = '/home/algo/code/poselab/export'
    
    filter.filter_features_distance_camera(input_path, export_path, 4)
    visual.visualize(input_path)
    visual.visualize(export_path)


if __name__ == "__main__":
    main()           
