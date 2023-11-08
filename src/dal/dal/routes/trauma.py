import logbook
from fastapi import APIRouter

from .. import config

trauma_router = APIRouter()

logger = logbook.Logger(__name__)


@trauma_router.get('/images/{patient}')
def get_images(patient: int):
    import pyodbc
    import pandas as pd
    with pyodbc.connect(config.arc_connection) as con:
        results = pd.read_sql(
            f''' select distinct
                  [SPS_KEY]
                 ,[image_name]
                 ,[image_date]
             FROM [dwh].[stg].[hospitalization_with_trauma]
             where image_date>=hospitaladmission-1
             and id={patient}''', con
        ).to_dict(orient='records')
    return [
        {
            'imageLink': f'https://eagle.arc-beta.sheba.gov.il/portal/default.aspx?user_name=9999999999&password=ABPKFCHFOGIEJFALBEIIKGGJNKCMPJOB&password_encrypted=true&accession_number={result["SPS_KEY"]}',
            'at': result["image_date"],
            'imageName': result["image_name"]
        } for result in results
    ]


@trauma_router.get('/surgeries/{patient}')
def get_surgeries(patient: int):
    import pyodbc
    import pandas as pd
    with pyodbc.connect(config.arc_connection) as con:
        results = pd.read_sql(
            f'''SELECT distinct 
                [surgery] 
	           ,[surgery_time]
              FROM [dwh].[stg].[Hospitalization_with_trauma]
              where surgery_time>=hospitaladmission-1
             and id={patient}
             order by surgery_time desc ''', con
        ).to_dict(orient='records')
    return [
        {
            'at': result["surgery_time"],
            'surgeryName': result["surgery"]
        } for result in results
    ]


@trauma_router.get('/records')
def get_records():
    import pyodbc
    import pandas as pd
    sql = f"""
       SELECT  distinct[id] 
      ,[first_name] + ' ' +[last_name] as [name]
      ,[HospitalAdmission]
      ,[DepartmentNames]
      ,[last_DepartmentName] AS [DepartmentName]
      ,[diagnosis]
  FROM [dwh].[stg].[hospitalization_with_trauma]  with(nolock)
    """

    logger.debug('sql query: ', sql)

    try:
        with pyodbc.connect(config.arc_connection) as con:
            data = pd.read_sql(sql, con)
    except TypeError:
        logger.exception('Could not fetch data')
    return data.to_dict(orient="records")
