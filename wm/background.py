from pywm import PyWMBackgroundWidget


class Background(PyWMBackgroundWidget):
    def __init__(self, wm, path):
        super().__init__(wm, path)

    def update(self):
        min_i, min_j, max_i, max_j = self.wm.get_extent()

        """
        Box of background
        """
        x = 0
        y = 0
        w = (max_i - min_i + 1)
        h = (max_j - min_j + 1)

        """
        Box of viewport within background
        """
        vp_x = self.wm.i - min_i
        vp_y = self.wm.j - min_j
        vp_w = self.wm.size
        vp_h = self.wm.size

        """
        Enlarge box and viewport
        """
        factor = 3.

        cx = x + w/2
        cy = y + h/2
        x = cx - factor/2.*w
        y = cy - factor/2.*h
        w = factor*w
        h = factor*h

        vp_cx = vp_x + vp_w/2
        vp_cy = vp_y + vp_h/2
        vp_x = vp_cx - factor/2.*vp_w
        vp_y = vp_cy - factor/2.*vp_h
        vp_w = factor*vp_w
        vp_h = factor*vp_h

        """
        Transform such that viewport has
        x, y == 0; w == wm.width; h == wm.height
        """
        m = self.wm.width / vp_w
        b = - vp_x * m
        x, w = (m * x + b), (m * (x + w) + b)
        w -= x

        m = self.wm.height / vp_h
        b = - vp_y * m
        y, h = (m * y + b), (m * (y + h) + b)
        h -= y

        """
        Fix aspect ratio
        """
        if w/h > self.width/self.height:
            new_h = self.height * w/self.width
            y -= (new_h - h)/2.
            h = new_h
        else:
            new_w = self.width * h/self.height
            x -= (new_w - w)/2.
            w = new_w

        self.set_box(x, y, w, h)