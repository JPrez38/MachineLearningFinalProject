package main

import com.github.tototoshi.csv._

object DataMerge {
	def readCSV(csvFile: String) = {
		csv3()
		//csv1()
	}

	def csv3() = {
		import java.io._
		val reader = CSVReader.open(new File("data/out.csv"))
		var country_year = Map[String,Map[String,List[Any]]]()
		for (x <- reader) {
			var tmpList = List[Any]()
			for (i <- 2 to 12) {
				tmpList = x(i) :: tmpList
			}
			tmpList = tmpList.reverse
			var tmpMap = country_year.getOrElse(x(0),Map[String,List[Any]]())
			tmpMap += x(1) -> tmpList
			country_year += x(0) -> tmpMap
		}

		val tmp = country_year.getOrElse("Andorra",null)
		println(tmp)
		val tmpyear = tmp.getOrElse("2003",List[Any]())
		tmpyear.foreach(x => println(x))
	
	}

	def csv2() = {
		import java.io._
		val reader = CSVReader.open(new File("data/out.csv"))
		var set = Set[Any]()
		for (x <- reader) {
			set = set + x(0)
		}
		set.foreach(i => println(i))
		println(set.size)
	}

	def csv1() = {
		import java.io._
		var country_year = Map[(String,Int),Double]()
		val reader = CSVReader.open(new File("data/totalbirths.csv"))
		for (x <- reader) {
			val str = x(4).replaceAll("\\D+",",")
			val y = str.split(",")
			if (y.length > 1 && y(1) != " " && y(1).toInt < 20){
			//if (y(1).toInt < 20) {
				var tmp = (x(0),x(1).toInt)
				var count = country_year.getOrElse(tmp,0.0)
				count += x(8).toDouble
				country_year += tmp -> count
				//println(x(0) + "," + x(1) + "," + x(4) + "," + x(8))
			}
			//}
		}
		
		//country_year.foreach(x => println(x))
		val x = country_year.toList.sortBy(_._1)
		var outList = List[List[Any]]()
		for (y <- x) {
			var tmp = List(y._1._1,y._1._2,0,0,0,0,0,0,0,0,0,0,y._2)
			//tmp.foreach(i => println(i))
			outList = tmp :: outList
		}
		//outList.foreach(u => println(u))
		outList = outList.reverse
		reader.close()

		val f = new File("data/out.csv")
		val writer = CSVWriter.open(f)
		writer.writeAll(outList)
		writer.close()
	}
}