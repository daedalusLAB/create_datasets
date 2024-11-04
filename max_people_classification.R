library(arrow)
library(logger)

args <- commandArgs(trailingOnly = TRUE)
input_folder <- args[1]
expression_year_dir <- args[2]

log_info("Input folder: {input_folder}")
log_info("Expression year directory: {expression_year_dir}")

# Load dfMaker from the correct path
tryCatch({
  load("dfMaker/dfMaker.rda")
  log_info("dfMaker loaded successfully")
}, error = function(e) {
  log_error("Error loading dfMaker: {conditionMessage(e)}")
  stop("Execution stopped due to error in loading dfMaker")
})

# Process the directory content with dfMaker
tryCatch({
  log_info("Starting dfMaker processing")
  log_info("Contents of input folder: {paste(list.files(input_folder), collapse=', ')}")
  
  clip <- dfMaker(
    input.folder = input_folder,
    no_save = TRUE,
    config.path = "dfMaker/configuration_files/config_dfMaker.json"
  )
  
  log_info("dfMaker processing completed")
  log_info("Structure of clip: {capture.output(str(clip))}")
  
}, error = function(e) {
  log_error("Error in dfMaker: {conditionMessage(e)}")
  log_error("Traceback: {paste(capture.output(traceback()), collapse='\n')}")
  stop("Execution interrupted due to an error in dfMaker")
})

# Obtener el id del clip
clip$id

# Número total de personas
num_people <- max(clip$people_id)

# Definir la ruta de salida usando expression_year_dir
output_path <- file.path(
  expression_year_dir,
  paste0(num_people, "_persons"),
  "parquet_files",
  paste0(unique(clip$id), ".parquet")
)

# Crear el directorio si no existe
output_dir <- dirname(output_path)
if (!dir.exists(output_dir)) {
  dir.create(output_dir, recursive = TRUE)
}

# Escribir el dataframe en un archivo Parquet
write_parquet(x = clip, sink = output_path)

# Guardar el número de personas en un archivo para uso posterior
num_people_file <- file.path(input_folder, "num_persons.txt")
write(num_people, file = num_people_file)

cat("Archivo procesado y guardado en:", output_path, "\n")
