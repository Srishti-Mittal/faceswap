try:
    import os
    import sys
    import cv2
except Exception as err:
    print(err)
    
from face_detection import select_face, select_all_faces
from face_swap import face_swap


if __name__ == '__main__':
    src_oldname = sys.argv[1]
    dst_oldname = sys.argv[2]
    
    src_newname = src_oldname+".jpeg"
    dst_newname = dst_oldname+".jpeg"

    os.rename(src_oldname,src_newname)
    os.rename(dst_oldname,dst_newname)
    
    args = {'src': src_newname,'dst':dst_newname,'out':'public/img1.jpeg','warp_2d': False, 'correct_color': False}

    # Read images
    src_img = cv2.imread(args['src'])
    dst_img = cv2.imread(args['dst'])

    print ("Select src face")
    src_points, src_shape, src_face = select_face(src_img)
    # Select dst face
    print("Before select all faces")
    dst_faceBoxes = select_all_faces(dst_img)
    print("After select all faces")

    if dst_faceBoxes is None:
        print('Detect 0 Face !!!')
        exit(-1)

    output = dst_img
    for k, dst_face in dst_faceBoxes.items():
        output = face_swap(src_face, dst_face["face"], src_points,
                           dst_face["points"], dst_face["shape"],
                           output, args)
    
    print("Writing 1st output img")
    cv2.imwrite(args['out'], output)

    print ("Select dst face")
    dst_points, dst_shape, dst_face = select_face(dst_img)
    # Select dst face

    print("select all faces src")
    src_faceBoxes = select_all_faces(src_img)

    if src_faceBoxes is None:
        print('Detect 0 Face !!!')
        exit(-1)

    output2 = src_img
    for k, src_face in src_faceBoxes.items():
        output2 = face_swap(dst_face, src_face["face"], dst_points,
                           src_face["points"], src_face["shape"],
                           output2, args)
    print("writing 2nd img")
    cv2.imwrite("public/img2.jpeg", output2)

    os.remove(src_newname)
    os.remove(dst_newname)
