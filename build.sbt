name := "FinalProject"

version := "1.0"

scalaVersion := "2.10.3"

mainClass := Some("main.Main")

resolvers += "Sonatype snapshots" at "http://oss.sonatype.org/content/repositories/snapshots/"

libraryDependencies += "com.github.tototoshi" %% "scala-csv" % "1.0.0-SNAPSHOT"