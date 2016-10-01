__author__ = 'msorescu'
import bliss
from bliss.serializers import PictureSerializer
from rest_framework.views import APIView
from rest_framework import parsers
from rest_framework import renderers

from rest_framework.response import Response

from rest_framework import status
from decorators import error_handler_decorator


class FileUploadView(APIView):

    permission_classes = ()
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)
    serializer_class = PictureSerializer

    @error_handler_decorator(version_number='1.0.0')
    def post(self, request, format=None):
        bliss.log.debug('Starting posting files...')
        result = []
        for key in dict(request.FILES).keys():
            for f in request.FILES.getlist(key):
                serializer = self.serializer_class(data={'file':f, 'slug':key})

                if serializer.is_valid():
                    serializer.save()
                    msg = str('Stored in S3 the file {1:s} from fileuploader {0:s}'.format(key,f))
                    bliss.log.debug(msg)
                    result.append(msg)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(result, status=status.HTTP_201_CREATED)


