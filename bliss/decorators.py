# coding=utf-8
__author__ = 'msorescu'

import bliss
import traceback


from collections import OrderedDict
from django.utils.functional import wraps
from rest_framework.response import Response
from rest_framework import status


def content_type_decorator(c_type):
    """
    Overrides the Content-Type provided by the view.
    Accepts a single argument, the new Content-Type
    value to be written to the outgoing response.
    """
    def decorator(view):
        def wrapper(request, *args, **kwargs):
            response = view(request, *args, **kwargs)
            response['Content-Type'] = c_type
            return response
        return wraps(view)(wrapper)
    return decorator


def error_handler_decorator(**arguments):
    """
    Logs any errors that occurred during the view
    in a special model design for app-specific errors
    """
    version_number = safe_val(arguments, 'version_number', '1.0.0')

    def decorator(view):
        def wrapper(request, *args, **kwargs):

            try:

                return view(request, *args, **kwargs)

            except (TypeError, ValueError), e:
                error_message = str('BLISS API ERROR: you provide invalid data: %s ' % str(e))
                bliss.log.error(error_message, exc_info=True)
                return handle_exception(view=view, error_message=error_message, version_number=version_number)

            except (IndexError, KeyError, AttributeError), e:
                error_message = str('BLISS API ERROR: data retrieval accessing a non-existent element: %s ' % str(e))
                bliss.log.error(error_message, exc_info=True)
                return handle_exception(view=view, error_message=error_message, version_number=version_number)

            except ArithmeticError, e:
                error_message = str('BLISS API ERROR: some math error occurred: %s ' % str(e))
                bliss.log.error(error_message, exc_info=True)
                return handle_exception(view=view, error_message=error_message, version_number=version_number)

            except RuntimeError, e:
                error_message = str('BLISS API RUNTIME ERROR: %s ' % str(e))
                bliss.log.error(error_message, exc_info=True)
                return handle_exception(view=view, error_message=error_message, version_number=version_number)


            except Exception, e:
                error_message = str('CALLBACK API ERROR: %s ' % str(e))
                bliss.log.error(error_message, exc_info=True)

                return handle_exception(view=view, error_message=error_message, version_number=version_number)

                # Re-raise it so standard error handling still applies
                # raise
        return wraps(view)(wrapper)
    return decorator


def handle_exception(view=None, error_message=None, version_number=None):
    error_code = str('200%d' % view.func_code.co_flags)
    error_description = str('Developer-targeted at file: %s, method: %s, at first line number: %s'
                            % (view.func_code.co_filename, view.func_code.co_name, view.func_code.co_firstlineno))
    error_trace = str(traceback.format_exc())

    results = OrderedDict([('meta',
                            OrderedDict([('errors',
                                          OrderedDict([('message', error_message),
                                                       ('code', error_code), ('description', error_description),
                                                       ('trace', error_trace)])),
                                         ('build', version_number)]))])
    return Response(results, status=status.HTTP_200_OK)


def safe_val(data, name, def_val=None):
    return data[name] if name in data else def_val
