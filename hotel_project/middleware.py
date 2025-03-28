"""
Middleware to handle Elastic Beanstalk specific needs
"""

class EBHealthCheckMiddleware:
    """
    Middleware to handle Elastic Beanstalk health checks.
    This middleware ensures that health check requests from ELB are responded to properly.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.META.get('HTTP_USER_AGENT', '').startswith('ELB-HealthChecker'):
            if request.path == '/' and request.method == 'GET':
                from hotel_project.health_check import health_check
                return health_check(request)
        return self.get_response(request)
