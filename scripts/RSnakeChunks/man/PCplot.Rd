% Generated by roxygen2: do not edit by hand
% Please edit documentation in R/pc_plot.R
\name{PCplot}
\alias{PCplot}
\title{Compute principal components and draw a plot with the first components}
\usage{
PCplot(x, PCs = c(1, 2), sample.desc, main = "PC plot",
  sample.labels = row.names(sample.desc),
  sample.col = sample.desc$color)
}
\arguments{
\item{x}{a data frame with genes as rows and samples as columns}

\item{PCs=c(1, 2)}{user-selected components for the XY plot}

\item{main="PC}{plot" # Main title for the plot}
}
\value{
the object of prcomp()
}
\description{
taking as input a data frame, compute principal components and draw XY plot with user-selected component numbers (default: PC1 and PC2).
}
\author{
Jacques van Helden & Fanny Casse
}
