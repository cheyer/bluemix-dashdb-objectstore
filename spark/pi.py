# This script gets rows from DashDB and saves them as a Parquet File in the Bluemix Object Store
from pyspark import SparkConf, SparkContext
from pyspark.sql import SQLContext

conf = SparkConf().setAppName("dashdb to objectstore")
sc = SparkContext(conf=conf)
sqlContext = SQLContext(sc)

### TODO ###
# paste the credentials of DashDB
credentialsDDB = {
  'port':'',
  'db':'',
  'username':'',
  'ssljdbcurl':'',
  'host':'',
  'https_url':'',
  'dsn':'',
  'hostname':'',
  'jdbcurl':'',
  'ssldsn':'',
  'uri':'',
  'password':''
}

### TODO ###
# change the tablename 
tablename = "MYTABLE";
url = credentialsDDB["jdbcurl"]+":user="+credentialsDDB["username"]+";password="+credentialsDDB["password"]+";";
table = credentialsDDB["username"]+"."+tablename;

# create Spark SQLContext with JDBC URL
df = sqlContext.read.format('jdbc').options(url=url, dbtable=table).load()

# make data available as table with the name simdata
df.registerTempTable("simdata")

# get all rows in table simdata
df = sqlContext.sql("SELECT * FROM simdata")

# test: print out first 5 elements and number of rows
print(df.head())
print(df.count())

### TODO ###
# paste the credentials of Object Store
# check that there is an attribute "name" with the value "spark in the credentials, else add
oscredentials = {
    "name": "spark",
    "auth_url": "",
    "project": "",
    "projectId": "",
    "region": "",
    "userId": "",
    "username": "",
    "password": "",
    "domainId": "",
    "domainName": ""
}

# function to set write configuration
def set_hadoop_config(credentials):
    prefix = "fs.swift.service." + credentials['name']
    hconf = sc._jsc.hadoopConfiguration()
    hconf.set(prefix + ".auth.url", credentials['auth_url']+'/v3/auth/tokens')
    hconf.set(prefix + ".auth.endpoint.prefix", "endpoints")
    hconf.set(prefix + ".tenant", credentials['projectId'])
    hconf.set(prefix + ".username", credentials['userId'])
    hconf.set(prefix + ".password", credentials['password'])
    hconf.setInt(prefix + ".http.port", 8080)
    hconf.set(prefix + ".region", credentials['region'])
    hconf.setBoolean(prefix + ".public", True)
    
# set write configuration with Object Store credentials
set_hadoop_config(oscredentials)

### TODO ###
# change container name (my-container) and file name to be saved (simdata.parquet)
df.write.parquet("swift://my-container.spark/simdata.parquet", mode="overwrite")

print("finished script!")
