package main

import com.github.tototoshi.csv._,
import java.io._
/*
 * heavily modified nearest neighbor algorithm to
 * fill data gaps by averaging together the "k"
 * nearest neighbor's value for feature, n_i
 */

object NN {
	inFile = "data/output.csv"
	var country_year = Map[String,Map[String,List[Any]]]()

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

	def trainGaps(){
		loadCSV()

		

	}



}
