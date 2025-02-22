import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from awsgluedq.transforms import EvaluateDataQuality

args = getResolvedOptions(sys.argv, ['JOB_NAME'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Default ruleset used by all target nodes with data quality enabled
DEFAULT_DATA_QUALITY_RULESET = """
    Rules = [
        ColumnCount > 0
    ]
"""

# Script generated for node Album
Album_node1740185838111 = glueContext.create_dynamic_frame.from_options(format_options={"quoteChar": "\"", "withHeader": True, "separator": ",", "optimizePerformance": False}, connection_type="s3", format="csv", connection_options={"paths": ["s3://spotify-project-s/staging/albums.csv"], "recurse": True}, transformation_ctx="Album_node1740185838111")

# Script generated for node track
track_node1740185838924 = glueContext.create_dynamic_frame.from_options(format_options={"quoteChar": "\"", "withHeader": True, "separator": ",", "optimizePerformance": False}, connection_type="s3", format="csv", connection_options={"paths": ["s3://spotify-project-s/staging/track.csv"], "recurse": True}, transformation_ctx="track_node1740185838924")

# Script generated for node Artist
Artist_node1740185838557 = glueContext.create_dynamic_frame.from_options(format_options={"quoteChar": "\"", "withHeader": True, "separator": ",", "optimizePerformance": False}, connection_type="s3", format="csv", connection_options={"paths": ["s3://spotify-project-s/staging/artists.csv"], "recurse": True}, transformation_ctx="Artist_node1740185838557")

# Script generated for node Album artist Join
AlbumartistJoin_node1740185963456 = Join.apply(frame1=Album_node1740185838111, frame2=Artist_node1740185838557, keys1=["artist_id"], keys2=["id"], transformation_ctx="AlbumartistJoin_node1740185963456")

# Script generated for node all join
alljoin_node1740185973874 = Join.apply(frame1=AlbumartistJoin_node1740185963456, frame2=track_node1740185838924, keys1=["track_id"], keys2=["track_id"], transformation_ctx="alljoin_node1740185973874")

# Script generated for node Drop Fields
DropFields_node1740186158418 = DropFields.apply(frame=alljoin_node1740185973874, paths=["`.track_id`", "id"], transformation_ctx="DropFields_node1740186158418")

# Script generated for node destination
EvaluateDataQuality().process_rows(frame=DropFields_node1740186158418, ruleset=DEFAULT_DATA_QUALITY_RULESET, publishing_options={"dataQualityEvaluationContext": "EvaluateDataQuality_node1740185825953", "enableDataQualityResultsPublishing": True}, additional_options={"dataQualityResultsPublishing.strategy": "BEST_EFFORT", "observations.scope": "ALL"})
destination_node1740186224442 = glueContext.write_dynamic_frame.from_options(frame=DropFields_node1740186158418, connection_type="s3", format="glueparquet", connection_options={"path": "s3://spotify-project-s/datawarehouse/", "partitionKeys": []}, format_options={"compression": "snappy"}, transformation_ctx="destination_node1740186224442")

job.commit()