package main

import com.github.tototoshi.csv._
import scala.math._

object DataMerge {
	var country_year = Map[String,Map[String,List[Any]]]()
	val inFile = "data/out13.csv"
	val outFile = "data/out14.csv"
	var listLength = 0
	var totalChange = 0.0
	var changeCount = 0
	val changeAmount = .8434602024019697 //avg change by year under 98%
	def readCSV(csvFile: String) = {
		//fixBrokenCountries()
		loadCSV()
		var tmpMap = country_year.getOrElse("Uruguay",Map[String,List[Any]]())
		var tmp = tmpMap.getOrElse("2005",List[Any]())
		listLength = tmp.size
		patchLiteracyRates()
		//getLiteracyRates()
		//removeNotEnoughData(2)
		//fixMinMarriageAge()
		//csv8()
		//csv5()
		//csv3()
		//getTotalCountries()
		//csv1()
		//csv4()
		//println(totalChange/changeCount)
		//output()
	}

	def patchLiteracyRates() {
		for (x <- country_year) {
			var country = country_year.getOrElse(x._1,Map[String,List[Any]]())
			var femaleLitRates = List[(Int,Double)]()
			var maleLitRates = List[(Int,Double)]()
			for (y <- x._2){
				if(y._2(3)!= "x") {
					var lityear = (y._2(0).toString.toInt,y._2(3).toString.toDouble)
					femaleLitRates = lityear :: femaleLitRates
					//println(lityear)
				}
				if(y._2(4)!= "x") {
					var lityear = (y._2(0).toString.toInt,y._2(4).toString.toDouble)
					maleLitRates = lityear :: maleLitRates
				}
			}
			femaleLitRates = femaleLitRates.sortBy(_._1)
			maleLitRates = maleLitRates.sortBy(_._1)
			if(femaleLitRates.size == 1) {
				if (femaleLitRates(0)._2 > 98.0) {
					var constantlit = femaleLitRates(0)._2
					//println(x._1 + "," + j._1 + "," + j._2)
					for (y <- x._2){
						if (y._2(3) == "x") {
							var lityear = (y._2(0).toString.toInt,constantlit)
							femaleLitRates = lityear :: femaleLitRates
						}
					}
				} else {
					var constantlit = femaleLitRates(0)._2
					val startYear = femaleLitRates(0)._1
					for (r <- startYear-3 to startYear+3) {
						
						val deltaYear = r - startYear
						if (deltaYear != 0) {
							var change = deltaYear * changeAmount
							var lityear = (r,constantlit + change)
							femaleLitRates = lityear :: femaleLitRates
						}
					}
					//println(x._1 + "," + j._1 + "," + j._2)
				}
			} else if (femaleLitRates.size > 1) {
				val change= femaleLitRates(femaleLitRates.size-1)._2-femaleLitRates(0)._2
				val span = femaleLitRates(femaleLitRates.size-1)._1-femaleLitRates(0)._1
				val avgChange = change/span
		
				//println(avgChange)
				if (femaleLitRates(femaleLitRates.size-1)._2 < 98) {
					totalChange += avgChange
					changeCount+= 1
				} 
				var newFemaleLitRates = femaleLitRates
				for (k <- 1 to femaleLitRates.size-1) {
					val change = femaleLitRates(k)._2 - femaleLitRates(k-1)._2
					val changeYear = femaleLitRates(k)._1 - femaleLitRates(k-1)._1
					val delta = change/changeYear
					for( g <- femaleLitRates(k-1)._1+1 to femaleLitRates(k)._1-1) {
						val deltaYear = g - femaleLitRates(k-1)._1
						var change = deltaYear * delta
						var lityear = (g,femaleLitRates(k-1)._2 + change)
						newFemaleLitRates = lityear :: newFemaleLitRates
					}
				} 
				femaleLitRates = newFemaleLitRates
				femaleLitRates = femaleLitRates.sortBy(_._1)
				val beg = femaleLitRates(0)._1
				val end = femaleLitRates(femaleLitRates.size-1)._1
				val begVal = femaleLitRates(0)._2
				val endVal = femaleLitRates(femaleLitRates.size-1)._2
				for (e <- beg-3 to beg-1) {
					val deltaYear = e - beg
					var change = deltaYear * avgChange
					var newVal = begVal + change
					if (newVal > 99) {
						newVal = 99
					}
					if (newVal > 10 && avgChange < 2) {
						var lityear = (e,newVal)
						femaleLitRates = lityear :: femaleLitRates
					}
				}
				if (x._1 == "Cameroon") {
					//println(avgChange)
				}
				if (avgChange > 2) {
					//println(avgChange + "," + x._1)
				}
					
				for (e <- end+1 to end +3) {
					val deltaYear = e - end
					var change = deltaYear * avgChange
					var newVal = endVal + change
					if (newVal > 99) {
						newVal = 99
					}
					if (newVal > 10 && avgChange < 2) {
						var lityear = (e,newVal)
						femaleLitRates = lityear :: femaleLitRates
					}
				}
			}
			femaleLitRates = femaleLitRates.sortBy(_._1)
			if (x._1 == "Nepal") {
				femaleLitRates.foreach(x => println(x))
			}

			/*
			for (y <- x._2) {
				var tmpMap = country.getOrElse(y._1,List[Any]())
				if (tmpMap(1) == "x") {
					tmpMap = tmpMap.updated(1,femaleAge)
				}
				if (tmpMap(2) == "x") {
					tmpMap = tmpMap.updated(2,maleAge)
				}
				country += y._1 -> tmpMap	
			}
			country_year += x._1 -> country*/
		}
	}

	def removeNotEnoughData(min:Int) {
		for (x <- country_year) {
			var country = country_year.getOrElse(x._1,Map[String,List[Any]]())
			var femaleAge = "x"
			var maleAge = "x"
			for (y <- x._2){
				var count = 0
				for (i <- 1 to y._2.size-1) {
					if(y._2(1)!= "x") {
						count+=1
					}
				}
				if (count < min) {
					println(x._1 + " " + y._1)
					country -= y._1
				}
			}
			country_year += x._1 -> country
		}
	}

	def fixMinMarriageAge() {
		for (x <- country_year) {
			var country = country_year.getOrElse(x._1,Map[String,List[Any]]())
			var femaleAge = "x"
			var maleAge = "x"
			for (y <- x._2){
				if(y._2(1)!= "x") {
					femaleAge=y._2(1).toString
				}
				if(y._2(2)!= "x") {
					maleAge=y._2(2).toString
				}
			}
			for (y <- x._2) {
				var tmpMap = country.getOrElse(y._1,List[Any]())
				if (tmpMap(1) == "x") {
					tmpMap = tmpMap.updated(1,femaleAge)
				}
				if (tmpMap(2) == "x") {
					tmpMap = tmpMap.updated(2,maleAge)
				}
				country += y._1 -> tmpMap	
			}
			country_year += x._1 -> country
		}
	}

	def fixBrokenCountries() {
		import java.io._
		val reader = CSVReader.open(new File(inFile))
		
		for (x <- reader) {
			var tmpList = List[Any]()
			for (i <- 1 to x.size-1) {
				tmpList = x(i) :: tmpList
			}
			tmpList = tmpList.reverse
			var tmpMap = country_year.getOrElse(x(0),Map[String,List[Any]]())
			var newList = List[Any]()
			for (i <- 0 to 13) {
				newList = "x" :: newList
			}
			var tmp2List = tmpMap.getOrElse(x(1),newList)
			for (i <- 0 to tmpList.length-1) {
				if (tmp2List(i).toString=="x") {
					tmp2List = tmp2List.updated(i,tmpList(i))
				}
			}
			tmpMap += x(1) -> tmp2List
			country_year += x(0) -> tmpMap
		}
		//val reader2 = CSVReader.open(new File("data/"))
		val tmp = country_year.getOrElse("Andorra",null)
		//println(tmp)
		val tmpyear = tmp.getOrElse("2003",List[Any]())
		//tmpyear.foreach(x => println(x))
	}

	def csv8() = {
		import java.io._
		val reader = CSVReader.open(new File("data/femalemaleratio.csv"))
		for (x <- reader) {
			var maleRate = ""
			var femaleRate = ""
			var tmpMap = country_year.getOrElse(x(0),Map[String,List[Any]]())
			val newList = List("x","x","x","x","x","x","x","x","x","x","x","x","x","x")
			if (x(1)!="") {
				var tmpYear = tmpMap.getOrElse(x(1),newList)
				tmpYear = tmpYear.updated(12,x(2))
				
				tmpMap += x(1) -> tmpYear
				country_year += x(0) -> tmpMap
			}
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
			

		}
	}
	def csv7() = {
		import java.io._
		val reader = CSVReader.open(new File("data/womensshareoflabourforce.csv"))
		for (x <- reader) {
			var maleRate = ""
			var femaleRate = ""
			var tmpMap = country_year.getOrElse(x(0),Map[String,List[Any]]())
			val newList = List("x","x","x","x","x","x","x","x","x","x","x","x","x","x")
			if (x(1)!="") {
				var tmpYear = tmpMap.getOrElse(x(1),newList)
				tmpYear = tmpYear.updated(11,x(2))
				
				tmpMap += x(1) -> tmpYear
				country_year += x(0) -> tmpMap
			}
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
			

		}
		
		reader.close()
	}

	def loadCSV() = {
		import java.io._
		val reader = CSVReader.open(new File(inFile))
		
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

	def csv6() = {
		import java.io._
		val reader = CSVReader.open(new File("data/marriageage.csv"))
		for (x <- reader) {
			var maleRate = ""
			var femaleRate = ""
			var tmpMap = country_year.getOrElse(x(0),Map[String,List[Any]]())
			val newList = List("x","x","x","x","x","x","x","x","x","x","x","x","x","x")
			if (x(1)!="") {
				var tmpYear = tmpMap.getOrElse(x(1),newList)
				if (x(2)=="Men"){
					tmpYear = tmpYear.updated(8,x(3))
					tmpYear = tmpYear.updated(10,x(4))
					maleRate = x(3)
				} else {
 					tmpYear = tmpYear.updated(7,x(3))
 					tmpYear = tmpYear.updated(9,x(4))
					femaleRate = x(3)
				}
				//println(x(1))
				tmpMap += x(1) -> tmpYear
				country_year += x(0) -> tmpMap
			}
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
			

		}
		
		reader.close()
	}

	def csv5() {
				import java.io._
		val reader = CSVReader.open(new File("data/contraceptiveprevalencemethod.csv"))
		for (x <- reader) {
			var maleRate = ""
			var femaleRate = ""
			var tmpMap = country_year.getOrElse(x(0),Map[String,List[Any]]())
			val newList = List("x","x","x","x","x","x","x","x","x","x","x","x")
			if (x(1)!="") {
				var tmpYear = tmpMap.getOrElse(x(1),newList)
				tmpYear = tmpYear.updated(6,x(2))
 				tmpYear = tmpYear.updated(5,x(3))
				//println(x(1))
				tmpMap += x(1) -> tmpYear
				country_year += x(0) -> tmpMap
			}
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
			

		}
		
		reader.close()
	}

	def getLiteracyRates() = {
		import java.io._
		val reader = CSVReader.open(new File("data/literacyrate.csv"))
		for (x <- reader) {
			var maleRate = ""
			var femaleRate = ""
			var tmpMap = country_year.getOrElse(x(0),Map[String,List[Any]]())
			var newList = List[Any]()
			for(i <- 1 to listLength) {
				newList = "x" :: newList
			}
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

		val f = new File(outFile)
		val writer = CSVWriter.open(f)
		writer.writeAll(outList)
		writer.close()
	}

	def getTotalCountries() = {
		import java.io._
		val reader = CSVReader.open(new File(inFile))
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