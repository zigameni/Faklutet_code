# APACHE SPARK

## Contents

- Basic Concepts
- Stream Processing Usage
- Structured Stream Programming
- Queries on Streams

## Spark

The Apache Spark software library provides a framework for distributed processing of large data sets using clusters of computers and a simple programming model. It allows applications to scale based on the available hardware, whether it's a single server or a large number of servers each with local storage. Spark offers an interface for programming clusters with implicit data parallelism and fault tolerance.

It includes the following modules:

- **Spark Core** – The foundation of the platform
- **Spark Streaming** – Real-time analytics
- **Spark SQL** – Interactive queries
- **Spark Mllib** – Machine learning
- **Spark GraphX** – Graph processing

## MapReduce

MapReduce is a programming model designed to facilitate the processing and creation of large amounts of data using parallel algorithms that can be executed on a group of computers. Inspired by functional languages (like Lisp), it involves mapping and reducing phases.

### Usage can be divided into the following steps:

1. The entire input data set that needs to be processed is split into key-value pairs.
2. In the mapping phase, an input key-value pair is processed. Based on this pair, a list is formed containing zero, one, or more key-value pairs.
   - **Map**: `(key1, val1) -> listOf(key2, val2)`
3. Once the mapping phase is complete, the outputs are grouped by key and passed to the reduction phase.
4. In the reduction phase, an input key and a list of values created in the mapping phase are processed. Based on these values, a list of results is formed.
   - **Reduce**: `(key2, listOf(val2)) -> listOf(val3)`

Depending on the language and model, some steps can be executed multiple times.

## Hadoop MapReduce

Hadoop MapReduce is a programming model for processing large data sets with parallel, distributed algorithms. Programmers can write massively parallel operators without worrying about job distribution and fault tolerance. This model uses a linear data flow structure for distributed programs where programs first read input data from disk, then map (perform) functions on the data, reduce the mapping results, and store the saved results to disk in HDFS. Since each step requires reading and writing from the disk, these jobs are slower due to disk I/O latency.

![alt text](media/image.png)

## Hadoop vs. Spark

## Comparison

### Overview

- The core of Spark's architecture was developed to address limitations in the Apache Hadoop MapReduce solution by processing data in memory. This reduces the number of job steps and reuses data across multiple parallel operations. Data is loaded into memory, operations are executed, and results are returned, significantly reducing latency in such applications. Data reuse is achieved by creating resilient distributed datasets (RDDs), which are collections of objects that are cached in memory and reused in multiple operations.

### Spark

- The architecture is based on using datasets whose elements can only be read, and these elements are distributed across multiple computers with fault tolerance in mind.
- Unlike the two-stage execution process in the Hadoop MapReduce architecture, Spark processes data using a directed acyclic graph (DAG) for task scheduling and worker node orchestration across the cluster. Nodes in the graph represent datasets, while edges represent operations on these datasets.
- This task tracking allows for fault tolerance, as it can reapply recorded operations to data from a previous state.
- Spark facilitates the implementation of iterative algorithms, which visit their dataset multiple times in a loop, and interactive/exploratory data analysis, i.e., repeated querying of a dataset.

## Using Stream Processing

### Basic Concepts

- **Mapping**
- **Filtering**
- **Reduction**
- **Collecting**
- **Combining**

### Streams

- Streams provide a way to process collections of objects similarly to functional programming.
- The collection itself does not change during processing.
- Streams allow for internal iteration over their elements.
- This differs from using iterators or for-each loops where iteration is performed manually.

### Stream Processing

- Processing elements of a stream involves setting listeners on the stream.
- These listeners are called when the stream internally iterates over elements.
- Stream iterators can form a chain:
  - The first listener in the chain can process an element and then pass it, or another element, to the next listener for further processing.

### Pipeline Processing

- Stream operations fit together to form a pipeline.
  - **Source** -> **Operations** -> **Terminal Operation**
- The stream starts with its source:
  - Sources can be data collections, arrays, functions, or input/output channels (I/O channels).
- Then comes zero or more operations:
  - Each operation creates a new stream as a result.
  - Examples of these operations are filtering and mapping.
- The stream ends with a terminal operation:
  - This operation creates a result that is not a stream.
  - Examples are reduction and processing individual elements.

### Initialization

- At the start of processing, a `JavaSparkContext` object is created, which specifies how to access the cluster. The context is created using a `SparkConf` configuration object that contains application information.

  ```java
  SparkConf conf = new SparkConf()
      .setAppName(appName)
      .setMaster(master);
  JavaSparkContext sc = new JavaSparkContext(conf);

  ```

  - `appName` – the name of the application in the cluster.
  - `master` – specifies the URL of the Spark, Mesos, or YARN cluster, or "local" if running locally.

## RDD and Dataset

### RDD

- At its core, Spark uses the Resilient Distributed Dataset (RDD).
- This is a read-only dataset distributed across multiple machines.
- The system maintains the dataset to be fault-tolerant.
- These datasets function as a working set for distributed programs, offering a (deliberately) limited form of distributed shared memory.
- A newer variant, Dataset, is an abstraction built on top of RDDs.

### RDD Creation

#### Parallelizing an Existing Collection

- Parallelization of existing collections is done by calling the `parallelize` method of the `JavaSparkContext` class on the existing collection of data. The elements of the collection are copied into a distributed dataset for parallel access.

  ```java
  List<Integer> data = Arrays.asList(1, 2, 3, 4, 5);
  JavaRDD<Integer> distData = sc.parallelize(data);
  ```

#### Methods

```java
public <T> JavaRDD<T> parallelize(List<T> list)
public <T> JavaRDD<T> parallelize(List<T> list, int numSlices)
```

- `list` – the collection of data to be parallelized.
- `numSlices` – the number of partitions to divide the dataset into. Spark will run one task for each partition of the cluster. Typically, you want 2-4 partitions for each CPU in the cluster. Spark tries to automatically set the number of partitions based on the cluster.

### Referencing an External Dataset

- A distributed dataset can be created from any storage source supported by Hadoop, including the local file system, HDFS, Cassandra, HBase, Amazon S3, etc.
- Example of creating a dataset from a text file:

  ```java
  JavaRDD<String> distFile = sc.textFile(fileName);
  ```

- The method accepts a file URI (local path, hdfs://, s3a://, etc.) and reads it as a collection of lines. The text file must be UTF-8 encoded.

#### Methods

```java
public JavaRDD<String> textFile(String path)
public JavaRDD<String> textFile(String path, int minPartitions)

```

- `path` – the file URI. File-based input methods, including `textFile`, support running on directories, compressed files, and wildcard characters. For example, `textFile("/my/directory")`, `textFile("/my/directory/*.txt")`, and `textFile("/my/directory/*.gz")`.
- `minPartitions` – the number of partitions for the file. By default, one partition is created per file block (default blocks are 128 MB in HDFS). There cannot be fewer partitions than blocks.

### Other Methods of `JavaSparkContext`

```java
public JavaPairRDD<String,String> wholeTextFiles(String path, int minPartitions)
```

- Reads a directory containing multiple small text files and returns each as pairs (filename, content). Note: `textFile` returns one record per line in each file.

```java
public <T> JavaRDD<T> objectFile(String path, int minPartitions)
```

- Supports saving objects in a simple format consisting of serialized Java objects. It is not as efficient as specialized formats but offers a simple way to save any object.

```java
public <K, V> JavaPairRDD<K,V> sequenceFile(String path, Class<K> keyClass, Class<V> valueClass, int minPartitions)
```

- `K` and `V` are the key and value types in the file. These should be subclasses of the `Writable` interface in Hadoop, such as `IntWrwitable` and `Text`.

```java
public <K, V, F extends org.apache.hadoop.mapred.InputFormat<K, V>>
JavaPairRDD<K,V> hadoopRDD(org.apache.hadoop.mapred.JobConf conf, Class<F> inputFormatClass, Class<K> keyClass, Class<V> valueClass, int minPartitions)
```

- Takes an arbitrary `JobConf` and input format class, key class, and value class. Set them as you would for a Hadoop job with an input source.

## Operations on Streams

## Types of Operations

- **Transformations:** Create a new dataset from an existing one.
- **Actions:** Return a value after performing computations on a dataset.

### Examples

- **Mapping (`map`)** is a transformation that passes each dataset element through a function and returns a new RDD representing the results.
- **Reduction (`reduce`)** is an action that aggregates all elements of an RDD using a function and returns the final result to the program.

### Lazy Transformations

- All transformations in Spark are lazy, meaning they do not compute their results immediately. Instead, they remember the transformations applied to a base dataset (e.g., a file). Transformations are only computed when an action requires returning a result to the program. This design allows Spark to operate more efficiently. For instance, it can understand that the dataset created by a map operation will be used in a reduction and return only the reduced result to the driver, rather than the larger mapped dataset.

### Caching

- By default, each transformed RDD can be recomputed every time an action is run on it. However, you can persist an RDD in memory using the `persist` (or `cache`) method, in which case Spark will keep the elements around the cluster for much faster access the next time you query it. There is also support for persisting RDDs on disk or replicating them across multiple nodes.

## Example of Stream Operations

```java
import org.apache.spark.SparkConf;
import org.apache.spark.api.java.JavaRDD;
import org.apache.spark.api.java.JavaSparkContext;

public class Test1 {
    public static void main(String[] args) {
        String appName = "Spark test 1";
        String master = "local"; // "local[*]";
        SparkConf conf = new SparkConf().setAppName(appName).setMaster(master);
        try (JavaSparkContext sc = new JavaSparkContext(conf);) {
            JavaRDD<String> textLines = sc.textFile("data.txt");
            JavaRDD<Integer> lineLengths = textLines.map(s -> s.length());
            int totalLength = lineLengths.reduce((a, b) -> a + b);
            System.out.println(totalLength);
        }
    }
}
```

## Function Passing

- Working with Spark heavily relies on passing functions from your program to run on the cluster. In Java, functions are represented as classes implementing interfaces in the `org.apache.spark.api.java.function` package.
- There are two ways to create such functions:
  - Implementing the `Function` interface in a class, either as an anonymous inner class or a named one, and passing its instance to Spark.
  - Using lambda expressions to concisely define the implementation.

### Anonymous Function Passing

```java
JavaRDD<String> lines1 = sc.textFile("data.txt");
JavaRDD<Integer> lineLengths1 = lines1.map(new Function<String, Integer>() {
    public Integer call(String s) { return s.length(); }
});
int totalLength1 = lineLengths1.reduce(new Function2<Integer, Integer, Integer>() {
    public Integer call(Integer a, Integer b) { return a + b; }
});
System.out.println(totalLength1);
```

### Named Function Passing

```java
static class GetLength implements Function<String, Integer> {
    public Integer call(String s) {
        return s.length();
    }
}
static class Sum implements Function2<Integer, Integer, Integer> {
    public Integer call(Integer a, Integer b) {
        return a + b;
    }
}
JavaRDD<String> lines2 = sc.textFile("data.txt");
JavaRDD<Integer> lineLengths2 = lines2.map(new GetLength());
int totalLength2 = lineLengths2.reduce(new Sum());
System.out.println(totalLength2);
```

### Lambda Function Passing

```java
JavaRDD<String> textLines = sc.textFile("data.txt");
JavaRDD<Integer> lineLengths = textLines.map(s -> s.length());
int totalLength = lineLengths.reduce((a, b) -> a + b);
System.out.println(totalLength);
```

## Operation Descriptions

| Operation            | Description                                        |
|----------------------|----------------------------------------------------|
| `map(func)`          | Maps input elements to output elements             |
| `filter(func)`       | Filters elements based on a predicate              |
| `flatMap(func)`      | Maps input elements to an output stream            |
| `mapToPair(func)`    | Maps input elements to output pairs                |
| `flatMapToPair(func)`| Maps input elements to an output stream of pairs   |
| `groupBy(func)`      | Groups elements into groups                        |
| `union(otherDataset)`| Returns the union of two datasets                  |
| `intersection(otherDataset)`| Returns the intersection of two datasets   |
| `distinct([numPartitions])` | Eliminates duplicates using equals          |
...