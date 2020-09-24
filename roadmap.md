# bascorro_cv

## To do and research in nearby future

1. **Using custom compiled opencv-contrib library with OPENMP enabled**

    open mp will enable pararell processing, which will allow us to utilize all four core in our raspi,
    but somehow as mentioned [here](https://stackoverflow.com/questions/37337828/openmp-how-to-use-all-available-cpu-to-improve-performance), the improvement not really significant, but still worth to try

      really usefull links
      - https://stackoverflow.com/questions/29494503/how-to-compile-opencv-with-openmp
      - http://answers.opencv.org/question/103701/how-opencv-use-openmp-thread-to-get-performance/
    
2. **Research about the encoding that being used in the realtime video processing**

    **if** you still using usb web cam, while based on the previous experience, seems not very bad, the problem with the usb webcam is that the encoding process of the realtime video will hogging the cpu so much by theory (but somehow seems not really happening), rather than if you're using raspi camera which will utilize the GPU to do the encoding, so probably this also worth to research


4. **Update raspi to last version**

      uselfull links 
        - [Raspbian strecth](https://www.raspberrypi.org/blog/raspbian-stretch/)
    

5. **Update your code to fit with OpenCV 4**

    opencv 4 as mentioned in its website offers more feature, and some new algorithm, not really mentioning about performance increase, but we're expecting there is no performance degradation, so this also worth to try

      Usefull links 
      - https://www.pyimagesearch.com/2018/09/26/install-opencv-4-on-your-raspberry-pi/

 11. **Research about ROS**
 
 With our current method to drive the servo and stuff, as far as i know, it's fundamentally different than how ros works. And so little reference about how to drive non dynamixel servo, and "really" builing at least biped robot. So this part perhaps need longer time to research than any other part.
Carefully read the whole documentation from ros website (link below)

  Usefull Reference
  - https://answers.ros.org/question/270089/how-to-implement-ros-in-my-custom-made-robot/
  - http://wiki.ros.org/tf/Tutorials
  
    
