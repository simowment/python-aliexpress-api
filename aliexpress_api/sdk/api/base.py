# -*- coding: utf-8 -*-
"""
AliExpress API SDK Base Module.

This module provides the core functionality for making API requests,
including signature generation and request handling.
"""

import hashlib
import hmac
import json
import time
import requests as http_requests

from ...logging_config import get_logger

logger = get_logger("sdk")

# SDK Version
SYSTEM_GENERATE_VERSION = "iop-sdk-python-20220609"

P_APPKEY = "app_key"
P_API = "method"
P_SESSION = "session"
P_ACCESS_TOKEN = "access_token"
P_VERSION = "v"
P_FORMAT = "format"
P_TIMESTAMP = "timestamp"
P_SIGN = "sign"
P_SIGN_METHOD = "sign_method"
P_PARTNER_ID = "partner_id"

P_CODE = "code"
P_SUB_CODE = "sub_code"
P_MSG = "msg"
P_SUB_MSG = "sub_msg"


N_REST = "/sync"


def sign(secret, api, parameters):
    """Generate HMAC-SHA256 signature for API request.

    Args:
        secret: App secret key
        api: API name/path (e.g. 'aliexpress.affiliate.link.generate')
        parameters: Dict of request parameters (excluding 'sign')

    Returns:
        Uppercase hex string of HMAC-SHA256 signature
    """
    # Sort parameters alphabetically
    sorted_keys = sorted(parameters.keys())

    # Build signature string
    # If API contains '/', prepend it to the parameters string
    if "/" in api:
        parameters_str = api + "".join("%s%s" % (key, parameters[key]) for key in sorted_keys)
    else:
        parameters_str = "".join("%s%s" % (key, parameters[key]) for key in sorted_keys)

    # Calculate HMAC-SHA256
    h = hmac.new(
        secret.encode("utf-8"),
        parameters_str.encode("utf-8"),
        digestmod=hashlib.sha256
    )
    return h.hexdigest().upper()


class FileItem(object):
    """Represents a file to be uploaded in a multipart request."""

    def __init__(self, filename=None, content=None):
        self.filename = filename
        self.content = content


class TopException(Exception):
    """API business logic exception."""

    def __init__(self):
        self.errorcode = None
        self.message = None
        self.subcode = None
        self.submsg = None
        self.application_host = None
        self.service_host = None

    def __str__(self):
        parts = [
            f"errorcode={self.errorcode}",
            f"message={self.message}",
            f"subcode={self.subcode}",
            f"submsg={self.submsg}",
            f"application_host={self.application_host}",
            f"service_host={self.service_host}",
        ]
        return " ".join(parts)


class RequestException(Exception):
    """HTTP request exception."""
    pass


class RestApi(object):
    """Base class for all REST API requests."""

    def __init__(self, domain="api-sg.aliexpress.com", port=443):
        """Initialize the REST API base class.

        Args:
            domain: API domain (default: api-sg.aliexpress.com)
            port: Port number (default: 443 for HTTPS)
        """
        self.__domain = domain
        self.__port = port
        self.__httpmethod = "POST"
        from .. import getDefaultAppInfo

        if getDefaultAppInfo():
            self.__app_key = getDefaultAppInfo().appkey
            self.__secret = getDefaultAppInfo().secret

    def set_app_info(self, appinfo):
        """Set the app credentials."""
        self.__app_key = appinfo.appkey
        self.__secret = appinfo.secret

    def getapiname(self):
        """Return the API name. Override in subclasses."""
        return ""

    def getMultipartParas(self):
        """Return list of multipart parameters. Override in subclasses."""
        return []

    def getTranslateParas(self):
        """Return parameter translation dict. Override in subclasses."""
        return {}

    def _check_requst(self):
        """Validate request. Override in subclasses."""
        pass

    def getResponse(self, authrize=None, timeout=30):
        """Execute the API request and return the response.

        Args:
            authrize: Optional access token for authenticated requests
            timeout: Request timeout in seconds (default: 30)

        Returns:
            dict: Parsed JSON response

        Raises:
            RequestException: If the HTTP request fails
            TopException: If the API returns an error response
        """
        # Build base URL
        protocol = "https" if self.__port == 443 else "http"
        base_url = f"{protocol}://{self.__domain}{N_REST}"

        # Build timestamp
        timestamp = str(int(time.time() * 1000))

        # System parameters
        sys_parameters = {
            P_FORMAT: "json",
            P_APPKEY: self.__app_key,
            P_SIGN_METHOD: "sha256",
            P_TIMESTAMP: timestamp,
            P_PARTNER_ID: SYSTEM_GENERATE_VERSION,
            P_API: self.getapiname(),
        }

        if authrize is not None:
            sys_parameters[P_ACCESS_TOKEN] = authrize

        # Application parameters
        application_parameter = self.getApplicationParameters()

        # Generate signature
        sign_parameter = sys_parameters.copy()
        sign_parameter.update(application_parameter)
        sys_parameters[P_SIGN] = sign(self.__secret, self.getapiname(), sign_parameter)

        # Build request
        if self.getMultipartParas():
            # Multipart form data for file uploads
            files = {}
            for key in self.getMultipartParas():
                fileitem = getattr(self, key, None)
                if fileitem and isinstance(fileitem, FileItem):
                    files[key] = (fileitem.filename, fileitem.content)

            logger.debug(f"API {self.getapiname()} - Multipart request with files: {list(files.keys())}")
            response = http_requests.post(
                base_url,
                params=sys_parameters,
                data=application_parameter,
                files=files,
                timeout=timeout
            )
        else:
            # Standard form data
            logger.debug(f"API {self.getapiname()} - Request params: {sys_parameters}")
            logger.debug(f"API {self.getapiname()} - Application params: {application_parameter}")
            response = http_requests.post(
                base_url,
                params=sys_parameters,
                data=application_parameter,
                timeout=timeout
            )

        # Check HTTP status
        if response.status_code != 200:
            raise RequestException(
                f"HTTP {response.status_code}: {response.text}"
            )

        # Log raw response
        logger.debug(f"API {self.getapiname()} - Raw response: {response.text}")

        # Parse JSON
        jsonobj = response.json()

        # Check for API errors
        if "error_response" in jsonobj:
            error = TopException()
            err = jsonobj["error_response"]
            error.errorcode = err.get(P_CODE)
            error.message = err.get(P_MSG)
            error.subcode = err.get(P_SUB_CODE)
            error.submsg = err.get(P_SUB_MSG)
            error.application_host = response.headers.get("Application-Host", "")
            error.service_host = response.headers.get("Location-Host", "")
            raise error

        return jsonobj

    def getApplicationParameters(self):
        """Extract application parameters from the request object."""
        application_parameter = {}
        for key in self.__dict__:
            value = self.__dict__[key]
            if (
                not key.startswith("__")
                and key not in self.getMultipartParas()
                and not key.startswith("_RestApi__")
                and value is not None
            ):
                if key.startswith("_"):
                    application_parameter[key[1:]] = value
                else:
                    application_parameter[key] = value

        # Translate parameter names if needed
        translate_parameter = self.getTranslateParas()
        for key in list(application_parameter.keys()):
            if key in translate_parameter:
                application_parameter[translate_parameter[key]] = application_parameter[key]
                del application_parameter[key]

        logger.debug(f"API {self.getapiname()} - Final params: {application_parameter}")
        return application_parameter
