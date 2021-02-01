import cv2
import numpy as np
from matplotlib import pyplot as plt
 
path = 'P5082909.JPG'                                               # 画像のパス
i = cv2.imread(path, 1)                                        # 画像読み込み
print(i.shape)
 
# 変換前後の対応点を設定
p_original = np.float32([[506,862], [1874,710], [1906, 1336], [3470, 902]])
p_trans = np.float32([[0, 0], [2700, 0], [0, 2700], [2700, 2700]])
print(p_original)
print(type(p_original))
print(p_trans)
print(type(p_trans))

# 変換マトリクスと射影変換
M = cv2.getPerspectiveTransform(p_original, p_trans)
i_trans = cv2.warpPerspective(i, M, (524, 478))
 
cv2.imwrite("out.jpg", i_trans)
 
#ここからグラフ設定
fig = plt.figure()
ax1 = fig.add_subplot(111)
 
# 画像をプロット
show = cv2.cvtColor(i_trans, cv2.COLOR_BGR2RGB)
ax1.imshow(show)
 
fig.tight_layout()
plt.show()
plt.close()