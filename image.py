import json
import cv2
import requests
import sys

LIMIT_PX = 1024
LIMIT_BYTE = 1024*1024  # 1MB
LIMIT_BOX = 40

rest_api_key = 'b9db889183cb0808c8ebefde50abfed6'

def kakao_ocr_resize(image):
   
    height, width, _ = image.shape

    if LIMIT_PX < height or LIMIT_PX < width:
        ratio = float(LIMIT_PX) / max(height, width)
        image = cv2.resize(image, None, fx=ratio, fy=ratio)
        height, width, _ = height, width, _ = image.shape
        

        return image
    return None


def kakao_ocr(image, appkey: str):
    
    API_URL = 'https://dapi.kakao.com/v2/vision/text/ocr'
    headers = {'Authorization': 'KakaoAK {}'.format(appkey)}
    jpeg_image = cv2.imencode(".jpg", image)[1]
    data = jpeg_image.tobytes()
    return requests.post(API_URL, headers=headers, files={"image": data})


def main(image):
   
  
    resize= kakao_ocr_resize(image)
    if resize is not None:
        image = resize
       
    output = kakao_ocr(image, rest_api_key).json()
    outputdata=json.dumps(output, sort_keys=True, indent=2, ensure_ascii=False)
    outputdata = json.loads(outputdata)
    
    text = ""
    
    for i in range(len(outputdata['result'])):
      text = text + outputdata['result'][i]['recognition_words'][0]+' '
    return text

if __name__ == "__main__":
    main()
