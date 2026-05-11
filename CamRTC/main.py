import host 


class HeadsetView: 
    def start_view():
        headset = host.stream()
        headset.start()

HeadsetView.start_view()