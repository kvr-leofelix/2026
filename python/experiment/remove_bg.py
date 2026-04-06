from withoutbg import WithoutBG
img=WithoutBG.opensource()
result=img.remove_background("img.jpeg")
result.save("bg.png")