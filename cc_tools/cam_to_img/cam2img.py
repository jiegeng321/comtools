def cam2img(img_path="./img/", img_name="img"):
    '''
    :param img_path: 保存图像路径（文件夹） 默认'./img/'
    :param img_name: 保存图像文件名前缀 默认'img'
    :return:
    '''
    cap = cv2.VideoCapture(0)  # 创建一个 VideoCapture 对象
    count = 0  # 递增，用来保存文件名
    try:
        os.makedirs(img_path)
        print("make path")
    except:
        pass
    while (cap.isOpened()):  # 循环读取每一帧
        ret_flag, Vshow = cap.read()  # 返回两个参数，第一个是bool是否正常打开，第二个是照片数组，如果只设置一个则变成一个tumple包含bool和图片
        cv2.imshow("Camera", Vshow)
        k = cv2.waitKey(1) & 0xFF  # 每帧数据延时 1ms，延时不能为 0，否则读取的结果会是静态帧
        if k == ord('s'):  # 若检测到按键 ‘s’，打印字符串
            num = ("%06d" % (count))
            cv2.imwrite(img_path + img_name + str(num) + ".jpg", Vshow)
            print(cap.get(3))  # 得到长宽
            print(cap.get(4))
            print("success to save" + str(num) + ".jpg")
            print("-------------------------")
            count += 1

        elif k == ord('q'):  # 若检测到按键 ‘q’，退出
            break
    cap.release()  # 释放摄像头
    cv2.destroyAllWindows()  # 删除建立的全部窗口
if __name__ == "__main__":

    # 测试相机获取图像 cam2img
    img_path = './img/'
    img_name = 'Live'
    cam2img(img_path, img_name)