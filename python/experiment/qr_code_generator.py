import qrcode
url="enter the url"
img=qrcode.make("https://www.amazon.in/?&tag=googhydrabk1-21&ref=pd_sl_5szpgfto9i_e&adgrpid=155259813593&hvpone=&hvptwo=&hvadid=674893540034&hvpos=&hvnetw=g&hvrand=4340125976810266176&hvqmt=e&hvdev=c&hvdvcmdl=&hvlocint=&hvlocphy=9050480&hvtargid=kwd-64107830&hydadcr=14452_2316413&gad_source=1")
img.save("qrcode.png")
print("qr generated")
