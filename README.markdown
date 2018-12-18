# python FFmpeg wrapper based on rVideo


## Warning

Don't pass a user input as an ffmpeg execute command since it's executed with
subprocess' shell argument set to True. This could lead to bad things (shell injection)


## Sample usage (VideoInspector)

    from video_inspector import VideoInspector
    video = VideoInspector("/path/to/video.mov")
    print video.duration()
    print video.fps()


## Sample usage (VideoEncoder)

    from video_encoder import VideoEncoder
    video = VideoEncoder("/path/to/video_input.mov")
    def print_progress(current_pos, duration):
        print "%s%%" % (current_pos / duration) * 100
    def encoding_complete():
        print "encoding complete"
    video.execute(
        "%(ffmpeg_bin)s -y -i %(input_file)s %(output_file)s",
        "/path/to/output.mp4",
        print_progress,
        encoding_complete
    )

## Sample usage (VideoRtspInspector)

ffmpeg execute command with subprocess' shell argument set to False.

    from video_rtsp_inspector import VideoRtspInspector

    video = VideoRtspInspector()
    video.setUp(RTSP_TRANSPORT, RTSP_URL, OUTPUT)
    if video.waitReady(5) == False:
        print("please confirm '{}' is ready!".format(self.RTSP_URL))
    else:
        print(video.fps_round())

## Test usage (VideoRtspInspector)

    python test_rtsp.py tcp rtsp://192.168.5.8 udp://localhost:8888