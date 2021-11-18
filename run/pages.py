import multiprocessing

import streamlit as st
import numpy as np
import time
import socket
import pickle

from PIL import Image


def send_to_sever(item):
    # socket 传输
    proxy_addr = "localhost"
    proxy_port = 6456
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((proxy_addr, proxy_port))
    s.send(bytes(item, encoding='utf8'))
    s.close()


# from streamlit.elements.image import image_to_url
#
# st.set_page_config(page_title="background", layout="wide")
# img_url = image_to_url('handx2.jpg', width=-3, clamp=False, channels='RGB', output_format='auto',
#                        image_id='', allow_emoji=False)
# #
# st.markdown('''
# <style>
# .css-fg4pbf{background-image:url(''' + img_url + ''');}</style>
# ''',unsafe_allow_html=True)

file_dir = './resources/upload_music.pkl'

# title
st.title(":raised_hand:Smart Gloves:raised_hand:")
st.subheader("powered by Raspberry Pi 4B")

# show details
if st.checkbox('Show details'):
    st.write(
        "该产品为类似于手上音乐喷泉的智能手套。用户将手套佩戴在手上后，可以在配套屏幕上选择歌曲。经调取云数据并进行人工智能情感分析后，会在手套上产生与该歌曲相对应的破浪式振动和灯光变化。手套上遍布大量振子和大量微型彩色灯管，其中振子会根据音乐及其情感做类似音乐喷泉式的破浪行振动变化，彩色灯管会根据人工智能情感分析的结果，随歌曲的情感变化进行灯管颜色变化。后期也可能会增添其他创新功能。")
    image = Image.open('frame.jpg')
    st.image(image, caption='hust', use_column_width=True)

st.subheader('搜索音乐')
st.write('您可以在云上音乐数据库中搜索您喜欢的歌曲')
t0 = ''
t = st.text_input('搜索音乐', '')
if not t == t0:
    pool = multiprocessing.Pool(processes=1)
    results = [pool.apply_async(send_to_sever, (t,))]
    t0 = t
    st.write('You mean ' + t + ' ?')

st.subheader('音乐上传')
st.write('您可以上传您喜欢的歌曲的文件，或者自己唱歌进行录制并上传')
uploaded_file = st.file_uploader("上传一个音乐文件", type="wav")

if uploaded_file is not None:
    # 将传入的文件转为Opencv格式
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    up_pkl = open(file_dir, 'wb')
    pickle.dump(file_bytes, up_pkl)
    up_pkl.close()
    pool = multiprocessing.Pool(processes=1)
    results = [pool.apply_async(send_to_sever, ('uploaded',))]
    # opencv_image = cv2.imdecode(file_bytes, 1)
    # 展示图片
    # st.image(opencv_image, channels="BGR")
    # 保存图片
    # cv2.imwrite('test.jpg',opencv_image)
# 然后就可以用这个图片进行一些操作了

f = open(file_dir, 'rb')
music = pickle.load(f)
f.close()

st.audio(music, format='audio/wav')

st.balloons()

with st.spinner('Wait for it...'):
    time.sleep(5)
    st.success('Done!')
