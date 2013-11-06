package main

import com.github.tototoshi.csv._

object DataMerge {
	var country_year = Map[String,Map[String,List[Any]]]()
	def readCSV(csvFile: String) = {
		loadCSV()
		//csv3()
		//csv1()
		csv4()
		output()
	}

	def loadCSV() = {
		import java.io._
		val reader = CSVReader.open(new File("data/out1.csv"))
		
		for (x <- reader) {
			var tmpList = List[Any]()
			for (i <- 1 to x.size-1) {
				tmpList = x(i) :: tmpList
			}
			tmpList = tmpList.reverse
			var tmpMap = country_year.getOrElse(x(0),Map[String,List[Any]]())
			tmpMap += x(1) -> tmpList
			country_year += x(0) -> tmpMap
		}
		//val reader2 = CSVReader.open(new File("data/"))
		val tmp = country_year.getOrElse("Andorra",null)
		//println(tmp)
		val tmpyear = tmp.getOrElse("2003",List[Any]())
		//tmpyear.foreach(x => println(x))
	
	}

	def csv4() = {
		import java.io._
		val reader = CSVReader.open(new File("data/adultliteracyrate.csv"))
		for (x <- reader) {
			var maleRate = ""
			var femaleRate = ""
			var tmpMap = country_year.getOrElse(x(0),Map[String,List[Any]]())
			val newList = List("x","x","x","x","x","x","x","x","x","x","x","x")
			var tmpYear = tmpMap.getOrElse(x(1),newList)
			if (x(2)=="Male"){
				tmpYear = tmpYear.updated(4,x(3))
				maleRate = x(3)
			} else {
 				tmpYear = tmpYear.updated(3,x(3))
				femaleRate = x(3)
			}
			//println(tmpYear)
			tmpMap += x(1) -> tmpYear
			/*
			for (j <- tmpMap) {
				var newJ2 = j._2
				if (maleMin != "" && j._2(2)=="x") {
					newJ2 = j._2.updated(2,maleMin)
				} 
				if (femaleMin != "" && j._2(1)=="x") {
					newJ2 = j._2.updated(1,femaleMin)
				}
				tmpMap += j._1 -> newJ2
			}*/
			country_year += x(0) -> tmpMap

		}
		
		reader.close()
	}

	def csv3() = {
		import java.io._
		val reader = CSVReader.open(new File("data/minmarriageage.csv"))
		for (x <- reader) {
			var maleMin = ""
			var femaleMin = ""
			var tmpMap = country_year.getOrElse(x(0),Map[String,List[Any]]())
			val newList = List("x","x","x","x","x","x","x","x","x","x","x","x")
			var tmpYear = tmpMap.getOrElse(x(2),newList)
			if (x(1)=="Male"){
				tmpYear = tmpYear.updated(2,x(3))
				maleMin = x(3)
			} else {
 				tmpYear = tmpYear.updated(1,x(3))
				femaleMin = x(3)
			}
			//println(tmpYear)
			tmpMap += x(2) -> tmpYear
			
			for (j <- tmpMap) {
				var newJ2 = j._2
				if (maleMin != "" && j._2(2)=="x") {
					newJ2 = j._2.updated(2,maleMin)
				} 
				if (femaleMin != "" && j._2(1)=="x") {
					newJ2 = j._2.updated(1,femaleMin)
				}
				tmpMap += j._1 -> newJ2
			}
			country_year += x(0) -> tmpMap

		}
		
		//outList.foreach(j => println(j))
		reader.close()
	}

	def output() = {
		import java.io._
		val x = country_year.toList.sortBy(_._1)
		var outList = List[List[Any]]()
		for (y <- x) {
			var tmpList = List[List[Any]]()
			for (j <- y._2) {
				var tmp = List[Any]()
				tmp = y._1 :: tmp
				tmp = j._1 :: tmp
				for (h <- 1 to j._2.size-1) {
					tmp = j._2(h) :: tmp
				}
				tmp = tmp.reverse
				tmpList = tmp :: tmpList
			}
			//tmpList.foreach(a => println(a))
			tmpList = tmpList.sortBy(w => w(1).toString.toInt)
			tmpList = tmpList.reverse
		
			outList = tmpList ::: outList
			//tmp.foreach(i => println(i))
			//outList = tmp :: outList
		}

		//outList.foreach(u => println(u))
		outList = outList.reverse
		//outList.foreach(u => println(u))

		val f = new File("data/out2.csv")
		val writer = CSVWriter.open(f)
		writer.writeAll(outList)
		writer.close()
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
			var tmp = List[Any]()
			tmp = y._1._1 :: tmp
			tmp = y._1._2 :: tmp
			for (i <- 1 to 11) {
				tmp = 'x' :: tmp
			}
			tmp = y._2 :: tmp
			tmp = tmp.reverse
			
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