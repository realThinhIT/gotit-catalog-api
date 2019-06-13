def add_resources(api):
    """
    To extend RESTful resources and create endpoints to existing Flask server

    :param api: Api instance from flask_restful
    """

    from .user import UserResource

    # Define list of resources and its endpoints here
    # Format: [(Resource, 'route')]
    _resources = [
        (UserResource, '/users')
    ]

    for resource in _resources:
        api.add_resource(resource[0], resource[1])
