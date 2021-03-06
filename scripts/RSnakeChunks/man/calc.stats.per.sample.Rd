% Generated by roxygen2: do not edit by hand
% Please edit documentation in R/calc_stats_per_sample.R
\name{calc.stats.per.sample}
\alias{calc.stats.per.sample}
\title{Compute sample-wise statistics for a count table}
\usage{
calc.stats.per.sample(sample.descriptions, counts, verbose = 1)
}
\arguments{
\item{sample.descriptions}{a data.frame with one row per sample, in the same order as the columns of the count table.}

\item{counts}{a data.frame with one row per feature (gene, transcript, ...) and one column per sample. The columns of the count table must correspond to the rows of the sample descrtiption file.}

\item{verbose=1}{verbosity}
}
\description{
Compute sample-wise statistics for a count table
}
\author{
Jcaques van Helden
}
