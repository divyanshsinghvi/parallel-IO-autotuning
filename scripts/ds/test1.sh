mpiexec -l -n 8  -env PNETCDF_HINTS_DISPLAY=1 -env PNETCDF_HINTS="romio_ds_write=enable;nc_header_align_size=103171" ./s3d_io.x 100 200 100 2 2 2 1 F output/"
