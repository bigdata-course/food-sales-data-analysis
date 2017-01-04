import org.apache.spark.SparkConf
import org.apache.spark.SparkContext
import org.apache.spark.mllib.linalg.Vectors
import org.apache.spark.mllib.clustering.KMeans

object kmeans extends App {

    val conf = new SparkConf()
    conf.setAppName("K-Means 1")

    val sc = new SparkContext(conf)
    val rawtxt = sc.textFile("/Users/emma/Work/bigData/code/Hotel/data2/hotel_result")

    // 将文本文件的内容转化为 Double 类型的 Vector 集合
    val allData = rawtxt.map {
        line =>
            Vectors.dense(line.split(',').map(_.toDouble))
    }

    // 由于 K-Means 算法是迭代计算，这里把数据缓存起来（广播变量）
    allData.cache()
    // 分为 5 个子集，最多100次迭代
    val kMeansModel = KMeans.train(allData, 5, 100)
    // 输出每个子集的质心
    kMeansModel.clusterCenters.foreach { println }

    val kMeansCost = kMeansModel.computeCost(allData)
    // 输出本次聚类操作的收敛性，此值越低越好
    println("K-Means Cost: " + kMeansCost)

    // 输出每组数据及其所属的子集索引
    allData.foreach {
        vec =>
            println(kMeansModel.predict(vec) + ": " + vec)
    }

}
