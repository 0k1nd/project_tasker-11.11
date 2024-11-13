# from rest_framework.routers import DefaultRouter, DynamicRoute, Route
#
#
# class CustomRouter(DefaultRouter):
#     """
#     sets action as detail = False for all default urls
#     """
#     routes = [
#         # List route.
#         Route(
#             url=r'^{prefix}{trailing_slash}$',
#             mapping={
#                 'get': 'list',
#                 'post': 'create'
#             },
#             name='{basename}-list',
#             detail=False,
#             initkwargs={'suffix': 'List'}
#         ),
#         # Dynamically generated list routes. Generated using
#         # @action(detail=False) decorator on methods of the viewset.
#         DynamicRoute(
#             url=r'^{prefix}/{url_path}{trailing_slash}$',
#             name='{basename}-{url_name}',
#             detail=False,
#             initkwargs={}
#         ),
#         # Detail route.
#         Route(
#             url=r'^{prefix}{trailing_slash}$',  ######### changed
#             mapping={
#                 'get': 'retrieve',
#                 'put': 'update',
#                 'patch': 'partial_update',
#                 'delete': 'destroy'
#             },
#             name='{basename}-detail',
#             detail=False,  ######### changed
#             initkwargs={'suffix': 'Instance'}
#         ),
#         # Dynamically generated detail routes. Generated using
#         # @action(detail=True) decorator on methods of the viewset.
#         DynamicRoute(
#             url=r'^{prefix}/{url_path}{trailing_slash}$',  ######### changed
#             name='{basename}-{url_name}',
#             detail=False,  ######### changed
#             initkwargs={}
#         ),
#     ]