library(rinat)
library(sf)
library(keras)
library(dplyr)

get_recs <- function(name,taxon_id){
  bounds <- readRDS("gb_simple.RDS")
  maxresults <- 100
  recs <- get_inat_obs(taxon_id = taxon_id ,bounds = bounds,
                       maxresults = maxresults,quality = "research", geo = TRUE ,query = name,)
  recs <- recs[recs$image_url != "", ]
  recs <- recs[,c("scientific_name","image_url")]
  rownames(recs) = seq(length = nrow(recs))
  return(recs)}
download_images <- function(spp_recs =NULL, image_folder =("~/BIO3199/Python/training_data/raw_images"),spp_folder=NULL){
  dir.create(image_folder, showWarnings = FALSE)
  if(is.null(spp_recs)|is.null(spp_folder)){
    print("Please set up spp_recs and spp_folder")
    return()
  }
  dir.create(paste0(image_folder,"/",spp_folder))
  for (image in 1:nrow(spp_recs)) {
    print(paste(spp_folder,":Processing image number...", image))
    spp_urlm <- spp_recs$image_url[image]
    download.file(spp_urlm,destfile=paste0(image_folder,"/",spp_folder,"/spp_"
                                           ,image,".jpg"),mode="wb")
  }
}


bird_list <- read.csv("training_species_list.csv")
for (i in 1:nrow(bird_list)){
  name <- bird_list$name[i]
  taxon_id <- as.character(bird_list$taxon_id[i])
  print(name)
  print(taxon_id)
  rec <- get_recs(name = name,taxon_id = taxon_id)
  download_images(spp_recs = rec, spp_folder = name)
}

#' Count the number of species inside the training data folder and print out the 
#' number of folders ie. the number of species the species identification model
#' is going to be trained on. 
for (species in bird_list$name){
  num_files = as.character(length(list.files(paste0("~/BIO3199/Python/training_data/raw_images",species))))
  print(paste0(num_files," images of ", species))
}  
