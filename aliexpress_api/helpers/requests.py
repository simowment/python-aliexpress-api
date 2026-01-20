"""Helper functions for making API requests."""

from types import SimpleNamespace
import json
from typing import Type, TypeVar, Optional, Any

from ..models.base import BaseModel
from ..errors import ApiRequestException, ApiRequestResponseException
from ..logging_config import get_logger

logger = get_logger("helpers")

T = TypeVar("T", bound=BaseModel)


def api_request(
    request,
    response_name: str,
    model_class: Optional[Type[T]] = None,
    session: Optional[str] = None
) -> Any:
    """Make an API request and return the parsed response.

    Args:
        request: The API request object from SDK.
        response_name: The name of the response key in the JSON.
        model_class: The class to parse the result into. If None, returns SimpleNamespace.
        session: Optional session token for authenticated requests.

    Returns:
        The parsed response, either as a model_class instance or a SimpleNamespace.

    Raises:
        ApiRequestException: If the request fails
        ApiRequestResponseException: If the response contains an error
    """
    logger.debug(f"Making API request: {request.getapiname()}")

    try:
        response = request.getResponse(authrize=session)
    except Exception as error:
        logger.error(f"API request failed: {error}")
        if hasattr(error, 'message'):
            raise ApiRequestException(error.message) from error
        raise ApiRequestException(str(error)) from error

    try:
        if response_name not in response:
            # Check for top-level errors if response_name is missing
            if 'code' in response and response['code'] not in ('0', 0, '200', 200, 'success'):
                raise ApiRequestResponseException(
                    f"API Error {response['code']}: {response.get('msg', 'Unknown error')}"
                )
            raise ApiRequestResponseException(
                f"Response key '{response_name}' not found. Available: {list(response.keys())}"
            )

        inner_response = response[response_name]

        # Check for error codes in inner response
        inner_code = inner_response.get(
            'resp_code',
            inner_response.get('rsp_code', inner_response.get('code'))
        )
        if inner_code is not None and inner_code not in ('0', 0, '200', 200, 'success'):
            inner_msg = inner_response.get(
                'resp_msg',
                inner_response.get('rsp_msg', inner_response.get('msg', 'Unknown error'))
            )
            raise ApiRequestResponseException(f"API Error {inner_code}: {inner_msg}")

        # Extract result object from various response structures
        if 'resp_result' in inner_response:
            result_obj = inner_response['resp_result']
        elif 'result' in inner_response:
            result_obj = inner_response['result']
        elif 'data' in inner_response:
            result_obj = inner_response['data']
        else:
            result_obj = inner_response

        # Flatten nested result structures
        if isinstance(result_obj, dict) and 'result' in result_obj:
            result_obj = result_obj['result']

        logger.debug(f"Extracted result: {type(result_obj)}")

        # Parse into model class if provided
        if model_class and issubclass(model_class, BaseModel):
            return model_class.from_dict(result_obj)

        # Convert to SimpleNamespace for legacy compatibility
        result_json = json.dumps(result_obj)
        return json.loads(result_json, object_hook=lambda d: SimpleNamespace(**d))

    except (ApiRequestResponseException, ApiRequestException):
        raise
    except Exception as error:
        logger.error(f"Error parsing response: {error}")
        raise ApiRequestResponseException(str(error)) from error
