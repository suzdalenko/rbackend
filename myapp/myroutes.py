from django.urls import path
from .controllers.excel import Excel
from .controllers.api import Api
from .controllers import person, collection, lines_collection, report


urlpatterns = [
    path('example/', Api.example),
  
    path('userLogin/', person.PersonController.userLogin),
    path('save_user_location/', person.PersonController.save_user_location),
    
    path('uploadFileCollection/', collection.CollectionController.uploadFileCollection ),
    path('getAllCollection/', collection.CollectionController.getAllCollection),
    path('deleteCollection/', collection.CollectionController.deleteCollection),
    
    path("lines_collection/<str:actionget>/", lines_collection.LinesCollectionController.dataget),
    path("post_parameters/<str:actionpost>/", lines_collection.LinesCollectionController.dataupdate),
    
    path("basic_report/", Excel.basic_report),
    
    
    # http://127.0.0.1:8000/myapp/report/jui/
    path("report/<str:action_get>/", report.MyReports.report_work),

]