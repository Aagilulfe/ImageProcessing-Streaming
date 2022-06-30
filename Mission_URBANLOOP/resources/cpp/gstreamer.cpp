#include <iostream>
// #include </home/luc/OpenCV_installation/opencv-4.x/include/opencv2/opencv.hpp>
#include </usr/local/include/opencv4/opencv2/opencv.hpp>

void sender()
{
    // VideoCapture: Getting frames using 'v4l2src' plugin, format is 'BGR' because
    // the VideoWriter class expects a 3 channel image since we are sending colored images.
    // Both 'YUY2' and 'I420' are single channel images. 
    VideoCapture cap("v4l2src ! video/x-raw,format=BGR,width=640,height=480,framerate=30/1 ! appsink",CAP_GSTREAMER);

    // VideoWriter: 'videoconvert' converts the 'BGR' images into 'YUY2' raw frames to be fed to
    // 'jpegenc' encoder since 'jpegenc' does not accept 'BGR' images. The 'videoconvert' is not
    // in the original pipeline, because in there we are reading frames in 'YUY2' format from 'v4l2src'
    VideoWriter out("appsrc ! videoconvert ! video/x-raw,format=YUY2,width=640,height=480,framerate=30/1 ! jpegenc ! rtpjpegpay ! udpsink host=127.0.0.1 port=5000",CAP_GSTREAMER,0,30,Size(640,480),true);

    if(!cap.isOpened() || !out.isOpened())
    {
        cout<<"VideoCapture or VideoWriter not opened"<<endl;
        exit(-1);
    }

    Mat frame;

    while(true) {

        cap.read(frame);

        if(frame.empty())
            break;

        out.write(frame);

        imshow("Sender", frame);
        if(waitKey(1) == 's')
            break;
    }
    destroyWindow("Sender");
}

void receiver()
{    
    // The sink caps for the 'rtpjpegdepay' need to match the src caps of the 'rtpjpegpay' of the sender pipeline
    // Added 'videoconvert' at the end to convert the images into proper format for appsink, without
    // 'videoconvert' the receiver will not read the frames, even though 'videoconvert' is not present
    // in the original working pipeline
    VideoCapture cap("udpsrc port=5000 ! application/x-rtp,media=video,payload=26,clock-rate=90000,encoding-name=JPEG,framerate=30/1 ! rtpjpegdepay ! jpegdec ! videoconvert ! appsink",CAP_GSTREAMER);

    if(!cap.isOpened())
    {
        cout<<"VideoCapture not opened"<<endl;
        exit(-1);
    }

    Mat frame;

    while(true) {

        cap.read(frame);

        if(frame.empty())
            break;

        imshow("Receiver", frame);
        if(waitKey(1) == 'r')
            break;
    }
    destroyWindow("Receiver");
}

int main() {
    receiver();
    return 0;
}