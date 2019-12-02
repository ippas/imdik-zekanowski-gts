### Data analysis:

Samples were analysed with hail (0.2.27) in jupyter notebooks. Due to bein large outliers in PCA analysis two samples: 'WGS_139', 'WGS_D6816' were excluded. What is more samples: 'S_7288' and 'S_7289' and also: 'S_7240' and 'S_7241' had their samples_id's swapped in relation with their barcodes. During the analysis this was corrected.

### data and setting up the hail enviornment

1. Hail enviornment was created in a [docker container](Dockerfile)

2. To start the container: `docker run -it --rm -p 8889:8889 -v $PWD:/hail hail-jupyter` 

3. To connect from local:`ssh -N -f -L localhost:8889:localhost:8889 ifpan` then `localhost:8889` in browser
 
