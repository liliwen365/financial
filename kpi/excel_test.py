from django.shortcuts import render, redirect
from django.core.files.uploadedfile import InMemoryUploadedFile
from io import BytesIO



def decrypt(request):
    """解密文件"""
    if request.method == "GET":
        return render(request, "kpi/decrypt.html")
    else:
        # 获取文件
        pic = request.FILES["pic"]
        print(type(pic))
        # 创建一个文件
        # save_path = "%s/booktest/%s" % (settings.MEDIA_ROOT, pic.name)
        save_path = "E:/不常用工作/已解密文件/%s" % pic.name
        with open(save_path, "wb") as f:
            # 获取上传文件的内容并写入打开的文件
            for content in pic.chunks():
                f.write(content)
        # 复制一份文件放入桌面
        save_path_desktop = "C:/Users/931304/Desktop/已解密文件/%s" % pic.name
        with open(save_path_desktop, "wb") as f:
            for content in pic.chunks():
                f.write(content)
        # 返回
        return redirect("/decrypt")


pic_io = BytesIO(b"C:/Users/931304/Desktop")
pic = InMemoryUploadedFile(file=pic_io, field_name="pic", name="wenjian.xlsx", content_type=None, size=11854, charset=None)


save_path = "E:/不常用工作/已解密文件/wenjian.xlsx"
with open(save_path, "wb") as f:
    # 获取上传文件的内容并写入打开的文件
    for content in pic.chunks():
        f.write(content)








