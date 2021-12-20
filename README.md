# calibration-and-pose-estimation

체스보드를 다양한 각도로 20장 촬영 후 카메라 calibration을 수행 후 Aruco marker 기반 pose estimation을 수행한 것입니다.


# calibration

<사전 측정>

![image](https://user-images.githubusercontent.com/63800086/146789942-fd2b48bf-a613-4caa-a576-a9e3225b2330.png)


<2d 코너 찾기>

![image](https://user-images.githubusercontent.com/63800086/146789966-fb50fbe6-918c-4819-b0df-61be22c336a0.png)

![image](https://user-images.githubusercontent.com/63800086/146790069-f4eec250-6dbd-4eeb-9b60-c9f4c9dce696.png)

<calibration 결과 저장> - 오차 1픽셀 이하

![image](https://user-images.githubusercontent.com/63800086/146790097-288505fa-d87d-47a5-b063-2d9060d7dd14.png)

<calibration 결과로 2d영상에서 3d point에 대응하는 2d pixel position 찾기 >

![image](https://user-images.githubusercontent.com/63800086/146790299-43fc020d-8b3d-478d-b837-6be970b53f51.png)

(X축 – 빨간색, Y축 – 녹색, Z축 – 파란색)


# pose-estimation

![image](https://user-images.githubusercontent.com/63800086/146790412-89e56591-e02f-45d4-a8f2-cd20a8652433.png)
