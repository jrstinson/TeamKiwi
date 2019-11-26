from unittest import TestCase
import os
class TestPicture(TestCase):

    def test_picture(self):
        sut= "/picture/dummy/IMG_2034.jpg"
        if not os.path.exists(sut):
            self.fail()