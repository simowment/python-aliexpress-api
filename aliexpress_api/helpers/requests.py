from types import SimpleNamespace
import json
from typing import Type, TypeVar, Optional, Any
from ..models.base import BaseModel

from ..errors import ApiRequestException, ApiRequestResponseException

T = TypeVar("T", bound=BaseModel)

def api_request(request, response_name: str, model_class: Optional[Type[T]] = None, session: Optional[str] = None) -> Any:
    """Makes an API request and returns the parsed response.
    
    Args:
        request: The API request object from SDK.
        response_name: The name of the response key in the JSON.
        model_class: The class to parse the result into. If None, returns SimpleNamespace.
        session: Optional session token.
        
    Returns:
        The parsed response, either as a model_class instance or a SimpleNamespace.
    """
    try:
        response = request.getResponse(authrize=session)
    except Exception as error:
        if hasattr(error, 'message'):
            raise ApiRequestException(error.message) from error
        raise ApiRequestException(str(error)) from error

    try:
        if response_name not in response:
            # Check for top-level errors if response_name is missing
            if 'code' in response and response['code'] not in ('0', 0, '200', 200, 'success'):
                raise ApiRequestResponseException(f"API Error {response['code']}: {response.get('msg', 'Unknown error')}")
            raise ApiRequestResponseException(f"Response Name '{response_name}' not found in response keys: {list(response.keys())}")
        
        inner_response = response[response_name]
        
        # Check for code in inner response (supporting various formats)
        inner_code = inner_response.get('resp_code', inner_response.get('rsp_code', inner_response.get('code')))
        if inner_code is not None and inner_code not in ('0', 0, '200', 200, 'success'):
            inner_msg = inner_response.get('resp_msg', inner_response.get('rsp_msg', inner_response.get('msg', 'Unknown error')))
            raise ApiRequestResponseException(f"API Error {inner_code}: {inner_msg}")

        if 'resp_result' in inner_response:
            result_obj = inner_response['resp_result']
        elif 'result' in inner_response:
             result_obj = inner_response['result']
        else:
            # Fallback if neither resp_result nor result is present but other data is
            if 'data' in inner_response:
                result_obj = inner_response['data']
            else:
                # If it's a success but has no result/resp_result/data, return the inner response
                 result_obj = inner_response

        # Some APIs return result and then another result inside, we flatten if possible
        if isinstance(result_obj, dict) and 'result' in result_obj:
            result_obj = result_obj['result']

        if model_class and issubclass(model_class, BaseModel):
            return model_class.from_dict(result_obj)

        # Deeply convert result_obj to SimpleNamespace (legacy)
        result_json = json.dumps(result_obj)
        processed_response = json.loads(result_json, object_hook=lambda d: SimpleNamespace(**d))
        
        return processed_response

    except Exception as error:
        if isinstance(error, (ApiRequestResponseException, ApiRequestException)):
            raise error
        raise ApiRequestResponseException(str(error)) from error
