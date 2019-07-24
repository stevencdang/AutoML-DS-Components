
import logging

logger = logging.getLogger(__name__)


class IframeBuilder(object):

    def __init__(self, src, height=1024, width=768):

        self.src = src
        self.height = height
        self.width = width

    def get_document(self):
        return '<!DOCTYPE html>\
                <html>\
                    <body>\
                        <iframe src="%s" width="%i" height="%i"></iframe>\
                    </body>\
                </html> ' % (self.src, self.width, self.height)

