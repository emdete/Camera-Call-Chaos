import torch


model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)


def analyseImage(image, **argv):
    imgs = [image] 
    results = model(imgs)
    test = results.pandas().xyxy[0]
    test2 = results.xyxy[0]
    res = 0.0
    for i2 in test2:
        res = float(i2[4])
    if results.names[0] == "person" and res >= 0.5:
        return True
    else:
        return False

    
