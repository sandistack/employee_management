from rest_framework import status
from rest_framework.response import Response


class APIResponse:
    """
    Standardized API Response Handler
    ==================================
    Provides consistent response formatting across all API endpoints.
    All responses follow the structure: {status, message, data/errors}
    """
    
    @staticmethod
    def success(data=None, message="Success", status_code=status.HTTP_200_OK):
        """
        Standard success response
        
        Args:
            data: Response payload (dict, list, or None)
            message: Success message description (default: "Success")
            status_code: HTTP status code (default: 200 OK)
        
        Returns:
            Response: {
                'status': 'success',
                'message': str,
                'data': any
            }
        
        Example:
            >>> APIResponse.success(data={'user_id': 1}, message="User retrieved")
            >>> APIResponse.success(data=[...], message="List fetched", status_code=200)
        """
        return Response({
            'status': 'success',
            'message': message,
            'data': data
        }, status=status_code)
    
    @staticmethod
    def paginated(data, pagination_info, message="Success"):
        """
        Paginated success response
        
        Args:
            data: Response payload (usually list of items)
            pagination_info: Pagination metadata dict containing:
                - current_page: Current page number
                - total_pages: Total number of pages
                - per_page: Items per page
                - total_items: Total item count
                - has_next: Boolean for next page availability
                - has_previous: Boolean for previous page availability
                - next_page: Next page number or None
                - previous_page: Previous page number or None
            message: Success message (default: "Success")
        
        Returns:
            Response: {
                'status': 'success',
                'message': str,
                'data': list,
                'pagination': dict
            }
        
        Example:
            >>> pagination = {
            ...     'current_page': 1,
            ...     'total_pages': 5,
            ...     'per_page': 10,
            ...     'total_items': 50,
            ...     'has_next': True,
            ...     'has_previous': False
            ... }
            >>> APIResponse.paginated(data=[...], pagination_info=pagination)
        """
        return Response({
            'status': 'success',
            'message': message,
            'data': data,
            'pagination': pagination_info
        }, status=status.HTTP_200_OK)
    
    @staticmethod
    def error(message="Error occurred", errors=None, status_code=status.HTTP_400_BAD_REQUEST):
        """
        Standard error response
        
        Args:
            message: Error message description (default: "Error occurred")
            errors: Additional error details - dict or list (optional)
            status_code: HTTP status code (default: 400 Bad Request)
        
        Returns:
            Response: {
                'status': 'error',
                'message': str,
                'errors': dict|list (optional)
            }
        
        Example:
            >>> APIResponse.error(message="Validation failed", errors={'email': 'Invalid format'})
            >>> APIResponse.error(message="Bad request", status_code=400)
        """
        response_data = {
            'status': 'error',
            'message': message
        }
        if errors:
            response_data['errors'] = errors
        return Response(response_data, status=status_code)
    
    @staticmethod
    def created(data=None, message="Created successfully"):
        """
        Resource created response (HTTP 201)
        
        Args:
            data: Created resource data (optional)
            message: Success message (default: "Created successfully")
        
        Returns:
            Response: Success response with 201 status code
        
        Example:
            >>> APIResponse.created(data={'id': 123, 'name': 'New User'})
        """
        return APIResponse.success(data, message, status.HTTP_201_CREATED)
    
    @staticmethod
    def not_found(message="Resource not found"):
        """
        Resource not found response (HTTP 404)
        
        Args:
            message: Error message (default: "Resource not found")
        
        Returns:
            Response: Error response with 404 status code
        
        Example:
            >>> APIResponse.not_found(message="User not found")
        """
        return APIResponse.error(message, status_code=status.HTTP_404_NOT_FOUND)
    
    @staticmethod
    def unauthorized(message="Unauthorized access"):
        """
        Unauthorized access response (HTTP 401)
        
        Args:
            message: Error message (default: "Unauthorized access")
        
        Returns:
            Response: Error response with 401 status code
        
        Example:
            >>> APIResponse.unauthorized(message="Invalid credentials")
        """
        return APIResponse.error(message, status_code=status.HTTP_401_UNAUTHORIZED)
    
    @staticmethod
    def forbidden(message="Forbidden access"):
        """
        Forbidden access response (HTTP 403)
        
        Args:
            message: Error message (default: "Forbidden access")
        
        Returns:
            Response: Error response with 403 status code
        
        Example:
            >>> APIResponse.forbidden(message="Insufficient permissions")
        """
        return APIResponse.error(message, status_code=status.HTTP_403_FORBIDDEN)
    
    @staticmethod
    def server_error(message="Internal server error"):
        """
        Internal server error response (HTTP 500)
        
        Args:
            message: Error message (default: "Internal server error")
        
        Returns:
            Response: Error response with 500 status code
        
        Example:
            >>> APIResponse.server_error(message="Database connection failed")
        """
        return APIResponse.error(message, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)