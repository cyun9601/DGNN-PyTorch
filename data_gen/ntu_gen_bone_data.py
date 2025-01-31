import os
import numpy as np
from numpy.lib.format import open_memmap

from tqdm import tqdm

# Joint 연관 관계
paris = {
    'ntu/xview': [
        (1, 2), (2, 21), (3, 21), (4, 3), (5, 21),
        (6, 5), (7, 6), (8, 7), (9, 21), (10, 9),
        (11, 10), (12, 11), (13, 1), (14, 13), (15, 14),
        (16, 15), (17, 1), (18, 17), (19, 18), (20, 19),
        (22, 23), (21, 21), (23, 8), (24, 25), (25, 12)
    ],
    
    'ntu/xsub': [
        (1, 2), (2, 21), (3, 21), (4, 3), (5, 21),
        (6, 5), (7, 6), (8, 7), (9, 21), (10, 9),
        (11, 10), (12, 11), (13, 1), (14, 13), (15, 14),
        (16, 15), (17, 1), (18, 17), (19, 18), (20, 19),
        (22, 23), (21, 21), (23, 8), (24, 25), (25, 12)
    ],

    'kinetics': [
        (0, 0), (1, 0), (2, 1), (3, 2), (4, 3), (5, 1),
        (6, 5), (7, 6), (8, 2), (9, 8), (10, 9), (11, 5),
        (12, 11), (13, 12), (14, 0), (15, 0), (16, 14), (17, 15)
    ]
}

sets = {'train', 'val'}
datasets = {'ntu/xview', 'ntu/xsub'}

def gen_bone_data():
    """Generate bone data from joint data for NTU skeleton dataset"""
    for dataset in datasets: # 'ntu/xview', 'ntu/xsub'
        for set in sets: # 'train', 'val'
            print(dataset, set)
            
            # 앞에서 생성한 Joint data Load
            data = np.load('./data/{}/{}_data_joint.npy'.format(dataset, set))
            N, C, T, V, M = data.shape # channels (C), frames (T), nodes (V), persons (M)
            
            # Bone 데이터 저장할 파일 생성. Joint 데이터와 Shape를 같게.
            fp_sp = open_memmap(
                './data/{}/{}_data_bone.npy'.format(dataset, set),
                dtype='float32',
                mode='w+',
                shape=(N, 3, T, V, M))
            
            # Joint data를 fp_sp에 복사 
            fp_sp[:, :C, :, :, :] = data # Deep copy
        
            for v1, v2 in tqdm(paris[dataset]): # dataset : 'ntu/xview', 'ntu/xsub'
                # Reduce class index for NTU datasets
                
                # Joint 번호는 1부터 시작하지만, 인덱스는 0부터 시작하기 때문
                if dataset != 'kinetics':
                    v1 -= 1
                    v2 -= 1
                    
                # Assign bones to be joint1 - joint2, the pairs are pre-determined and hardcoded
                # There also happens to be 25 bones
                fp_sp[:, :, :, v1, :] = data[:, :, :, v1, :] - data[:, :, :, v2, :]


if __name__ == '__main__':
    gen_bone_data()