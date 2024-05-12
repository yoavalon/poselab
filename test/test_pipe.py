from poselab import pose

def main():

    input_path = '/home/algo/nerf/exp30/colmap/sparse/0'
    export_path = '/home/algo/code/poselab/export'

    pose.load(input_path)
    pose.describe()    
    #pose.show()
    pose.save(export_path)

if __name__ == "__main__":
    main()           
