# K2 - Spark notes

## initialization

At the beginning of the process, an object JavaSparkContext is created, which specifies how to access the cluster. To create the context, a configuration object SparkConf is used, which contains information about the application.

```java
package ziga.spark;

import org.apache.spark.SparkConf;
import org.apache.spark.api.java.JavaSparkContext;

public class StartingPoint {
    public static void main(String[] args) {
        String appName = "Start0";  // must be unique in the claster
        String master = "local";    // specifies the URL of the Spark, Mesos, or YARN cluster, or "local" if running locally.

        SparkConf conf = new SparkConf()
                            .setAppName(appName)
                            .setMaster(master );
        
        JavaSparkContext sc = new JavaSparkContext(conf);

    }
}
```

## RDD and Dataset

- At its core, Spark uses a `Resilient Distributed Dataset (RDD)`.
- This is a `read-only` dataset intended for use on clusters of multiple machines.
- The system maintains this dataset to be `fault-tolerant`.
- These datasets function as the working set for distributed programs, offering a (deliberately) limited form of distributed shared memory.
- A newer variant of the architecture, Dataset, represents an abstraction built on top of the given dataset.

There are two ways to create these datasets:

- Parallelizing an existing collection
- Referencing a dataset in an external storage system, such as a shared file system, HDFS, HBase, or any data source that offers Hadoop InputFormat.


