# Libraries required 
suppressMessages({
  library(arrow, warn.conflicts = FALSE)
  library(splines)
})

# Parsing 
args <- commandArgs(trailingOnly = TRUE)
input_file <- args[1]
output_file <- args[2]

# Load the data
data <- read.csv(file = args[1])

columnsToExpand <- c("Pitches", 
                     "Intensities",
                     "Harmonicities",
                     "Formant.1",
                     "Formant.2",
                     "Formant.3",
                     "Formant.4")

nonExpandedCols <- setdiff(names(data), columnsToExpand)

# Assuming that data is your dataframe and columnsToExpand is a vector with the names of the columns to expand
expandedData <- suppressWarnings(lapply(data[columnsToExpand], function(column) {
  do.call(rbind, strsplit(as.character(column), split = ",", fixed = TRUE))
}))

# Determine the maximum number of columns among all the matrices in all the sublists
maxCols <- max(sapply(expandedData, function(sublist) 
  max(sapply(1:nrow(sublist), function(i) ncol(sublist[i, , drop = FALSE])))))


# Adjust all the matrices to have the maximum number of columns
normalizedData <- lapply(expandedData, function(sublist) {
  lapply(1:nrow(sublist), function(i) {
    matrix <- sublist[i, , drop = FALSE]
    colsToAdd <- maxCols - ncol(matrix)
    if (colsToAdd > 0) {
      matrix <- cbind(matrix, matrix(NA, nrow = 1, ncol = colsToAdd))
    }
    return(matrix)
  })
})

# Combine all variables into a single matrix/dataframe
combinedData <- as.data.frame(do.call(cbind, lapply(columnsToExpand, function(col) unlist(normalizedData[[col]]))))
colnames(combinedData) <- columnsToExpand

# Repeat the values of each non-expanded column according to maxCols
replicatedData <- lapply(data[nonExpandedCols], function(column) rep(column, each = maxCols))

# Combine the replicated data into a dataframe
combinedReplicatedData <- as.data.frame(do.call(cbind, replicatedData))

# Final result
result <- cbind(combinedReplicatedData, combinedData)

# Generate splines for each column in columnsToExpand
for (col in columnsToExpand) {
  spline_data <- spline(x = 1:nrow(result), y = as.numeric(result[[col]]), n = nrow(result))
  result[[paste0(col, "_spline")]] <- spline_data$y
}

# Check that the output file has the extension .parquet
if (!grepl("\\.parquet$", output_file)) {
  output_file <- paste0(output_file, ".parquet")
}

# Write Parquet file
write_parquet(result, output_file)

print("Bro/Sister, otro video al saco")
