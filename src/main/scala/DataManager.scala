package main

import com.github.tototoshi.csv._
import scala.math._

object DataMerge {
	var country_year = Map[String,Map[String,List[Any]]]()
	val inFile = "data/out24.csv"
	val outFile = "data/normaldata.csv"
	var listLength = 0
	var totalChange = 0.0
	var changeCount = 0
	val changeAmount = .8434602024019697 //avg change by year under 98%
	val contraceptiveChangeAmount = 0.6527541387052763
	val teansMarriedChangeAmount = -0.16619477398381088
	val marriedAgeChangeAmount = 0.10122822640700432
	val womensShareChangeAmount = 0.13282134532134532
	val maleFemaleChangeAmount = 0.006712239642299642
	def readCSV(csvFile: String) = {
		//fixBrokenCountries()
		loadCSV()
		var tmpMap = country_year.getOrElse("Uruguay",Map[String,List[Any]]())
		var tmp = tmpMap.getOrElse("2005",List[Any]())
		listLength = tmp.size
		elim()
		//patchLiteracyRates("female")
		//patchLiteracyRates("male")
		//patchContreceptiveRate("female")
		//patchContreceptiveRate("male")
		//fixWeirdChar()
		//patchTeensMarried("female")
		//patchTeensMarried("male")
		//patchWomensShareOfLaborForce()
		//patchfemaleMaleRatio()
		//addFemalePop()
		//normalizeOutput()
		//fullData()
		//outputs()
		//possibles()
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
		output()
	}

	def elim() {
		var total = 0
		for (x <- country_year) {
			var country = country_year.getOrElse(x._1,Map[String,List[Any]]())
			for (y <- country) {
				var add = true
				for (j <- y._2) {
					if (j == "x") {
						add = false
						country -= y._1
					}
				}
				if (add == true) {
					total += 1
					//println(x._1 +  "," + y)
				}

			}
			country_year += x._1 -> country
		}
		//println(total)
	}

	def normalizeOutput() {
		for (x <- country_year) {
			var country = country_year.getOrElse(x._1,Map[String,List[Any]]())
			for (y <- country) {
				//println(y)
				if (y._2(y._2.size-1) != "x" && y._2(y._2.size-2) != "x") {
					val normal = y._2(y._2.size-2).toString.toDouble/y._2(y._2.size-1).toString.toDouble
					val newList = y._2 ::: List(normal)
					country += y._1 -> newList
				} else {
					val newList = y._2 ::: List("x")
					country += y._1 -> newList
				}

			}
			country_year += x._1 -> country
		}
	}

	def addFemalePop() = {
		import java.io._
		val reader = CSVReader.open(new File("data/femalepop.csv"))
		val startYear = 1950

		var set = Set[String]()
		for (x <- reader) {
			var country = country_year.getOrElse(x(0),Map[String,List[Any]]())
			if (country.size != 0) {
				for (y <- 1 to x.length-1) {
					val year = startYear + y - 1
					var j = country.getOrElse(year.toString,List[Any]())
					//var newList = List(x(y).replaceAll(" ",""))
					if (j.size != 0) {
						val num = ((x(y).replaceAll(" ","").toInt)*1000).toString
						j = j ::: List(num)
						country += year.toString -> j
					}
				}
				country_year += x(0) -> country
			}

		}
		//set.foreach(i => println(i))
		//println(set.size)
		//println(country_year.size)
		var sum = 0
		for (x <- set) {
			if (country_year.getOrElse(x,None) != None) {
				sum += 1
			}
		}
		for (x <- country_year) {
			if (!set.contains(x._1)) {
				//println(x._1)
			}
		}
		//println(sum)
	}

	def patchfemaleMaleRatio() {
		val threshold = 200.0
		val yearSpan = 7
		val maxChange = 2
		val minThreshold =.01
		var a = 12
		for (x <- country_year) {
			var country = country_year.getOrElse(x._1,Map[String,List[Any]]())
			var litRates = List[(Int,Double)]()
			var maleLitRates = List[(Int,Double)]()
			for (y <- x._2){
				if(y._2(a)!= "x") {
					var lityear = (y._2(0).toString.toInt,y._2(a).toString.toDouble)
					litRates = lityear :: litRates
					//println(lityear)
				}
			}
			litRates = litRates.sortBy(_._1)
			if(litRates.size == 1) {
				if (litRates(0)._2 > threshold) {
					var constantlit = litRates(0)._2
					//println(x._1 + "," + j._1 + "," + j._2)
					for (y <- x._2){
						if (y._2(a) == "x") {
							var lityear = (y._2(0).toString.toInt,constantlit)
							litRates = lityear :: litRates
						}
					}
				} else {
					var constantlit = litRates(0)._2
					val startYear = litRates(0)._1
					for (r <- startYear-yearSpan to startYear+yearSpan) {
						
						val deltaYear = r - startYear
						if (deltaYear != 0) {
							var change = deltaYear * maleFemaleChangeAmount
							var lityear = (r,constantlit + change)
							litRates = lityear :: litRates
						}
					}
					//println(x._1 + "," + j._1 + "," + j._2)
				}
			} else if (litRates.size > 1) {
				val change= litRates(litRates.size-1)._2-litRates(0)._2
				val span = litRates(litRates.size-1)._1-litRates(0)._1
				var avgChange = change/span
		
				//println(avgChange)
				if (litRates(litRates.size-1)._2 < threshold) {
					totalChange += avgChange
					changeCount+= 1
				} 
				var newlitRates = litRates
				for (k <- 1 to litRates.size-1) {
					val change = litRates(k)._2 - litRates(k-1)._2
					val changeYear = litRates(k)._1 - litRates(k-1)._1
					val delta = change/changeYear
					for( g <- litRates(k-1)._1+1 to litRates(k)._1-1) {
						val deltaYear = g - litRates(k-1)._1
						var change = deltaYear * delta
						var lityear = (g,litRates(k-1)._2 + change)
						newlitRates = lityear :: newlitRates
					}
				} 
				litRates = newlitRates
				litRates = litRates.sortBy(_._1)
				val beg = litRates(0)._1
				val end = litRates(litRates.size-1)._1
				val begVal = litRates(0)._2
				val endVal = litRates(litRates.size-1)._2
				for (e <- beg-yearSpan to beg-1) {
					val deltaYear = e - beg
					var change = deltaYear * avgChange
					var newVal = begVal + change
					if (newVal > 99) {
						newVal = 99
					}
					if (avgChange > maxChange) {
						avgChange = maxChange-.01
					}
					if (newVal < minThreshold) {
						//newVal = minThreshold +.01
					}
					if (newVal > minThreshold && avgChange < maxChange) {
						var lityear = (e,newVal)
						litRates = lityear :: litRates
					}
				}
				if (x._1 == "Cameroon") {
					//println(avgChange)
				}
				if (avgChange > maxChange) {
					println(avgChange + "," + x._1)
				}
					
				for (e <- end+1 to end +yearSpan) {
					val deltaYear = e - end
					var change = deltaYear * avgChange
					var newVal = endVal + change
					if (newVal >= 100.0) {
						newVal = 100.0
					}
					if (newVal < minThreshold) {
						newVal = minThreshold +.01
					}
					if (newVal > minThreshold && avgChange < maxChange) {
						var lityear = (e,newVal)
						litRates = lityear :: litRates
					}
				}
			}
			litRates = litRates.sortBy(_._1)
			if (x._1 == "Nepal") {
				//litRates.foreach(x => println(x))
			}
			for( y <- litRates) {
				var lit_year = country.getOrElse(y._1.toString,List[Any]())
				if (lit_year.size != 0 && lit_year(a) == "x") {
					if (x._1 == "Nepal") {
						//println(y._1.toString)
					}
					lit_year = lit_year.updated(a,y._2)
					country += y._1.toString -> lit_year
				}
			}
			country_year += x._1 -> country

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

	def patchWomensShareOfLaborForce() {
		val threshold = 98.0
		val yearSpan = 7
		val maxChange = 2
		val minThreshold =.01
		var a = 11
		for (x <- country_year) {
			var country = country_year.getOrElse(x._1,Map[String,List[Any]]())
			var litRates = List[(Int,Double)]()
			var maleLitRates = List[(Int,Double)]()
			for (y <- x._2){
				if(y._2(a)!= "x") {
					var lityear = (y._2(0).toString.toInt,y._2(a).toString.toDouble)
					litRates = lityear :: litRates
					//println(lityear)
				}
			}
			litRates = litRates.sortBy(_._1)
			if(litRates.size == 1) {
				if (litRates(0)._2 > threshold) {
					var constantlit = litRates(0)._2
					//println(x._1 + "," + j._1 + "," + j._2)
					for (y <- x._2){
						if (y._2(a) == "x") {
							var lityear = (y._2(0).toString.toInt,constantlit)
							litRates = lityear :: litRates
						}
					}
				} else {
					var constantlit = litRates(0)._2
					val startYear = litRates(0)._1
					for (r <- startYear-yearSpan to startYear+yearSpan) {
						
						val deltaYear = r - startYear
						if (deltaYear != 0) {
							var change = deltaYear * womensShareChangeAmount
							var lityear = (r,constantlit + change)
							litRates = lityear :: litRates
						}
					}
					//println(x._1 + "," + j._1 + "," + j._2)
				}
			} else if (litRates.size > 1) {
				val change= litRates(litRates.size-1)._2-litRates(0)._2
				val span = litRates(litRates.size-1)._1-litRates(0)._1
				var avgChange = change/span
		
				//println(avgChange)
				if (litRates(litRates.size-1)._2 < threshold) {
					totalChange += avgChange
					changeCount+= 1
				} 
				var newlitRates = litRates
				for (k <- 1 to litRates.size-1) {
					val change = litRates(k)._2 - litRates(k-1)._2
					val changeYear = litRates(k)._1 - litRates(k-1)._1
					val delta = change/changeYear
					for( g <- litRates(k-1)._1+1 to litRates(k)._1-1) {
						val deltaYear = g - litRates(k-1)._1
						var change = deltaYear * delta
						var lityear = (g,litRates(k-1)._2 + change)
						newlitRates = lityear :: newlitRates
					}
				} 
				litRates = newlitRates
				litRates = litRates.sortBy(_._1)
				val beg = litRates(0)._1
				val end = litRates(litRates.size-1)._1
				val begVal = litRates(0)._2
				val endVal = litRates(litRates.size-1)._2
				for (e <- beg-yearSpan to beg-1) {
					val deltaYear = e - beg
					var change = deltaYear * avgChange
					var newVal = begVal + change
					if (newVal > 99) {
						newVal = 99
					}
					if (avgChange > maxChange) {
						avgChange = maxChange-.01
					}
					if (newVal < minThreshold) {
						//newVal = minThreshold +.01
					}
					if (newVal > minThreshold && avgChange < maxChange) {
						var lityear = (e,newVal)
						litRates = lityear :: litRates
					}
				}
				if (x._1 == "Cameroon") {
					//println(avgChange)
				}
				if (avgChange > maxChange) {
					println(avgChange + "," + x._1)
				}
					
				for (e <- end+1 to end +yearSpan) {
					val deltaYear = e - end
					var change = deltaYear * avgChange
					var newVal = endVal + change
					if (newVal >= 100.0) {
						newVal = 100.0
					}
					if (newVal < minThreshold) {
						newVal = minThreshold +.01
					}
					if (newVal > minThreshold && avgChange < maxChange) {
						var lityear = (e,newVal)
						litRates = lityear :: litRates
					}
				}
			}
			litRates = litRates.sortBy(_._1)
			if (x._1 == "Nepal") {
				//litRates.foreach(x => println(x))
			}
			for( y <- litRates) {
				var lit_year = country.getOrElse(y._1.toString,List[Any]())
				if (lit_year.size != 0 && lit_year(a) == "x") {
					if (x._1 == "Nepal") {
						//println(y._1.toString)
					}
					lit_year = lit_year.updated(a,y._2)
					country += y._1.toString -> lit_year
				}
			}
			country_year += x._1 -> country

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


	def patchMarriageAge(male_female:String) {
		val threshold = 98.0
		val yearSpan = 7
		val maxChange = 2
		val minThreshold =.01
		var a = 0
		if (male_female == "male") {
			a = 10
		} else if (male_female == "female") {
			a = 9
		} else {
			return
		}
		for (x <- country_year) {
			var country = country_year.getOrElse(x._1,Map[String,List[Any]]())
			var litRates = List[(Int,Double)]()
			var maleLitRates = List[(Int,Double)]()
			for (y <- x._2){
				if(y._2(a)!= "x") {
					var lityear = (y._2(0).toString.toInt,y._2(a).toString.toDouble)
					litRates = lityear :: litRates
					//println(lityear)
				}
			}
			litRates = litRates.sortBy(_._1)
			if(litRates.size == 1) {
				if (litRates(0)._2 > threshold) {
					var constantlit = litRates(0)._2
					//println(x._1 + "," + j._1 + "," + j._2)
					for (y <- x._2){
						if (y._2(a) == "x") {
							var lityear = (y._2(0).toString.toInt,constantlit)
							litRates = lityear :: litRates
						}
					}
				} else {
					var constantlit = litRates(0)._2
					val startYear = litRates(0)._1
					for (r <- startYear-yearSpan to startYear+yearSpan) {
						
						val deltaYear = r - startYear
						if (deltaYear != 0) {
							var change = deltaYear * marriedAgeChangeAmount
							var lityear = (r,constantlit + change)
							litRates = lityear :: litRates
						}
					}
					//println(x._1 + "," + j._1 + "," + j._2)
				}
			} else if (litRates.size > 1) {
				val change= litRates(litRates.size-1)._2-litRates(0)._2
				val span = litRates(litRates.size-1)._1-litRates(0)._1
				var avgChange = change/span
		
				//println(avgChange)
				if (litRates(litRates.size-1)._2 < threshold) {
					totalChange += avgChange
					changeCount+= 1
				} 
				var newlitRates = litRates
				for (k <- 1 to litRates.size-1) {
					val change = litRates(k)._2 - litRates(k-1)._2
					val changeYear = litRates(k)._1 - litRates(k-1)._1
					val delta = change/changeYear
					for( g <- litRates(k-1)._1+1 to litRates(k)._1-1) {
						val deltaYear = g - litRates(k-1)._1
						var change = deltaYear * delta
						var lityear = (g,litRates(k-1)._2 + change)
						newlitRates = lityear :: newlitRates
					}
				} 
				litRates = newlitRates
				litRates = litRates.sortBy(_._1)
				val beg = litRates(0)._1
				val end = litRates(litRates.size-1)._1
				val begVal = litRates(0)._2
				val endVal = litRates(litRates.size-1)._2
				for (e <- beg-yearSpan to beg-1) {
					val deltaYear = e - beg
					var change = deltaYear * avgChange
					var newVal = begVal + change
					if (newVal > 99) {
						newVal = 99
					}
					if (avgChange > maxChange) {
						avgChange = maxChange-.01
					}
					if (newVal < minThreshold) {
						//newVal = minThreshold +.01
					}
					if (newVal > minThreshold && avgChange < maxChange) {
						var lityear = (e,newVal)
						litRates = lityear :: litRates
					}
				}
				if (x._1 == "Cameroon") {
					//println(avgChange)
				}
				if (avgChange > maxChange) {
					println(avgChange + "," + x._1)
				}
					
				for (e <- end+1 to end +yearSpan) {
					val deltaYear = e - end
					var change = deltaYear * avgChange
					var newVal = endVal + change
					if (newVal >= 100.0) {
						newVal = 100.0
					}
					if (newVal < minThreshold) {
						newVal = minThreshold +.01
					}
					if (newVal > minThreshold && avgChange < maxChange) {
						var lityear = (e,newVal)
						litRates = lityear :: litRates
					}
				}
			}
			litRates = litRates.sortBy(_._1)
			if (x._1 == "Nepal") {
				//litRates.foreach(x => println(x))
			}
			for( y <- litRates) {
				var lit_year = country.getOrElse(y._1.toString,List[Any]())
				if (lit_year.size != 0 && lit_year(a) == "x") {
					if (x._1 == "Nepal") {
						//println(y._1.toString)
					}
					lit_year = lit_year.updated(a,y._2)
					country += y._1.toString -> lit_year
				}
			}
			country_year += x._1 -> country

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

	def patchTeensMarried(male_female:String) {
		val threshold = 98.0
		val yearSpan = 7
		val maxChange = 2
		val minThreshold =.01
		var a = 0
		if (male_female == "male") {
			a = 8
		} else if (male_female == "female") {
			a = 7
		} else {
			return
		}
		for (x <- country_year) {
			var country = country_year.getOrElse(x._1,Map[String,List[Any]]())
			var litRates = List[(Int,Double)]()
			var maleLitRates = List[(Int,Double)]()
			for (y <- x._2){
				if(y._2(a)!= "x") {
					var lityear = (y._2(0).toString.toInt,y._2(a).toString.toDouble)
					litRates = lityear :: litRates
					//println(lityear)
				}
			}
			litRates = litRates.sortBy(_._1)
			if(litRates.size == 1) {
				if (litRates(0)._2 > threshold) {
					var constantlit = litRates(0)._2
					//println(x._1 + "," + j._1 + "," + j._2)
					for (y <- x._2){
						if (y._2(a) == "x") {
							var lityear = (y._2(0).toString.toInt,constantlit)
							litRates = lityear :: litRates
						}
					}
				} else {
					var constantlit = litRates(0)._2
					val startYear = litRates(0)._1
					for (r <- startYear-yearSpan to startYear+yearSpan) {
						
						val deltaYear = r - startYear
						if (deltaYear != 0) {
							var change = deltaYear * teansMarriedChangeAmount
							var lityear = (r,constantlit + change)
							litRates = lityear :: litRates
						}
					}
					//println(x._1 + "," + j._1 + "," + j._2)
				}
			} else if (litRates.size > 1) {
				val change= litRates(litRates.size-1)._2-litRates(0)._2
				val span = litRates(litRates.size-1)._1-litRates(0)._1
				var avgChange = change/span
		
				//println(avgChange)
				if (litRates(litRates.size-1)._2 < threshold) {
					totalChange += avgChange
					changeCount+= 1
				} 
				var newlitRates = litRates
				for (k <- 1 to litRates.size-1) {
					val change = litRates(k)._2 - litRates(k-1)._2
					val changeYear = litRates(k)._1 - litRates(k-1)._1
					val delta = change/changeYear
					for( g <- litRates(k-1)._1+1 to litRates(k)._1-1) {
						val deltaYear = g - litRates(k-1)._1
						var change = deltaYear * delta
						var lityear = (g,litRates(k-1)._2 + change)
						newlitRates = lityear :: newlitRates
					}
				} 
				litRates = newlitRates
				litRates = litRates.sortBy(_._1)
				val beg = litRates(0)._1
				val end = litRates(litRates.size-1)._1
				val begVal = litRates(0)._2
				val endVal = litRates(litRates.size-1)._2
				for (e <- beg-yearSpan to beg-1) {
					val deltaYear = e - beg
					var change = deltaYear * avgChange
					var newVal = begVal + change
					if (newVal > 99) {
						newVal = 99
					}
					if (avgChange > maxChange) {
						avgChange = maxChange-.01
					}
					if (newVal < minThreshold) {
						//newVal = minThreshold +.01
					}
					if (newVal > minThreshold && avgChange < maxChange) {
						var lityear = (e,newVal)
						litRates = lityear :: litRates
					}
				}
				if (x._1 == "Cameroon") {
					//println(avgChange)
				}
				if (avgChange > maxChange) {
					println(avgChange + "," + x._1)
				}
					
				for (e <- end+1 to end +yearSpan) {
					val deltaYear = e - end
					var change = deltaYear * avgChange
					var newVal = endVal + change
					if (newVal >= 100.0) {
						newVal = 100.0
					}
					if (newVal < minThreshold) {
						newVal = minThreshold +.01
					}
					if (newVal > minThreshold && avgChange < maxChange) {
						var lityear = (e,newVal)
						litRates = lityear :: litRates
					}
				}
			}
			litRates = litRates.sortBy(_._1)
			if (x._1 == "Nepal") {
				//litRates.foreach(x => println(x))
			}
			for( y <- litRates) {
				var lit_year = country.getOrElse(y._1.toString,List[Any]())
				if (lit_year.size != 0 && lit_year(a) == "x") {
					if (x._1 == "Nepal") {
						//println(y._1.toString)
					}
					lit_year = lit_year.updated(a,y._2)
					country += y._1.toString -> lit_year
				}
			}
			country_year += x._1 -> country

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

	def patchContreceptiveRate(male_female:String) {
		val threshold = 98.0
		val yearSpan = 7
		val maxChange = 2
		val minThreshold =1.0
		var a = 0
		if (male_female == "male") {
			a = 6
		} else if (male_female == "female") {
			a = 5
		} else {
			return
		}
		for (x <- country_year) {
			var country = country_year.getOrElse(x._1,Map[String,List[Any]]())
			var litRates = List[(Int,Double)]()
			var maleLitRates = List[(Int,Double)]()
			for (y <- x._2){
				if(y._2(a)!= "x") {
					var lityear = (y._2(0).toString.toInt,y._2(a).toString.toDouble)
					litRates = lityear :: litRates
					//println(lityear)
				}
			}
			litRates = litRates.sortBy(_._1)
			if(litRates.size == 1) {
				if (litRates(0)._2 > threshold) {
					var constantlit = litRates(0)._2
					//println(x._1 + "," + j._1 + "," + j._2)
					for (y <- x._2){
						if (y._2(a) == "x") {
							var lityear = (y._2(0).toString.toInt,constantlit)
							litRates = lityear :: litRates
						}
					}
				} else {
					var constantlit = litRates(0)._2
					val startYear = litRates(0)._1
					for (r <- startYear-yearSpan to startYear+yearSpan) {
						
						val deltaYear = r - startYear
						if (deltaYear != 0) {
							var change = deltaYear * contraceptiveChangeAmount
							var lityear = (r,constantlit + change)
							litRates = lityear :: litRates
						}
					}
					//println(x._1 + "," + j._1 + "," + j._2)
				}
			} else if (litRates.size > 1) {
				val change= litRates(litRates.size-1)._2-litRates(0)._2
				val span = litRates(litRates.size-1)._1-litRates(0)._1
				var avgChange = change/span
		
				//println(avgChange)
				if (litRates(litRates.size-1)._2 < threshold) {
					totalChange += avgChange
					changeCount+= 1
				} 
				var newlitRates = litRates
				for (k <- 1 to litRates.size-1) {
					val change = litRates(k)._2 - litRates(k-1)._2
					val changeYear = litRates(k)._1 - litRates(k-1)._1
					val delta = change/changeYear
					for( g <- litRates(k-1)._1+1 to litRates(k)._1-1) {
						val deltaYear = g - litRates(k-1)._1
						var change = deltaYear * delta
						var lityear = (g,litRates(k-1)._2 + change)
						newlitRates = lityear :: newlitRates
					}
				} 
				litRates = newlitRates
				litRates = litRates.sortBy(_._1)
				val beg = litRates(0)._1
				val end = litRates(litRates.size-1)._1
				val begVal = litRates(0)._2
				val endVal = litRates(litRates.size-1)._2
				for (e <- beg-yearSpan to beg-1) {
					val deltaYear = e - beg
					var change = deltaYear * avgChange
					var newVal = begVal + change
					if (newVal > 99) {
						newVal = 99
					}
					if (avgChange > maxChange) {
						avgChange = maxChange-.01
					}
					if (newVal > minThreshold && avgChange < maxChange) {
						var lityear = (e,newVal)
						litRates = lityear :: litRates
					}
				}
				if (x._1 == "Cameroon") {
					//println(avgChange)
				}
				if (avgChange > maxChange) {
					println(avgChange + "," + x._1)
				}
					
				for (e <- end+1 to end +yearSpan) {
					val deltaYear = e - end
					var change = deltaYear * avgChange
					var newVal = endVal + change
					if (newVal >= 100.0) {
						newVal = 100.0
					}
					if (newVal > minThreshold && avgChange < maxChange) {
						var lityear = (e,newVal)
						litRates = lityear :: litRates
					}
				}
			}
			litRates = litRates.sortBy(_._1)
			if (x._1 == "Nepal") {
				//litRates.foreach(x => println(x))
			}
			for( y <- litRates) {
				var lit_year = country.getOrElse(y._1.toString,List[Any]())
				if (lit_year.size != 0 && lit_year(a) == "x") {
					if (x._1 == "Nepal") {
						//println(y._1.toString)
					}
					lit_year = lit_year.updated(a,y._2)
					country += y._1.toString -> lit_year
				}
			}
			country_year += x._1 -> country

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

	def patchLiteracyRates(male_female:String) {
		var a = 0
		if (male_female == "male") {
			a = 4
		} else if (male_female == "female") {
			a = 3
		} else {
			return
		}
		for (x <- country_year) {
			var country = country_year.getOrElse(x._1,Map[String,List[Any]]())
			var litRates = List[(Int,Double)]()
			var maleLitRates = List[(Int,Double)]()
			for (y <- x._2){
				if(y._2(a)!= "x") {
					var lityear = (y._2(0).toString.toInt,y._2(a).toString.toDouble)
					litRates = lityear :: litRates
					//println(lityear)
				}
			}
			litRates = litRates.sortBy(_._1)
			if(litRates.size == 1) {
				if (litRates(0)._2 > 98.0) {
					var constantlit = litRates(0)._2
					//println(x._1 + "," + j._1 + "," + j._2)
					for (y <- x._2){
						if (y._2(a) == "x") {
							var lityear = (y._2(0).toString.toInt,constantlit)
							litRates = lityear :: litRates
						}
					}
				} else {
					var constantlit = litRates(0)._2
					val startYear = litRates(0)._1
					for (r <- startYear-3 to startYear+3) {
						
						val deltaYear = r - startYear
						if (deltaYear != 0) {
							var change = deltaYear * changeAmount
							var lityear = (r,constantlit + change)
							litRates = lityear :: litRates
						}
					}
					//println(x._1 + "," + j._1 + "," + j._2)
				}
			} else if (litRates.size > 1) {
				val change= litRates(litRates.size-1)._2-litRates(0)._2
				val span = litRates(litRates.size-1)._1-litRates(0)._1
				val avgChange = change/span
		
				//println(avgChange)
				if (litRates(litRates.size-1)._2 < 98) {
					totalChange += avgChange
					changeCount+= 1
				} 
				var newlitRates = litRates
				for (k <- 1 to litRates.size-1) {
					val change = litRates(k)._2 - litRates(k-1)._2
					val changeYear = litRates(k)._1 - litRates(k-1)._1
					val delta = change/changeYear
					for( g <- litRates(k-1)._1+1 to litRates(k)._1-1) {
						val deltaYear = g - litRates(k-1)._1
						var change = deltaYear * delta
						var lityear = (g,litRates(k-1)._2 + change)
						newlitRates = lityear :: newlitRates
					}
				} 
				litRates = newlitRates
				litRates = litRates.sortBy(_._1)
				val beg = litRates(0)._1
				val end = litRates(litRates.size-1)._1
				val begVal = litRates(0)._2
				val endVal = litRates(litRates.size-1)._2
				for (e <- beg-3 to beg-1) {
					val deltaYear = e - beg
					var change = deltaYear * avgChange
					var newVal = begVal + change
					if (newVal > 99) {
						newVal = 99
					}
					if (newVal > 10 && avgChange < 2) {
						var lityear = (e,newVal)
						litRates = lityear :: litRates
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
					if (newVal >= 100.0) {
						newVal = 100.0
					}
					if (newVal > 10 && avgChange < 2) {
						var lityear = (e,newVal)
						litRates = lityear :: litRates
					}
				}
			}
			litRates = litRates.sortBy(_._1)
			if (x._1 == "Nepal") {
				//litRates.foreach(x => println(x))
			}
			for( y <- litRates) {
				var lit_year = country.getOrElse(y._1.toString,List[Any]())
				if (lit_year.size != 0 && lit_year(a) == "x") {
					if (x._1 == "Nepal") {
						//println(y._1.toString)
					}
					lit_year = lit_year.updated(a,y._2)
					country += y._1.toString -> lit_year
				}
			}
			country_year += x._1 -> country

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
					//println(x._1 + " " + y._1)
					country -= y._1
				}
			}
			country_year += x._1 -> country
		}
	}

		def fixWeirdChar() {
		var total = 0
		for (x <- country_year) {
			var country = country_year.getOrElse(x._1,Map[String,List[Any]]())
			for (y <- country) {
				var add = true
				var newList = y._2
				var index = 0
				for (j <- y._2) {
					try {
						j.toString.toDouble
					} catch {
						case e : Throwable => if (j != "x") {
							newList = newList.updated(index,"x")
							println(j)
						}
					}
					if (j == "x") {
						add = false
					}
					index+=1
					country += y._1.toString -> newList
				}
				if (add == true) {
					total += 1
					//println(x._1 +  "," + y)
				}
				country_year += x._1 -> country
			}
		}	
		//println(total)
	}

	def fullData() {
		var total = 0
		for (x <- country_year) {
			var country = country_year.getOrElse(x._1,Map[String,List[Any]]())
			for (y <- country) {
				var add = true
				for (j <- y._2) {
					if (j == "x") {
						add = false
					}
				}
				if (add == true) {
					total += 1
					//println(x._1 +  "," + y)
				}

			}
		}
		println(total)
	}

	def outputs() {
		var total = 0
		for (x <- country_year) {
			var country = country_year.getOrElse(x._1,Map[String,List[Any]]())
			for (y <- country) {
				var add = true
				if(y._2(y._2.size-1) == "x") {
					add = false
				}
				if (add == true) {
					total += 1
					//println(x._1 +  "," + y)
				}

			}
		}
		println(total)
	}

	def possibles() {
		var total = 0
		for (x <- country_year) {
			var country = country_year.getOrElse(x._1,Map[String,List[Any]]())
			for (y <- country) {
				var add = true
				var gg = 0
				val year = y._1.toString.toInt
				
				if (year < 1980 || year > 2005) {
					add = false
					//println(year)
				}
				if(y._2(y._2.size-1) == "x") {
					add = false
				}
				for (j <- y._2) {
					if (j == "x") {
						gg+=1
						if (gg == 3) {
							add = false
						}
					}
				}
				if (gg <= 3 && gg != 0 && y._2(y._2.size-1) != "x" && (year >= 1980 && year <= 2005)) {
					println(x._1 + ":" + y._2)
				}
				if (add == true) {
					total += 1
					//println(x._1 +  "," + y)
				}

			}
		}
		println(total)
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