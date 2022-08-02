# 批量txt生成词云，保持在png子目录下，生成png文件，文件大小为600*600*4倍，默认字体宋黑
import jieba
from wordcloud import WordCloud
import os
import tkinter as tk
from tkinter import messagebox
from tkinter.filedialog import askdirectory
from tkinter.filedialog import askopenfilename


def stopwordslist(stopfile):
    stopwords = [line.strip() for line in open(
        stopfile, encoding='UTF-8').readlines()]
    return stopwords


def chinese_jieba(userdictfile, stopfile, text):
    if userdictfile:
        jieba.load_userdict(userdictfile)
    wordlist = jieba.cut(text, HMM=True)
    if stopfile:
        stopwords = stopwordslist(stopfile)
    else:
        stopwords = []
    outstr = ''
    # 去停用词
    for word in wordlist:
        if word not in stopwords:
            if word != '\t':
                outstr += word
                outstr += "."
    #wordlist_for_cy = " ".join(wordlist)
    return outstr


def ciyun(txt_files_path, txtfile, png_output_path, stopfile, userdict, font):
    filefullname = os.path.join(txt_files_path, txtfile)
    #backgroud_Image = np.array(Image.open('mask.png'))
    with open(filefullname, encoding="utf-8")as file:
        text = file.read()
        text = chinese_jieba(userdict, stopfile, text)
        wordcloud = WordCloud(font_path=font,
                              background_color="white", width=600, scale=4,
                              height=600, max_words=200, min_font_size=8, contour_color='steelblue').generate(text)
        pngfile = os.path.splitext(txtfile)[0]+'.png'
        pngfullfile = os.path.join(png_output_path, pngfile)
        print("\""+pngfullfile+"\""+"    writing")
        wordcloud.to_file(pngfullfile)
        print("\"" + pngfullfile + "\"" + "    written")
    return


#####################GUI#################
def go(txt_files_path, png_output_path, stopfile, userdict):
    txt_files_path = txt_files_path.get()
    png_output_path = png_output_path.get()
    stopfile = stopfile.get()
    userdict = userdict.get()

    param_flag = 1
    if not txt_files_path:
        param_flag = 0
        messagebox.showinfo(
            '提示', '请输入正确txt文件目录路径,Please choose the right txtfile path !')
    if not png_output_path:
        param_flag = 0
        messagebox.showinfo(
            '提示', '请输入正确的png图片文件输出路径,Please choose the right png output path !')

    if param_flag:
        font = "simhei.ttf"
        with os.scandir(txt_files_path) as txt_file_list:
            for item in txt_file_list:
                if item.is_file() and item.name.endswith(".txt"):
                    txtfile = item.name
                    ciyun(txt_files_path, txtfile,
                          png_output_path, stopfile, userdict, font)
        messagebox.showinfo('提示', '任务已完成 !')
        os.startfile(png_output_path)


def selectpath(path):
    path_ = askdirectory()
    path.set(path_)


def selectfile(file):
    file_ = askopenfilename()
    file.set(file_)


def main():

    window = tk.Tk()
    window.title("PNG图片词云文件生成工具")

    txt_files_path = tk.StringVar()
    png_output_path = tk.StringVar()
    stopfile = tk.StringVar()
    userdict = tk.StringVar()

    frame1 = tk.Frame(window, highlightbackground="blue", highlightthickness=1)
    frame2 = tk.Frame(window, highlightbackground="blue", highlightthickness=1)
    frame3 = tk.Frame(window, highlightbackground="blue", highlightthickness=1)
    frame4 = tk.Frame(window, highlightbackground="blue", highlightthickness=1)
    frame5 = tk.Frame(window, highlightbackground="blue", highlightthickness=1)
    frame6 = tk.Frame(window, highlightbackground="blue", highlightthickness=1)

    entry_txt_path = tk.Entry(frame1, textvariable=txt_files_path,
                              state=tk.DISABLED, width=60)
    button_txt_path = tk.Button(
        frame1, text="TXT 文件 所在文件夹选择", command=lambda: selectpath(txt_files_path))

    entry_png_path = tk.Entry(frame2, textvariable=png_output_path,
                              state=tk.DISABLED, width=60)
    button_png_path = tk.Button(frame2, text="PNG图片输出文件夹选择", command=lambda: selectpath(
        png_output_path))

    entry_stopfile_path = tk.Entry(frame3, textvariable=stopfile,
                                   state=tk.DISABLED, width=60)
    button_stopfile_path = tk.Button(frame3, text="stop词语文件选择（可选）", command=lambda: selectfile(
        stopfile))

    entry_userdict_path = tk.Entry(frame4, textvariable=userdict,
                                   state=tk.DISABLED, width=60)
    button_userdict_path = tk.Button(frame4, text="用户字典文件选择（可选）", command=lambda: selectfile(
        userdict))

    button_confirm = tk.Button(
        frame5, text="确定 Go", command=lambda: go(txt_files_path, png_output_path, stopfile, userdict))

    #
    entry_txt_path.pack()
    button_txt_path.pack()

    #
    entry_png_path.pack()
    button_png_path.pack()

    #
    entry_stopfile_path.pack()
    button_stopfile_path.pack()

    #
    entry_userdict_path.pack()
    button_userdict_path.pack()

    button_confirm.pack()

    frame1.pack(padx=10, pady=10)
    frame2.pack(padx=10, pady=10)
    frame3.pack(padx=10, pady=10)
    frame4.pack(padx=10, pady=10)
    frame5.pack(padx=10, pady=10)
    frame6.pack(padx=10, pady=10)
    window.mainloop()


if __name__ == '__main__':
    main()
