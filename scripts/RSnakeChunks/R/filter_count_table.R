#' @title Filter features of an RNA-seq count table based on a combination of user-selected criteria. 
#' @author Jacques van Helden
#' @description Filter out the features of an RNA-seq count table based on several filters. 
#' This includes suppression of features based on the following criteria:
#' \itemize{
#' \item rows with min count  smaller than specified threshold (min.count);
#' \item rows with mean count smaller than specified threshold (mean.count);
#' \item rows where all values equal zeros (unless mean.count is set to 0);
#' \item rows with null variance (optional);
#' \item rows with variance  smaller than specified threshold (min.var);
#' \item user-speficied black-listed features.
#' }
#' @param counts  A data frame with counts (one row per feature and one column per sample).
#' @param condition=NULL An optional vector indicating the  groups (condition, genotype, treatment) of each sample. Must have the same length as the number of columns of the count table. 
#' @param na.rm=FALSE Remove rows with at least one NA value.
#' @param mean.count=NULL Filter out the features having a cross-sample mean count lower than the specified value. Setting mean.count to 0 cancels the filtering out of rows where all values equal zero.
#' @param min.count=NULL Filter out features for which the  max count (across all samples) is lower than the specified threshold.
#' @param mean.per.condition=NULL  Filter out features for which none of the conditions has a mean count above the threshold
#' @param zero.var.filter=TRUE Filter out features with null variance (note: this includes rows where all values are zero but possibly other rows as well).
#' @param min.var=NULL Filter out features for which the  variance (across all samples) is lower than the specified threshold.
#' @param black.list=NULL Black-listed" features: a vector of row IDs or row indices indicating a list of features to be filtered out (e.g. 16S, 12S RNA).
#' @param verbose=1 level of verbosity
#' @return a data.frame with the same columns (samples) as the input count table, and with rows restricted to the features that pass all the thresholds.
#' @export
FilterCountTable <- function(counts,
                             condition = NULL,
                             na.omit = FALSE,
                             mean.count = NULL,
                             min.count = NULL,
                             zero.var.filter = TRUE,
                             min.var = NULL,
                             mean.per.condition = NULL,
                             black.list = NULL,
                             verbose = 1
                            ) {
  if (verbose >= 1) { message("\tFiltering count table with ", nrow(counts), " features x ", ncol(counts), " samples. ") }

  if (na.omit) {
    na.rows <- apply(is.na(counts), 1, sum) > 0
    counts <- counts[!na.rows, ]
    if (verbose >= 1) { message("\t\tomitted NA values; discarded features: ", sum(na.rows), "; kept features: ", nrow(counts)) }
    
  }
  
  ## Min count per row  
  if (!is.null(min.count)) {
    discarded <- apply(counts, 1, min, na.rm = TRUE) < min.count
    counts <- counts[!discarded, ]
    if (verbose >= 1) { message("\t\tMin count per row >= ", min.count, "; discarded features: ", sum(discarded), "; kept features: ", nrow(counts)) }
  }
  
  ## Mean count per row
  if (!is.null(mean.count)) {
    discarded <- apply(counts, 1, mean, na.rm = TRUE) < mean.count
    counts <- counts[!discarded, ]
    if (verbose >= 1) { message("\t\tMean count per row >= ", mean.count, "; discarded features: ", sum(discarded), "; kept features: ", nrow(counts)) }
  } else {
    ## If no min has been specified for mean counts per row, 
    ## suppress rows containing only zeros.
    zeros.per.row <- apply(counts == 0, 1, sum, na.rm = TRUE)
    discarded <- zeros.per.row == ncol(counts) ## Discard rows where all counts equal zero
    counts <- counts[!discarded,]
    if (verbose >= 1) { message("\t\tDiscarding rows where all values equal zero; discarded features: ", sum(discarded), "; kept features: ", nrow(counts)) }
  }

  ## Zero var filter
  if (zero.var.filter) {
    discarded <- apply(counts, 1, var, na.rm = TRUE) == 0
    counts <- counts[!discarded,]
    if (verbose >= 1) { message("\t\tDiscarting rows with null variance; discarded features: ", sum(discarded), "; kept features: ", nrow(counts)) }
  }
  
  ## Minimum var filter
  if (!is.null(min.var)) {
    discarded <- apply(counts, 1, var, na.rm = TRUE) < min.var
    counts <- counts[!discarded,]
    if (verbose >= 1) { message("\t\tMin variance per row >= ", min.var, "; discarded features: ", sum(discarded), "; kept features: ", nrow(counts)) }
  }
  
  ## Filter out black-listed features
  if (!is.null(black.list)) {
    kept <- setdiff(row.names(counts), black.list)
    counts <- counts[kept, ]
    if (verbose >= 1) { message("\t\tBlack-listed features: ", length(black.list), "; kept features: ", nrow(counts)) }
  }
  
  if (verbose >= 1) { message("\tReturning from filtered count table with ", nrow(counts), " features x ", ncol(counts), " samples. ") }
  return(counts)
}
